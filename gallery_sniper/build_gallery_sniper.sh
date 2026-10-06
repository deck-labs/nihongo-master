#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=== Building Godot The Gallery Sniper ==="
mkdir -p "$DIR/build"

GODOT_BIN="/home/deck/Applications/godot/Godot_v4.7.2-stable_linux.x86_64"
if ! command -v godot &> /dev/null; then
    if [ -x "$GODOT_BIN" ]; then
        GODOT_CMD="$GODOT_BIN"
    else
        echo "Error: Godot executable not found."
        exit 1
    fi
else
    GODOT_CMD="godot"
fi

# 1. Export pack
"$GODOT_CMD" --headless --path "$DIR" --export-pack "Linux" "$DIR/build/gallery_sniper.pck"

# 2. Copy Godot binary as matching launcher
cp "$GODOT_BIN" "$DIR/build/gallery_sniper.x86_64"
chmod +x "$DIR/build/gallery_sniper.x86_64"

echo "=== Godot Build Complete: build/gallery_sniper.x86_64 ($(du -h "$DIR/build/gallery_sniper.pck" | cut -f1)) ==="
