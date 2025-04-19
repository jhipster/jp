# .github/scripts/translate.py
import os, sys, subprocess, re, difflib, datetime, time, textwrap
from patch_ng import fromstring as patch_fromstr
import google.generativeai as genai

MODE          = sys.argv[1] if len(sys.argv) > 1 else "full"
UPSTREAM_DIR  = "upstream"
FROM_SHA      = os.environ.get("FROM_SHA", "").strip()
API_KEY       = os.environ["GEMINI_API_KEY"]
TRANS_MODEL   = os.environ.get("GEMINI_TRANSLATE_MODEL", "models/gemini-2.5-flash")
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

def ask(model, prompt, text, max_tokens=2048):
    for attempt in range(3):
        try:
            # Make the API request - 修正: 正しいフォーマットでリクエストを送信
            content = f"{prompt}\n\n{text}" if text else prompt
            response = genai.GenerativeModel(model).generate_content(content)
            
            # LLMの回答を明示的に表示
            response_text = response.text.strip()
            print(f"\n=== LLM Response (Model: {model}) ===")
            print(response_text)
            print(f"=== End of LLM Response ===\n")
            
            # Return the text content if valid
            return response_text
            
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
    print(f"翻訳判断を開始します - 差分テキスト長: {len(diff_txt)} バイト")
    try:
        result = ask(REVIEW_MODEL, REVIEW_PROMPT.format(diff=diff_txt[:12000]), "")
        is_needed = result.upper().startswith("Y")
        print(f"翻訳判断結果: {'必要' if is_needed else '不要'} (AI回答: '{result}')")
        return is_needed
    except Exception as e:
        print(f"翻訳判断中にエラーが発生しました: {e}")
        # エラーの場合は安全策として必要と判断
        print(f"エラーが発生したため、安全策として翻訳必要と判断します")
        return True

