# ai-docsite-translator Runbook

本書は `ai-docsite-translator` を用いた翻訳自動化の運用手順をまとめたものです。

## 1. 概要
- 実行主体: GitHub Actions ワークフロー `.github/workflows/ai-docsite-translation.yml`
- 実行スケジュール: 毎日 12:30 JST (`cron: "30 3 * * *"`)
- 翻訳エンジン: [`hide212131/ai-docsite-translator`](https://github.com/hide212131/ai-docsite-translator)（ブランチ: `main`）
- 生成ブランチ: `sync-<upstream-short-sha>` 形式。PR は `main` 向けに自動作成。
- 翻訳対象: `docs/` 配下、拡張子 `md, mdx, txt, html`
- origin-url: `${{ github.server_url }}/${{ github.repository }}.git` を採用し、フォークや組織移転にも追従

## 2. Secrets / 環境変数
| 名称 | 設定場所 | 説明 |
| ---- | ---- | ---- |
| `GEMINI_API_KEY` | GitHub Secrets | Gemini API キー（未設定時は実行スキップ） |
| `WORKFLOWS_GITHUB_TOKEN` | GitHub Secrets | PAT。`actions/checkout` と翻訳アクションの `GITHUB_TOKEN` に供給 |
| `BOT_GIT_USER` | GitHub Secrets (任意) | PR/コミットの表示名 |
| `BOT_GIT_EMAIL` | GitHub Secrets (任意) | PR/コミットのメールアドレス |
| `.env.translator` | ローカルファイル | ローカル CLI 用環境変数 (Git 管理外) |
| `.secrets.translator` | ローカルファイル | `act` 用シークレット定義 |

**チェックリスト**
- [ ] `GEMINI_API_KEY` と `WORKFLOWS_GITHUB_TOKEN` が設定されている
- [ ] Bot 名義を利用する場合は `BOT_GIT_USER` / `BOT_GIT_EMAIL` を登録
- [ ] `.env.translator` にローカル検証用の環境変数を記入（コミット禁止）

## 3. GitHub Actions 実行手順
### 定期実行
設定済みの `schedule` に任せる。ジョブは `concurrency: ai-docsite-translation` により重複実行されない。

### 手動実行 (`workflow_dispatch`)
1. Actions タブから `ai-docsite-translation` を選択し `Run workflow`。
2. 必要であれば以下の入力を指定:
   - `translation_target_sha`: 翻訳対象 upstream short SHA を固定
   - `translation_limit`: 翻訳ファイル数の上限
   - `translation_mode`: `production` / `dry-run` / `mock`
3. 実行ログで `Translation branch` や PR 作成状態を確認。

補足: `actions/checkout` と翻訳アクションの両方で `WORKFLOWS_GITHUB_TOKEN` (PAT) を使用する。権限変更時は Secrets をローテーションする。

### ガード動作
`GEMINI_API_KEY` が未設定の場合、ワークフローは早期にスキップし、ログに警告を出力する。Secrets を更新後に再実行すること。

## 4. ローカル検証
### shell スクリプト
```bash
cp .env.translator.sample .env.translator
# 必要な値を編集（DRY_RUN=true, TRANSLATION_MODE=mock など）
./tools/run-ai-docsite-translator.sh --limit 5 --log-format text
```
- 初回実行時に `.tools/cache/ai-docsite-translator` へクローンする。
- `MODE=dev` と `TRANSLATION_MODE=mock` を推奨。Git 操作は `DRY_RUN=true` で抑止。

### act で再現
```bash
cp .secrets.translator.sample .secrets.translator
# GEMINI_API_KEY と PAT (WORKFLOWS_GITHUB_TOKEN 相当の権限を持つ GITHUB_TOKEN) を記入
act -j translate --secret-file .secrets.translator \
  --env TRANSLATION_TARGET_SHA=2d83acfe
```
- `act` 実行時は Docker イメージが Java 21 を含むことを確認。
- `--env TRANSLATION_MODE=mock` を追加すると API 消費なしで検証可能。

## 5. 段階的リリース計画
1. **Phase 1** – 単一コミット検証
   - `workflow_dispatch` で `translation_target_sha=2d83acfe` を指定。
   - PR の翻訳内容と差分をレビュー。
2. **Phase 2** – 最古 2 コミット対象
   - CLI もしくは `extra-args` に `--translation-order oldest --translation-target-count 2` を渡せるか確認。
   - 機能が無い場合は `ai-docsite-translator` リポジトリに issue を作成。
3. **Phase 3** – 制限解除
   - `translation_target_sha`／`translation_limit` を未設定で実行。
   - スケジュールトリガーを有効化し、本番運用に移行。

各フェーズ終了後は PR レビューとサイト反映を実施し、残課題をこの runbook に追記する。

## 6. トラブルシューティング
| 症状 | 対応 |
| ---- | ---- |
| ワークフロースキップ | Secrets の `GEMINI_API_KEY` を確認し再実行 |
| 翻訳ブランチ未生成 | `act` またはローカル CLI で `DRY_RUN=true` にしてログを確認 |
| 翻訳品質が低い | `TRANSLATION_MODE=mock` で再現 → upstream 差分を精査し、必要に応じて手動修正 |
| 実行タイムアウト | `translation_limit` を指定して処理量を分割。ログ形式 `json` をもとにボトルネックを特定 |

## 7. 定期メンテナンス
- 四半期ごとに `hide212131/ai-docsite-translator` の `main` ブランチ更新内容を確認し、`runbook` の記述を最新化。
- Secrets の有効期限や不要化した値を棚卸し。
- 未翻訳コミットの滞留状況をチェックし、必要に応じて `translation_limit` を増減。
- 初回運用結果や課題を `.migration/TASKS.md` のフォローアップ項目にフィードバック。

## 8. 参考資料
- `.migration/SPEC.md`
- `.migration/REQUIREMENTS.md`
- `README.md`「翻訳オートメーション」節
- `DEPLOYMENT_GUIDE.md`
