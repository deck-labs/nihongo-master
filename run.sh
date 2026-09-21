#!/usr/bin/env bash
# ==============================================================================
# Launch Nihongo Master (Python Edition)
# ==============================================================================
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

PYTHON_BIN="/home/deck/Applications/nihongo smith/.venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

exec "$PYTHON_BIN" "$DIR/python/main.py" "$@"
