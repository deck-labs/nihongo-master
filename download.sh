#!/usr/bin/env bash
# ==============================================================================
# Quick Download & Launch Shortcut for Nihongo Master
# Usage:
#   curl -sSL https://raw.githubusercontent.com/deck-labs/nihongo-master/main/download.sh | bash
# ==============================================================================
set -e

VERSION="1.5.0"
APPIMAGE="Nihongo_Master-v${VERSION}-x86_64.AppImage"
URL="https://github.com/deck-labs/nihongo-master/releases/download/v${VERSION}/${APPIMAGE}"
FALLBACK_URL="https://github.com/deck-labs/nihongo-master/releases/latest/download/${APPIMAGE}"
LEGACY_URL="https://github.com/deck-labs/nihongo-master/releases/latest/download/Nihongo_Master-x86_64.AppImage"

echo "=== Downloading Nihongo Master (v${VERSION}) ==="
if ! curl -L --progress-bar -f -o "${APPIMAGE}" "${URL}"; then
    echo "Falling back to latest release asset..."
    if ! curl -L --progress-bar -f -o "${APPIMAGE}" "${FALLBACK_URL}"; then
        echo "Falling back to legacy asset..."
        curl -L --progress-bar -f -o "${APPIMAGE}" "${LEGACY_URL}"
    fi
fi
chmod +x "${APPIMAGE}"

echo "=== Download complete! ==="
echo "AppImage saved to: $(pwd)/${APPIMAGE}"
echo "To run the game anytime: ./${APPIMAGE}"

if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    echo "Launching game..."
    exec ./"${APPIMAGE}" "$@"
fi
