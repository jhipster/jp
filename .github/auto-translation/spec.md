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

> **ポイント**: まず *衝突マーカーを含んだままコミット* し、その後に翻訳／マーカー除去を行う 2 段階コミット構成とする。

| ステップ                                                                                                                                           | 処理         | 主要コマンド・スクリプト |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------------ |
| 1                                                                                                                                              | **ブランチ生成** | \`\`\`bash   |
| git checkout origin/main                                                                                                                       |            |              |
| HASH=\$(git ls-remote [https://github.com/jhipster/jhipster.github.io.git](https://github.com/jhipster/jhipster.github.io.git) refs/heads/main | cut -c1-7) |              |
| BRANCH="sync-\${HASH}"                                                                                                                         |            |              |
| git switch -c "\$BRANCH"                                                                                                                       |            |              |

````|
| 2 | **強制マージ & コンフリクト込みコミット**<br>（一次コミット） | ```bash
git merge upstream/main --allow-unrelated-histories --no-edit || true
# 衝突状態でもステージする
git add -A
# デフォルトメッセージでコミット（衝突マーカー残存）
git commit --no-edit || true
``` |
| 3 | **変更判定 (a/b-1/b-2/c)** | `scripts/classify_changes.py` (`HEAD^` vs `HEAD` で diff 解析) |
| 4 | **Gemini 翻訳**<br>（衝突マーカーも入力に含める） | `scripts/translate_chunk.py` — 翻訳後にマーカー除去 & 行数チェック |
| 5 | **ポストプロセス & 翻訳コミット**<br>（二次コミット） | ```bash
python scripts/postprocess.py   # マーカー除去 ＋ 文法チェック
git add -A
git commit -m "docs(translate): upstream ${HASH} 日本語翻訳" --no-verify
``` |
| 6 | **PR 作成** | `scripts/commit_and_pr.py` → `gh pr create` |

### PR本文生成

自動翻訳システムで作成されるPRには以下の内容が含まれる：

#### 基本情報
- 翻訳元コミットハッシュ（JHipster upstream リポジトリへのリンク付き）
- 自動検出されたベースブランチ（main または auto-translation）
- **翻訳元英文参照リンク**：各翻訳対象ファイルの上流版へのGitHubリンク
  - 形式：`https://github.com/jhipster/jhipster.github.io/blob/{commit_hash}/{file_path}`
  - 例：`https://github.com/jhipster/jhipster.github.io/blob/abc1234/docs/installation.md`

#### 翻訳品質分析
1. **行数差異検出**：上流版と翻訳版で行数差（1行以上）があるファイルを検出
2. **LLM詳細分析**：行数差があるファイルのみをGemini 1.5 Flashで詳細分析
   - 重要な情報の欠落（import文、画像、リンク、コンポーネントなど）
   - 構造的な変更（セクション、段落の削除・追加）
   - マークダウン記法の問題
   - 意図しない内容の重複
   - 翻訳の一貫性

#### ファイル分類情報
- 総ファイル数と翻訳対象ファイル数
- 新規文書（カテゴリA）：各ファイル名に翻訳元英文リンク付き
- 更新文書 - 衝突なし（カテゴリB-1）：各ファイル名に翻訳元英文リンク付き
- 更新文書 - 衝突あり（カテゴリB-2）：各ファイル名に翻訳元英文リンク付き、手動確認推奨
- 非翻訳ファイル（カテゴリC）：各ファイル名に翻訳元英文リンク付き

**リンク表示例**：
```markdown
- `docs/installation.md` - [翻訳元を確認](https://github.com/jhipster/jhipster.github.io/blob/abc1234/docs/installation.md)
```

#### 品質保証機能
- **コンフリクトマーカー検出**：`<<<<<<<`、`=======`、`>>>>>>>`の残存をチェック
- **翻訳品質問題の重要度分類**：高（🚨）、中（⚠️）、低（ℹ️）
- **手動レビュー推奨箇所の明示**
- **LLM分析対象ファイルの翻訳元リンク**：行数差異が検出されたファイルの詳細分析結果に翻訳元英文リンクを併記

#### PR本文での翻訳元リンク生成ルール
1. **URL形式**：`https://github.com/jhipster/jhipster.github.io/blob/{commit_hash}/{file_path}`
2. **リンクテキスト**：「翻訳元を確認」
3. **適用対象**：全ての翻訳対象ファイル（カテゴリA, B-1, B-2）および非翻訳ファイル（カテゴリC）
4. **表示場所**：各ファイルリストでファイル名の直後に併記

---

## ローカル実行

### 1コミットだけ翻訳（2段階コミットを再現）

```bash
poetry install
python scripts/fetch_upstream.py --hash <commit-sha>        # ステップ1 & 2
python scripts/classify_changes.py                           # ステップ3
python scripts/translate_chunk.py --mode selective           # ステップ4
python scripts/postprocess.py                                # ステップ5-前半
python scripts/commit_and_pr.py --push-origin false          # ステップ5-後半/6
````

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

### スタイルガイドのカスタマイズ
特定のフォルダ以下のドキュメントに対して、文体を揃えるため、独自のスタイルガイドを適用する。
- `docs/releases` については、`.github/auto-translation/docs/style-guide-release.md` を適用

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

