# ai-docsite-translator 移行 SPEC

## ゴール
- `.github/auto-translation` 配下の既存 Python ベース自動翻訳パイプラインを全廃し、[ai-docsite-translator](https://github.com/hide212131/ai-docsite-translator) を唯一の翻訳エンジンとして採用する。
- GitHub Actions 本番環境とローカル (開発者マシン + `act`) の双方で同一フローを再現できるようにする。
- upstream (`jhipster/jhipster.github.io`) の更新を origin (`hide212131/jhipster.github.io-jp`) に対して安定的かつ段階的に取り込める運用を定義する。

## スコープ / 非スコープ
- スコープ: ワークフロー設計、Secrets/環境変数の整理、ローカル検証手順、初回リリース時の段階的翻訳オペレーション。
- 非スコープ: 翻訳結果の内容レビュー、`ai-docsite-translator` 自体の機能追加や改修、翻訳対象ディレクトリ (`docs`) 以外の運用整備。

## アーキテクチャ概要
- **CI**: `ubuntu-latest` 上で `actions/checkout@v4` → `hide212131/ai-docsite-translator@main` を実行する GitHub Actions ワークフローを新設する。
- **ローカル検証**: `act` でワークフローを再現 / `tools/run-ai-docsite-translator.sh` (新規) で CLI を直接起動する 2 系統を用意する。
- **構成管理**: `.github/auto-translation/**` を完全削除し、翻訳関連ドキュメントは `.migration/` と `.github/llm-translation/docs/` に整理する。
- **Secrets**: 本番は GitHub Secrets (`GEMINI_API_KEY`, `WORKFLOWS_GITHUB_TOKEN`) を使用し、ローカルは `.env.translator` (未コミット) で補完する。

## 想定ディレクトリ / ファイル構成
| 種別 | パス | 内容 |
| --- | --- | --- |
| **新規** | `.github/workflows/ai-docsite-translation.yml` | ai-docsite-translator を呼び出すメインワークフロー |
| **新規** | `.github/llm-translation/docs/runbook.md` | 運用手順 (段階的翻訳の進め方) |
| **新規** | `tools/run-ai-docsite-translator.sh` | ローカル用ラッパースクリプト (Java 21 + `.env.translator` 読み込み) |
| **新規** | `.env.translator.sample` | ローカル用環境変数テンプレート (Git 管理) |
| **更新** | `.gitignore` | `.env.translator` を除外 |
| **削除** | `.github/auto-translation/**` | 旧 Python 実装一式 |
| **ドキュメント** | `.migration/SPEC.md` (本書) | 設計指針 |

## GitHub Actions ワークフロー設計
- **トリガー**
  - `schedule`: `cron: "30 3 * * *"` (JST 12:30 実行目安)
  - `workflow_dispatch`
- **ジョブ構成**
  - `translate` ジョブ 1 本。`concurrency: { group: ai-docsite-translation, cancel-in-progress: false }` で重複実行を防止。
  - `permissions`: `contents: write`, `pull-requests: write`。
- **ステップ**
  1. 実行ガード: Secrets 不足 (`GEMINI_API_KEY` 未設定) 時は `SHOULD_SKIP=true` をセットし早期終了。
  2. Checkout (`actions/checkout@v4`, `fetch-depth: 0`, `token: ${{ secrets.WORKFLOWS_GITHUB_TOKEN }}`) — PAT を用いて push/PR 権限を確保。
  3. `uses: actions/setup-java@v4` (Temurin 21) — composite Action 側でも実施されるが、キャッシュ利用とローカル `act` 対応のため事前実行する。
  4. **翻訳実行**: `uses: hide212131/ai-docsite-translator@main`
     - `with`
       - `upstream-url`: `https://github.com/jhipster/jhipster.github.io.git`
       - `origin-url`: `${{ github.server_url }}/${{ github.repository }}.git`
       - `origin-branch`: `main`
       - `translation-branch-template`: `sync-<upstream-short-sha>`
       - `mode`: `batch`
       - `translation-mode`: `production`
       - `log-format`: `json`
     - `env`
       - `LLM_PROVIDER=gemini`
       - `LLM_MODEL=gemini-2.5-flash`
       - `TRANSLATION_INCLUDE_PATHS=docs`
       - `TRANSLATION_DOCUMENT_EXTENSIONS=md,mdx,txt,html`
       - `GEMINI_API_KEY=${{ secrets.GEMINI_API_KEY }}`
       - `GITHUB_TOKEN=${{ secrets.WORKFLOWS_GITHUB_TOKEN }}`
       - `DRY_RUN=false`
       - `MAX_FILES_PER_RUN=0`
- **初回段階的オペレーション**
  - 手動実行 (`workflow_dispatch`) で `env.TRANSLATION_TARGET_SHA=2d83acfe` を設定して 1 コミットのみ翻訳。
  - 次フェーズ: `extra-args: "--translation-target-count 2 --translation-order oldest"` (機能存在確認後に採用) もしくは `TRANSLATION_TARGET_MODE=oldest-two` 環境変数 (未実装なら CLI 側へ issue)。
  - 最終フェーズ: 変数を外し、未翻訳全件に拡張。

## ローカル / `act` 運用
- **`act`**
  - `act -j translate --secret-file .secrets.translator` で実行。
  - `.secrets.translator` は `GITHUB_TOKEN`, `GEMINI_API_KEY` を含む。
  - 初回検証では `ACT_ENV_TRANSPORT` を利用して `TRANSLATION_TARGET_SHA` を注入。
- **直接 CLI 実行**
  - `tools/run-ai-docsite-translator.sh`
    - `.env.translator` を読み込み (`LLM_PROVIDER`, `LLM_MODEL`, `GEMINI_API_KEY`, `GITHUB_TOKEN` 等)。
    - キャッシュディレクトリ (`.tools/cache/ai-docsite-translator`) に必要ならリポジトリを clone、`./gradlew :app:run` を呼び出す。
    - 引数例:
      ```bash
      MODE=dev DRY_RUN=true TRANSLATION_MODE=mock \
        TRANSLATION_TARGET_SHA=2d83acfe \
        ./tools/run-ai-docsite-translator.sh
      ```

## 環境変数 / Secrets 設計
| キー | デフォルト | 用途 / 備考 |
| --- | --- | --- |
| `LLM_PROVIDER` | `gemini` | LLM プロバイダー選択 |
| `LLM_MODEL` | `gemini-2.5-flash` | 使用モデル |
| `UPSTREAM_URL` | 固定 | ワークフロー/ラッパー内でセット |
| `ORIGIN_URL` | 固定 | 同上 |
| `ORIGIN_BRANCH` | `main` | 翻訳先ブランチ |
| `TRANSLATION_BRANCH_TEMPLATE` | `sync-<upstream-short-sha>` | 生成ブランチ命名規則 |
| `MODE` | `batch` (CI), `dev` (ローカル) | 実行モード |
| `TRANSLATION_MODE` | `production` (CI), `mock`/`dry-run` (ローカル検証) | 翻訳挙動 |
| `DRY_RUN` | `false` (CI) | ローカル検証では `true` |
| `MAX_FILES_PER_RUN` | `0` | 0 は無制限 |
| `TRANSLATION_INCLUDE_PATHS` | `docs` | 翻訳対象パス |
| `TRANSLATION_DOCUMENT_EXTENSIONS` | `md,mdx,txt,html` | 翻訳対象拡張子 |
| `TRANSLATION_TARGET_SHA` | 任意 | 特定コミットのみ翻訳する際に設定 |
| `GEMINI_API_KEY` | Secrets 必須 | LLM 認証 |
| `WORKFLOWS_GITHUB_TOKEN` | Secrets 必須 | PAT。Checkout と翻訳アクションから `GITHUB_TOKEN` として使用 |

## 実装タスク
1. `.github/auto-translation` ディレクトリと関連ドキュメントを削除。
2. `.gitignore` へ `.env.translator` / `.tools/cache/` を追加。
3. `.env.translator.sample` と `tools/run-ai-docsite-translator.sh` を追加。
4. `ai-docsite-translation.yml` ワークフローを新設し、`hide212131/ai-docsite-translator@main` を採用。
5. `.github/llm-translation/docs/runbook.md` (新規) で運用/トラブルシュートを記載。
6. `README.md` / `DEPLOYMENT_GUIDE.md` 等に新運用概要を追記。
7. `act` 用シークレットテンプレート (`.secrets.translator.sample`) を提供。
8. 初回ワークフロー実行ログを確認し、残タスク (2nd/3rd フェーズ) を runbook に反映。

## 検証計画
1. **ローカル CLI**: `.env.translator` に `DRY_RUN=true`, `TRANSLATION_MODE=mock`, `TRANSLATION_TARGET_SHA=2d83acfe` を設定し `tools/run-ai-docsite-translator.sh` を実行。Git 操作なしで差分とログを確認。
2. **`act`**: `act -j translate --secret-file .secrets.translator --env TRANSLATION_TARGET_SHA=2d83acfe` を実行し、GitHub Actions と同じ挙動を検証。
3. **本番ワークフロー (Phase 1)**: `workflow_dispatch` で `TRANSLATION_TARGET_SHA=2d83acfe` を設定し実行。作成された PR 内容をレビュー。
4. **本番ワークフロー (Phase 2)**: 未翻訳コミットのうち最も古い 2 件を対象に手動実行 (CLI で `--limit 2` 等を利用)。
5. **本番ワークフロー (Phase 3)**: 制限を解除し、通常スケジュール (`cron`) に移行。初回成功後に `TRANSLATION_TARGET_SHA` 関連設定を runbook から削除。

## リスクと緩和策
- **AI モデルのレスポンス遅延**: Gradle 実行が 30+ 分化する可能性 → `timeout-minutes` を 90 に設定し、ログフォーマット `json` を選択して監視しやすくする。
- **Secrets 誤設定**: `act` での dry-run を義務化し、ワークフローに `if: env.GEMINI_API_KEY != ''` ガードを追加。
- **Action バージョン追従**: `@main` を追従するため、四半期ごとに上流の BREAKING CHANGE 有無を確認し、必要ならワークフロー調整。
- **大量差分による PR 氾濫**: `MAX_FILES_PER_RUN` / `--limit` オプションで分割、runbook に対応手順を記す。

## 未確定事項 / ToDo
- `ai-docsite-translator` における「最も古い 2 つの未翻訳コミット」指定手段が CLI で提供されているか確認し、無い場合は issue を作成する。
- Bot 用の Git ユーザー情報 (表示名/メールアドレス) を確定し GitHub Secrets に登録。
- `GEMINI_API_KEY` が無い環境 (例: pull request from fork) でのフェールセーフ動作 (`if` で skip するか) を検討。