def translate_md(txt):
    """
    テキストを英語から日本語に翻訳する
    英語の元テキストの行数を数え、同じ行数で翻訳するように指示する
    """
    # 行数をカウント
    line_count = len(txt.splitlines())
    
    return ask(TRANS_MODEL,
               f"""
以下の内容を英語から日本語に翻訳してください。
重要な点:
1. マークダウンの構造を完全に保ってください
2. コードブロック、URLは翻訳せず、そのまま維持してください
3. 技術用語は適切な日本語訳またはカタカナで表記してください
4. 翻訳結果は必ず原文と同じ {line_count} 行にしてください
5. 行の対応関係を維持してください - 原文の1行目は訳文の1行目に、原文の2行目は訳文の2行目に対応するようにしてください
6. 空行は空行のまま保持してください
7. 行を結合したり分割したりしないでください
               """,
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

def translate_and_apply_diff(jp_current, diff_txt, new_content):
    """
    LLMを使用してファイル全体または差分の翻訳を行う
    
    Args:
        jp_current: 現在の日本語翻訳ファイルの内容（行番号なし）
        diff_txt: git diffの出力（行番号あり）
        new_content: 新しい英語のコンテンツ全体
        
    Returns:
        更新された日本語翻訳ファイルの内容
    """
    # 日本語ファイルに行番号を付与
    jp_numbered = "\n".join([f"{i+1}: {line}" for i, line in enumerate(jp_current.splitlines())])
    
    # 原文の行数をカウント
    original_line_count = len(new_content.splitlines())
    
    if not jp_current.strip():
        # 新規ファイルの場合は全体翻訳
        prompt = f"""
新しい英語のドキュメントを日本語に翻訳してください。マークダウンの構造、コードブロック、URLはそのまま維持してください。
重要な点:
1. 翻訳結果は必ず原文と同じ {original_line_count} 行にしてください
2. 行の対応関係を維持してください - 原文の1行目は訳文の1行目に、原文の2行目は訳文の2行目に対応するようにしてください
3. 空行は空行のまま保持してください
4. 行を結合したり分割したりしないでください
5. コードブロック、URL、技術用語は適切に処理してください

英語の原文:
{new_content}
"""
        return ask(TRANS_MODEL, prompt, "", 8192)
    else:
        # 差分適用の場合
        prompt = f"""
現在の日本語ドキュメントに、英語の差分を反映して翻訳してください。
マークダウンの構造、コードブロック、URLはそのまま維持してください。

現在の日本語ドキュメント（行番号付き）:
{jp_numbered}

英語の変更差分（行番号付き）:
{diff_txt}

指示:
1. 上記の英語の変更差分を日本語に翻訳し、該当する行番号の箇所に適用してください
2. 新規文書は全体を翻訳して出力してください
3. 変更の場合は行番号付近を探して翻訳を挿入し、全体を出力してください
4. 出力は行番号なしの日本語テキスト全体を返してください
5. 翻訳結果は必ず原文と同じ行数にしてください
6. 行の対応関係を維持してください - 原文の1行目は訳文の1行目になるようにしてください
"""
        return ask(TRANS_MODEL, prompt, "", 8192)

# 全体をtry-exceptで囲み、エラーが発生した場合に詳細情報を表示する
if __name__ == "__main__":
    try:
        # テストモードの場合は、指定された FROM_SHA を強制的に使用
        if MODE == "test" and FROM_SHA:
            print(f"テストモード: FROM_SHA={FROM_SHA} を使用します")
            # テストモードではFROM_SHAのコミット自体を処理対象とする
            try:
                commit_sha = git_upstream("rev-parse", FROM_SHA).strip()
                if commit_sha:
                    commits = [commit_sha]
                    print(f"処理対象コミット: {commit_sha}")
                else:
                    commits = []
                    print(f"指定されたFROM_SHA={FROM_SHA}が見つかりません")
            except subprocess.CalledProcessError:
                commits = []
                print(f"指定されたFROM_SHA={FROM_SHA}の取得でエラーが発生しました")
        else:
            # 通常のモードでは従来の方法で対象コミットを特定
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

        git_local("config", "user.name",  "github-actions")
        git_local("config", "user.email", "github-actions@no-reply.github.com")
        branch = f"{BR_PREFIX}-{datetime.datetime.now():%Y%m%d-%H%M%S}"
        git_local("checkout", "-b", branch)

        pr_lines = []
        any_changes = False  # 何らかの変更があったかを追跡する変数を追加

        for c in commits:
            try:
                diff_txt = git_upstream("diff", f"{c}~1", c)
                print(f"\n=== 処理対象のコミット: {c} ===")
                print(f"差分サイズ: {len(diff_txt)} バイト")
                
                needs_trans = needs_translation(diff_txt)
                print(f"翻訳判断結果: {'必要' if needs_trans else '不要'}")
                
                if not needs_trans:
                    print(f"コミット {c[:7]} は翻訳不要と判断されたためスキップします")
                    continue

                subj = git_upstream("show", "-s", "--format=%s", c)
                files = git_upstream("diff-tree", "--no-commit-id", "--name-only", "-r", c).split()
                print(f"変更ファイル数: {len(files)}")
                print(f"変更ファイル一覧: {files}")
                changed = False
                processed_files = 0

                for p in files:
                    try:
                        # 拡張子による制限を削除
                        print(f"ファイル処理: {p}")
                        processed_files += 1
                        
                        try:
                            old = git_upstream("show", f"{c}~1:{p}")
                            print(f"元のコンテンツ取得: {p} ({len(old)} バイト)")
                        except subprocess.CalledProcessError as e:
                            old = ""
                            print(f"元のコンテンツなし (新規ファイル): {p}")
                            
                        new = git_upstream("show", f"{c}:{p}")
                        print(f"新しいコンテンツ取得: {p} ({len(new)} バイト)")
                        
                        # テキストファイル以外はスキップ（バイナリファイル対策）
                        if b'\0' in new.encode('utf-8', errors='ignore'):
                            print(f"バイナリファイルと判断してスキップ: {p}")
                            continue
                        
                        # 差分取得（行番号付きのgit diff形式）
                        try:
                            diff_with_lines = git_upstream("diff", f"{c}~1", c, "--", p)
                            print(f"差分テキスト取得（行番号付き）: {len(diff_with_lines)} バイト")
                        except subprocess.CalledProcessError as e:
                            print(f"差分取得でエラー: {e}")
                            continue

                        try:
                            jp_current = open(p, encoding="utf-8").read()
                            print(f"現在のファイル読み込み: {p} ({len(jp_current)} バイト)")
                        except FileNotFoundError:
                            jp_current = ""
                            print(f"現在のファイルなし (新規作成): {p}")
                        except UnicodeDecodeError:
                            print(f"ファイル読み込みエラー (UTF-8でない可能性): {p} - スキップします")
                            continue

                        # 差分が実際にあるか確認 
                        if not diff_with_lines.strip():
                            print(f"有効な差分がないためスキップ: {p}")
                            continue
                            
                        # LLMを使用して翻訳と差分適用を行う
                        print(f"LLMによる翻訳差分適用を開始: {p}")
                        jp_new = translate_and_apply_diff(jp_current, diff_with_lines, new)
                        
                        if not jp_new.strip():
                            print(f"翻訳結果が空のためスキップ: {p}")
                            continue
                            
                        # 結果を保存
                        os.makedirs(os.path.dirname(p), exist_ok=True)
                        with open(p, "w", encoding="utf-8") as f:
                            f.write(jp_new)
                        git_local("add", p)
                        changed = True
                        print(f"ファイル {p} を正常に翻訳して追加しました")
                    except Exception as e:
                        print(f"ファイル {p} の処理中にエラーが発生しました: {e}")
                        import traceback
                        traceback.print_exc()

                if changed:
                    any_changes = True  # 何らかの変更があったことを記録
                    short = c[:7]
                    git_local("commit", "-m", f"Translate: {subj} (upstream {short})")
                    pr_lines.append(f"- [{short}](https://github.com/{UPSTREAM_REPO}/commit/{c}) : {subj}")
                    print(f"コミット {short} の翻訳を完了し、コミットしました")
                else:
                    print(f"コミット {c[:7]} には翻訳可能なファイルがなかったか、翻訳に失敗しました")
            
            except Exception as e:
                print(f"コミット {c[:7]} の処理中にエラーが発生しました: {e}")
                import traceback
                traceback.print_exc()

        # 変更がある場合のみプッシュする
        try:
            if any_changes and git_local("rev-list", branch, "--not", f"origin/{os.environ['BASE_BRANCH']}"):
                print(f"変更があるため、ブランチ {branch} をプッシュします")
                git_local("push", "origin", branch)
                pr_body = '\n'.join(pr_lines)
                env = f"PULL_REQUEST_BRANCH={branch}\nPR_BODY={pr_body}\n"
                open(os.environ["GITHUB_ENV"], "a").write(env)
                print("プルリクエスト作成のための情報を設定しました")
            else:
                print("翻訳が必要な変更が見つからなかったか、エラーが発生したため、プッシュは行いません")
                open(os.environ["GITHUB_ENV"], "a").write("PULL_REQUEST_BRANCH=\n")
        except Exception as e:
            print(f"プッシュ処理中にエラーが発生しました: {e}")
            import traceback
            traceback.print_exc()
            open(os.environ["GITHUB_ENV"], "a").write("PULL_REQUEST_BRANCH=\n")
            
    except Exception as e:
        print(f"スクリプト全体でエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
