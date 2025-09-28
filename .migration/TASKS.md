# ai-docsite-translator 移行タスクリスト

## 1. 旧ワークフローの整理
- [x] `.github/auto-translation/**` のコードと関連ドキュメントを削除
- [x] `README.md` / `DEPLOYMENT_GUIDE.md` から旧パイプラインの記述を整理

## 2. 新フローのファイル追加・調整
- [x] `.github/workflows/ai-docsite-translation.yml` を作成し、`hide212131/ai-docsite-translator@<commit-sha>` を呼び出す
- [x] `.gitignore` に `.env.translator` と `.tools/cache/` を追記
- [x] `.env.translator.sample` / `.secrets.translator.sample` を追加
- [x] `tools/run-ai-docsite-translator.sh` を追加しローカル実行を整備
- [x] `.github/llm-translation/docs/runbook.md` を作成し運用手順・段階的翻訳プロセスを記載
- [x] `.migration/SPEC.md` と整合が取れていることを確認

## 3. GitHub Actions 設定
- [x] スケジュール (`cron: "30 3 * * *"`) と `workflow_dispatch` を設定
- [x] `translate` ジョブで `actions/checkout@v4` (fetch-depth: 0) と `actions/setup-java@v4` (Temurin 21) を実行
- [x] `hide212131/ai-docsite-translator` の `with` / `env` を REQUIREMENTS.md の環境変数に合わせて指定
- [x] `concurrency` 設定と `timeout-minutes` (90) を付与
- [x] `GEMINI_API_KEY` 未設定時に早期終了するガードを追加

## 4. Secrets / 環境変数整備
- [ ] 本番リポジトリに `GEMINI_API_KEY` と `GITHUB_TOKEN` (必要なら Bot 用 `GH_TOKEN`) を登録
- [ ] Bot 用 Git ユーザー名・メールを決定し Secrets (or Action args) に登録
- [x] `.env.translator` (未コミット) を用意しローカル用環境変数を設定

## 5. 段階的リリース / 検証
- [x] ローカル CLI (`tools/run-ai-docsite-translator.sh`) で `DRY_RUN=true`, `TRANSLATION_MODE=mock`, `TRANSLATION_TARGET_SHA=2d83acfe` にて検証
- [ ] `act -j translate --secret-file .secrets.translator --env TRANSLATION_TARGET_SHA=2d83acfe` でワークフローを再現
- [ ] GitHub Actions を `workflow_dispatch` で起動し、`TRANSLATION_TARGET_SHA=2d83acfe` のみ翻訳 (Phase 1)
- [ ] "未翻訳が最も古い 2 コミット" を対象にする実行方法を調査し、実現する (Phase 2)
- [ ] すべての未翻訳コミットを翻訳する本運用に移行し、`schedule` トリガーを有効化 (Phase 3)

> メモ: ローカル CLI から本番リポジトリへ実行し PR #82 を作成済み。GitHub Actions の `workflow_dispatch` での検証は未実施。

## 6. フォローアップ / 未確定事項
- [ ] `ai-docsite-translator` に古いコミットを優先する CLI オプションが存在するか確認し、欠けていれば issue を作成
- [ ] `GEMINI_API_KEY` が未設定の PR (fork 等) でスキップする挙動の是非を決定
- [ ] 初回運用結果を runbook に反映し、残作業をレビュー
- [ ] Action のバージョン pin を定期的に見直す運用 (例: 四半期) を runbook に追記
