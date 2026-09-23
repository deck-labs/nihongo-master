#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=== Building Godot Hiragana Cards ==="
mkdir -p "$DIR/build"

# 1. Export pack
godot --headless --path "$DIR" --export-pack "Linux" "$DIR/build/hiragana_cards.pck"

# 2. Copy Godot binary as matching launcher
cp "/home/deck/Applications/godot/Godot_v4.7.2-stable_linux.x86_64" "$DIR/build/hiragana_cards.x86_64"
chmod +x "$DIR/build/hiragana_cards.x86_64"

echo "=== Godot Build Complete: build/hiragana_cards.x86_64 ($(du -h "$DIR/build/hiragana_cards.pck" | cut -f1)) ==="
