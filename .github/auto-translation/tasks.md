# tasks.md

---

## フェーズ0: 初期セットアップ

### Task 0-1: 開発ブランチ作成 & Poetry 初期化
- **構築内容**
  - `git clone` で `jhipster.github.io-jp` を取得し `spec-impl` ブランチを作成。
  - `poetry init -n && poetry add pytest language-tool-python google-generativeai gitpython`。
- **確認内容**
  - `poetry run pytest -q` がテストゼロで成功する。
  - `poetry lock` がコミットされている。

### Task 0-2: Secrets ダミー設定
- **構築内容**
  - `.env.sample` に `GEMINI_API_KEY=fake` 等を記載。
- **確認内容**
  - `poetry run python -c "import os,sys;assert 'GEMINI_API_KEY' in os.environ"` が 0 終了。

---

## フェーズ1: fetch_upstream.py

### Task 1-1: スクリプト実装
- **構築内容**
  - `scripts/fetch_upstream.py` を作成。
  - 引数 `--hash`（任意）で特定コミット checkout 可。
  - 無指定時は upstream/main 最新を取得し `sync-<hash>` ブランチ作成。
- **確認内容**
  - ダミーリポ上で `py tests/test_fetch_upstream.py` が PASS。
  - ブランチ名が `sync-` で始まり short SHA7 で終わる。

---

## フェーズ2: classify_changes.py

### Task 2-1: 変更判定ロジック
- **構築内容**
  - `git diff --name-status` と `<<<<` スキャンで a/b-1/b-2/c を判定。
  - JSON で `{path, status}` を stdout に出力。
- **確認内容**
  - `pytest` で 4 種 fixture (a,b-1,b-2,c) が正確に分類される。

---

## フェーズ3: style-guide.md

### Task 3-1: スタイルガイド策定
- **構築内容**
  - `docs/style-guide.md` に用語集・常体ルールを記載。
- **確認内容**
  - `grep -q "常体" docs/style-guide.md` が 0 で終了。

---

## フェーズ4: translate_chunk.py

### Task 4-1: Gemini API ラッパー
- **構築内容**
  - `scripts/translate_chunk.py` に Gemini 呼出実装。4096 tokens 超は段落分割。
- **確認内容**
  - `pytest` で mock に置換した呼出が正しい prompt を受ける。
  - 出力行数 == 入力行数 を assert。

---

## フェーズ5: postprocess.py

### Task 5-1: 行数検査 & マーカー除去
- **構築内容**
  - `scripts/postprocess.py` で `<<<<`, `====`, `>>>>` を除去し行数確認。
- **確認内容**
  - 衝突含む入力ファイル → 出力にマーカーなし, 行数一致。

---

## フェーズ6: commit_and_pr.py

### Task 6-1: コミット生成
- **構築内容**
  - `git add` された翻訳ファイルをコミット。メッセージ `docs(sync): ...`。
- **確認内容**
  - `git log -1 --pretty=%s` が正規表現 `^docs\(sync\):` にマッチ。

### Task 6-2: PR 自動作成
- **構築内容**
  - `gh pr create`(dry-run) または `PyGitHub` で PR 作成。
- **確認内容**
  - Dry-run 時に標準出力へ PR URL が表示される。

---

## フェーズ7: GitHub Actions ワークフロー

### Task 7-1: `.github/workflows/sync.yml` 作成
- **構築内容**
  - トリガー cron と `workflow_dispatch`、キャッシュ、Poetry セットアップを記載。
  - ステップ順: checkout → poetry install → run script chain → upload PR summary artefact。
- **確認内容**
  - `act -j sync` でローカル実行し成功ステータス。

---

## フェーズ8: 統合テスト

### Task 8-1: E2E Dry-run
- **構築内容**
  - ローカル fork でフェーズ0~7 スクリプトを通し、 `--dry-run` オプションで実行。
- **確認内容**
  - `tmp/sync-*.log` に `Finished without error` が記録。

### Task 8-2: GitHub Actions 実走
- **構築内容**
  - テストリポで Secrets を設定し `workflow_dispatch` 実行。
- **確認内容**
  - Actions が Success、PR が生成され diff が期待通り。

---

## フェーズ9: ドキュメント整理

### Task 9-1: README 更新
- **構築内容**
  - 使い方、ローカル実行方法、FAQ を README に追記。
- **確認内容**
  - `markdownlint README.md` が警告ゼロ。

### Task 9-2: CHANGELOG 初版
- **構築内容**
  - `CHANGELOG.md` に Semantic Versioning で `0.1.0` リリースノート記載。
- **確認内容**
  - `grep -q "## \[0.1.0\]" CHANGELOG.md` が 0 で終了。

---

## フェーズ10: リリース準備

### Task 10-1: タグ付け & GitHub Release
- **構築内容**
  - `git tag v0.1.0 && git push --tags`。
  - Release ノートに自動翻訳機能概要を記載。
- **確認内容**
  - GitHub Releases ページに `v0.1.0` が存在し、アセット無しで公開。

