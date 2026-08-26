#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
# macOS may re-mark .pth as hidden after copy/sync; clear before each run
chflags -R nohidden "$ROOT/.venv/lib/python3.12/site-packages" 2>/dev/null || true
exec "$ROOT/.venv/bin/da-cli" "$@"
