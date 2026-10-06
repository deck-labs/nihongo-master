#!/usr/bin/env bash
# ==============================================================================
# Quick Download & Launch Shortcut for Nihongo Master
# Usage:
#   curl -sSL https://raw.githubusercontent.com/deck-labs/nihongo-master/main/download.sh | bash
# ==============================================================================
set -e

APPIMAGE="Nihongo_Master.AppImage"
URL="https://github.com/deck-labs/nihongo-master/releases/latest/download/${APPIMAGE}"
FALLBACK_URL="https://github.com/deck-labs/nihongo-master/releases/latest/download/Nihongo_Master-x86_64.AppImage"

echo "=== Downloading Nihongo Master ==="
if ! curl -L --progress-bar -f -o "${APPIMAGE}" "${URL}"; then
    echo "Falling back to x86_64 release asset..."
    curl -L --progress-bar -f -o "${APPIMAGE}" "${FALLBACK_URL}"
fi
chmod +x "${APPIMAGE}"

echo "=== Download complete! ==="
echo "AppImage saved to: $(pwd)/${APPIMAGE}"
echo "To run the game anytime: ./${APPIMAGE}"

if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    echo "Launching game..."
    exec ./"${APPIMAGE}" "$@"
fi
