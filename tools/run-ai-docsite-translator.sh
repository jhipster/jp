#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CACHE_DIR="${REPO_ROOT}/.tools/cache"
TRANSLATOR_DIR="${CACHE_DIR}/ai-docsite-translator"
TRANSLATOR_REPO="https://github.com/hide212131/ai-docsite-translator.git"
TRANSLATOR_COMMIT="7cb3090ba0fac3a0c465be39117a422ee3afa5a3"

mkdir -p "${CACHE_DIR}"

ENV_FILE="${REPO_ROOT}/.env.translator"
if [[ -f "${ENV_FILE}" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
  set +a
fi

export UPSTREAM_URL="${UPSTREAM_URL:-https://github.com/jhipster/jhipster.github.io.git}"
export ORIGIN_URL="${ORIGIN_URL:-https://github.com/hide212131/jhipster.github.io-jp.git}"
export ORIGIN_BRANCH="${ORIGIN_BRANCH:-main}"
export TRANSLATION_BRANCH_TEMPLATE="${TRANSLATION_BRANCH_TEMPLATE:-sync-<upstream-short-sha>}"
export TRANSLATION_INCLUDE_PATHS="${TRANSLATION_INCLUDE_PATHS:-docs}"
export TRANSLATION_DOCUMENT_EXTENSIONS="${TRANSLATION_DOCUMENT_EXTENSIONS:-md,mdx,txt,html}"
export LLM_PROVIDER="${LLM_PROVIDER:-gemini}"
export LLM_MODEL="${LLM_MODEL:-gemini-2.5-flash}"
export MODE="${MODE:-dev}"
export TRANSLATION_MODE="${TRANSLATION_MODE:-mock}"
export DRY_RUN="${DRY_RUN:-true}"
export LOG_FORMAT="${LOG_FORMAT:-text}"

if [[ ! -d "${TRANSLATOR_DIR}/.git" ]]; then
  git clone "${TRANSLATOR_REPO}" "${TRANSLATOR_DIR}"
fi

pushd "${TRANSLATOR_DIR}" >/dev/null
trap 'popd >/dev/null' EXIT

git fetch origin --tags --quiet
if ! git rev-parse --verify "${TRANSLATOR_COMMIT}^{commit}" >/dev/null 2>&1; then
  git fetch origin "${TRANSLATOR_COMMIT}"
fi
git checkout --quiet "${TRANSLATOR_COMMIT}"

gradle_cmd=("${TRANSLATOR_DIR}/gradlew" ":app:run")

if [[ $# -gt 0 ]]; then
  args=$(printf '%q ' "$@")
  args=${args% }
  gradle_cmd+=("--args=${args}")
fi

"${gradle_cmd[@]}"
