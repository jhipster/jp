# デプロイメントガイド

本書は jhipster.github.io-jp のデプロイと翻訳運用をまとめたものです。

## Web サイトのビルドと公開

GitHub Pages (`gh-pages` ブランチ) により公開します。通常の更新手順は次の通りです。

1. 依存関係をインストール: `npm install`
2. 本番ビルドを実行: `npm run build`
3. GitHub Pages へデプロイ: `USE_SSH=true npm run deploy` または `GIT_USER=<your-account> npm run deploy`

自動化された翻訳ブランチ (`sync-*`) は `main` にマージしてからデプロイしてください。

## 翻訳オートメーションの概要

- **アクション**: `.github/workflows/ai-docsite-translation.yml`
- **翻訳エンジン**: [`hide212131/ai-docsite-translator`](https://github.com/hide212131/ai-docsite-translator)
- **スケジュール**: `cron: "30 3 * * *"`（毎日 12:30 JST）と `workflow_dispatch`
- **主な環境変数**: `GEMINI_API_KEY`, `GITHUB_TOKEN`, `LLM_PROVIDER=gemini`, `LLM_MODEL=gemini-2.5-flash`
- **成果物**: upstream の未翻訳コミットごとに `sync-<upstream-short-sha>` ブランチを作成し PR を発行

詳細な運用手順と段階的リリース方針は `.github/llm-translation/docs/runbook.md` を参照してください。

## ローカル検証

ローカルで翻訳パイプラインを試すときは以下の 2 つの方法があります。

1. `tools/run-ai-docsite-translator.sh`
   - `.env.translator` を作成して `GEMINI_API_KEY` などを設定。
   - `DRY_RUN=true` や `TRANSLATION_MODE=mock` を指定して挙動を確認。
2. [`act`](https://github.com/nektos/act)
   - `.secrets.translator` に `GEMINI_API_KEY` と `GITHUB_TOKEN` を記載。
   - `act -j translate --secret-file .secrets.translator` で GitHub Actions を再現。

## Secrets / 環境変数メモ

| 名前 | 用途 |
| ---- | ---- |
| `GEMINI_API_KEY` | Gemini API へのアクセスキー |
| `GITHUB_TOKEN` | 翻訳結果ブランチの push / PR 作成 |
| `LLM_PROVIDER` | LLM プロバイダー（既定: `gemini`） |
| `LLM_MODEL` | 使用モデル（既定: `gemini-2.5-flash`） |
| `TRANSLATION_TARGET_SHA` | 段階的翻訳時に対象コミットを固定する任意設定 |

Secrets の設定状況は GitHub リポジトリ設定で確認し、runbook のチェックリストに従ってメンテナンスしてください。
