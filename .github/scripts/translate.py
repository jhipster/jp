# .github/scripts/translate.py
import os, sys, subprocess, re, difflib, datetime, time, textwrap
from patch_ng import fromstring as patch_fromstr
import google.generativeai as genai

MODE          = sys.argv[1] if len(sys.argv) > 1 else "full"
UPSTREAM_DIR  = "upstream"
FROM_SHA      = os.environ.get("FROM_SHA", "").strip()
API_KEY       = os.environ["GEMINI_API_KEY"]
TRANS_MODEL   = os.environ.get("GEMINI_TRANSLATE_MODEL", "models/gemini-1.5-pro")
REVIEW_MODEL  = os.environ.get("GEMINI_REVIEW_MODEL", TRANS_MODEL)
SRC_LANG      = os.environ.get("SOURCE_LANG", "en")
TGT_LANG      = os.environ.get("TARGET_LANG", "ja")
BR_PREFIX     = os.environ.get("BR_PREFIX", "auto-translate")
UPSTREAM_REPO = os.environ["UPSTREAM_REPO"]

genai.configure(api_key=API_KEY)

def git(dir_, *args):
    return subprocess.check_output(["git", "-C", dir_, *args], text=True).strip()

def git_local(*args):     return git(".", *args)
def git_upstream(*args):  return git(UPSTREAM_DIR, *args)

latest = git_upstream("rev-parse", "HEAD")

# jp 側で最後の翻訳コミットを探す
try:
    msg = git_local("log", "-E", "--grep", r"upstream [0-9a-f]{7}", "-n1", "--pretty=%s")
except subprocess.CalledProcessError:
    msg = ""
m = re.search(r"upstream ([0-9a-f]{7,40})", msg)
base = None
if m:
    try:
        base = git_upstream("rev-parse", m.group(1))
    except subprocess.CalledProcessError:
        base = None
if not base and FROM_SHA:
    base = git_upstream("rev-parse", FROM_SHA)

commit_range = f"{base}..{latest}" if base else f"{latest}~1..{latest}"
commits = git_upstream("rev-list", "--reverse", commit_range).split()
if MODE == "test" and commits:
    commits = commits[:1]

if not commits:
    open(os.environ["GITHUB_ENV"], "a").write("PULL_REQUEST_BRANCH=\n")
    sys.exit(0)

def ask(model, prompt, text, max_tokens=2048):
    for attempt in range(3):
        try:
            # Make the API request
            response = genai.GenerativeModel(model).generate_content(
                [{"role":"user","text":prompt},{"role":"user","text":text}])
            
            # Debug logging of response structure
            print(f"Response type: {type(response).__name__}")
            print(f"Response attributes: {dir(response)}")
            
            # Validate response
            if not hasattr(response, 'text'):
                print(f"WARNING: Response missing 'text' attribute. Full response: {response}")
                if hasattr(response, 'parts'):
                    print(f"Response parts: {response.parts}")
                if hasattr(response, 'candidates'):
                    print(f"Response candidates: {response.candidates}")
                raise KeyError("Response is missing 'text' attribute")
            
            # Return the text content if valid
            return response.text.strip()
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {type(e).__name__} - {e}")
            # Log additional debugging information
            print(f"Model: {model}, Text length: {len(text)}")
            
            # If we have response details, log them for debugging
            if 'response' in locals():
                print(f"Response details: {response}")
            
            time.sleep(5 + attempt * 5)  # Exponential backoff: 5s, 10s, 15s
    
    error_msg = f"Gemini API interaction failed after 3 attempts with model {model}"
    print(f"ERROR: {error_msg}")
    raise RuntimeError(error_msg)

REVIEW_PROMPT = textwrap.dedent("""\
    以下は Git 差分です
    ---
    {diff}
    ---
    日本語翻訳が必要なら YES、不要なら NO とだけ答えてください
    - タイポ修正や Bot 更新なら NO
    """)

def needs_translation(diff_txt):
    return ask(REVIEW_MODEL, REVIEW_PROMPT.format(diff=diff_txt[:12000]), "").upper().startswith("Y")

def translate_md(txt):
    return ask(TRANS_MODEL,
               "Markdown の構造を保ったまま英語→日本語に翻訳してください。コードブロックと URL は翻訳しないでください。",
               txt, 8192)

def added_chunks(old, new):
    diff = difflib.unified_diff(old.splitlines(1), new.splitlines(1), lineterm="")
    chunks, buf, start = [], [], None
    for l in diff:
        if l.startswith("@@"):
            if buf:
                chunks.append(("".join(buf), start))
                buf = []
            start = int(l.split(" ")[2].split(",")[0][1:])
        elif l.startswith("+") and not l.startswith("+++"):
            buf.append(l[1:] + "\n")
    if buf:
        chunks.append(("".join(buf), start))
    return chunks

git_local("config", "user.name",  "github-actions")
git_local("config", "user.email", "github-actions@no-reply.github.com")
branch = f"{BR_PREFIX}-{datetime.datetime.now():%Y%m%d-%H%M%S}"
git_local("checkout", "-b", branch)

pr_lines = []

for c in commits:
    diff_txt = git_upstream("diff", f"{c}~1", c)
    if not needs_translation(diff_txt):
        continue

    subj = git_upstream("show", "-s", "--format=%s", c)
    files = git_upstream("diff-tree", "--no-commit-id", "--name-only", "-r", c).split()
    changed = False

    for p in files:
        if not p.endswith(".md"):
            continue
        try:
            old = git_upstream("show", f"{c}~1:{p}")
        except subprocess.CalledProcessError:
            old = ""
        new = git_upstream("show", f"{c}:{p}")
        hunks = added_chunks(old, new)
        if not hunks:
            continue

        try:
            jp_current = open(p, encoding="utf-8").read()
        except FileNotFoundError:
            jp_current = ""

        patch_body = []
        for chunk, _ in hunks:
            ja = translate_md(chunk)
            patch_body += ["@@\n"] + ["+" + l for l in ja.splitlines(1)]
        if not patch_body:
            continue

        patch_txt = f"--- a/{p}\n+++ b/{p}\n{''.join(patch_body)}"
        jp_new = patch_fromstr(patch_txt).apply(jp_current) or translate_md(new)

        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(jp_new)
        git_local("add", p)
        changed = True

    if changed:
        short = c[:7]
        git_local("commit", "-m", f"Translate: {subj} (upstream {short})")
        pr_lines.append(f"- [{short}](https://github.com/{UPSTREAM_REPO}/commit/{c}) : {subj}")

if git_local("rev-list", f"{branch} --not origin/{os.environ['BASE_BRANCH']}"):
    git_local("push", "origin", branch)
    env = f"PULL_REQUEST_BRANCH={branch}\nPR_BODY={'\\n'.join(pr_lines)}\n"
    open(os.environ["GITHUB_ENV"], "a").write(env)
else:
    open(os.environ["GITHUB_ENV"], "a").write("PULL_REQUEST_BRANCH=\n")
