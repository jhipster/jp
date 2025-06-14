# JHipster 日本語ドキュメント自動翻訳 **spec.md**

---

## 目的

- **upstream:** `jhipster/jhipster.github.io` (英語)
- **origin :** `jhipster.github.io-jp` (日本語)
- upstream の更新を一定周期で取り込み、LLM (Gemini) により日本語翻訳した PR を自動生成する。
- 同一処理をローカルでも再現可能にし、開発・デバッグコストを抑える。

## 対象ファイル

| 種別  | 拡張子                                                              | 翻訳要否              |
| --- | ---------------------------------------------------------------- | ----------------- |
| 文書  | `.md` `.mdx` `.adoc` `.html`                                     | **翻訳対象**          |
| 非文書 | `.png` `.jpg` `.svg` `.json` `.yml` `.yaml` `.conf` `.js` `.css` | **翻訳対象外** (コピーのみ) |

---

## GitHub Actions

### トリガー

```yaml
on:
  schedule:
    - cron:  "0 3 * * *"   # 毎日 12:00 JST (UTC 03:00)
  workflow_dispatch:         # 手動実行
```

### Secrets (必須)

| 名称               | 用途                  |
| ---------------- | ------------------- |
| `GEMINI_API_KEY` | Gemini API キー       |
| `GH_TOKEN`       | PR 作成用 GitHub Token |
| `BOT_GIT_USER`   | コミットユーザー名           |
| `BOT_GIT_EMAIL`  | コミットメール             |

---

## ディレクトリ構成 (抜粋)

```text
└─ scripts/
   ├─ fetch_upstream.py   # upstream 取得 + merge
   ├─ classify_changes.py # a/b-1/b-2/c 判定
   ├─ translate_chunk.py  # 単一ファイル翻訳
   ├─ postprocess.py      # 行数検査・衝突解消
   └─ commit_and_pr.py    # コミット & PR 作成
```

- **言語:** Python 3.11
- **依存:** Poetry 管理 (`poetry.lock`)

---

## ワークフロー詳細

1. **ブランチ生成**
   ```bash
   git checkout origin/main
   HASH=$(git ls-remote https://github.com/jhipster/jhipster.github.io.git refs/heads/main | cut -c1-7)
   BRANCH="sync-${HASH}"
   git switch -c "$BRANCH"
   ```
2. **強制マージ** (`git merge -s ours` を併用)
3. **変更判定** (`classify_changes.py`)
   - `git diff --name-status origin/main..HEAD` でファイル一覧取得
   - ファイルごとに次を判定
     | 状態                    | 判定条件                             |
     | --------------------- | -------------------------------- |
     | a. 新規文書               | `status == "A"` & 翻訳対象拡張子        |
     | b-1. 追記 (No conflict) | `status == "M"` かつ 差分に `<<<<` 無し |
     | b-2. 衝突 (Conflict)    | 差分に `<<<<` 含む                    |
     | c. 非文書／除外             | 翻訳対象外拡張子                         |
4. **Gemini 翻訳** (`translate_chunk.py`)
   - 4096 tokens 超は段落単位で分割
   - プロンプト先頭に `style-guide.md` をインジェクト
   - 出力後、原文と行数一致を確認
5. **ポストプロセス** (`postprocess.py`)
   - コンフリクトマーカー全削除 (`<<<<` `====` `>>>>`)
   - `language_tool_python` で簡易文法チェック
6. **コミット & PR**
   - コミットメッセージ: `docs(sync): upstream ${HASH} 翻訳`
   - PR タイトル: `docs: upstream ${HASH} Translation`
   - PR 本文: 差分ファイル表 (Markdown)

---

## ローカル実行

### 1コミットだけ翻訳

```bash
poetry install
python scripts/fetch_upstream.py --hash <commit-sha>
python scripts/classify_changes.py
python scripts/translate_chunk.py --mode selective
python scripts/commit_and_pr.py --push-origin false
```

- `make run` で全体一括処理も可能。

---

## Style Guide (docs/style-guide.md)

- 文体: 常体 (です・ます調 **禁止**)
- 長音符・半角英数字統一
- 用語統一表 (例: *Generator* → *ジェネレータ*)

---

## テスト

- `pytest` + `unittest.mock` で Gemini 呼出をスタブ
- a/b-1/b-2/c ケース毎の fixture ファイル
- GitHub Actions 内で `pytest -q` 実行

---

## ライセンス & コンプライアンス

- 生成物は upstream の MIT ライセンスを継承
- Gemini 利用規約への参照リンクを README に記載

---

## 変更履歴

| 日付         | 変更 | 執筆者             |
| ---------- | -- | --------------- |
| 2025-06-15 | 初版 | AI Coding Agent |

