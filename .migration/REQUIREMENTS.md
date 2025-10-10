# 要望
[ai-docsite-translator](https://github.com/hide212131/ai-docsite-translator) を用いて、
ドキュメントサイトの原文のリポジトリ(upstream) の更新を、翻訳サイト(origin)に反映する自動翻訳フローを構築する。

## 前提
- 環境: GitHub Actions が動く実環境と、ローカルPCのローカル環境の両方で動く。
- 動作確認: ローカルPCで動作確認できる。GitHub Actions を実行できるよう、act でエミュレートして動作確認する。
- 既存運用: リポジトリ内の `.github/auto-translation` 以下のコードはすべて削除し、`ai-docsite-translator`に完全に置き換える。
- 環境変数 `GEMINI_API_KEY`, `GITHUB_TOKEN` は実環境では GitHub Secrets (`GEMINI_API_KEY`, `WORKFLOWS_GITHUB_TOKEN`) から供給し、ローカルPCは環境変数で補う

### 設定項目
```sh
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash
UPSTREAM_URL=https://github.com/jhipster/jhipster.github.io.git
ORIGIN_URL=${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}.git
ORIGIN_BRANCH=main
TRANSLATION_BRANCH_TEMPLATE='sync-<upstream-short-sha>'
MODE=batch
TRANSLATION_MODE=production  
DRY_RUN=false
MAX_FILES_PER_RUN=0
TRANSLATION_INCLUDE_PATHS=docs
TRANSLATION_DOCUMENT_EXTENSIONS=md,mdx,txt,html
```

ローカル CLI で `GITHUB_SERVER_URL` / `GITHUB_REPOSITORY` が未定義の場合は、`ORIGIN_URL` にリポジトリ URL を直接指定する。

## 確認手順
1. ローカルPCで、リポジトリの .github/workflows を編集し、actで動作確認
2. 実環境で .github/workflows の確認
    1. 最初は、以下の特定の1つのコミットだけ翻訳する
    ```sh
    TRANSLATION_TARGET_SHA=2d83acfe
    ```
    2. そのあと、最も古い2つの未翻訳のコミットに対して翻訳する
    3. 最後に、すべての未翻訳に対して翻訳する
