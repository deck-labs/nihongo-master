#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "========================================================="
echo "   Building The Gallery Sniper Standalone AppImage        "
echo "========================================================="

# 1. Export Godot project in release mode
echo "=== 1. Exporting Godot Release Project ==="
"$DIR/build_gallery_sniper.sh"

# 2. Assemble AppDir
echo "=== 2. Assembling AppDir ==="
APPDIR="/tmp/Gallery_Sniper.AppDir"
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

# Copy binary and pck
cp "$DIR/build/gallery_sniper.x86_64" "$APPDIR/usr/bin/gallery_sniper"
cp "$DIR/build/gallery_sniper.pck" "$APPDIR/usr/bin/gallery_sniper.pck"
chmod +x "$APPDIR/usr/bin/gallery_sniper"

# Copy Icon
cp "$DIR/icon.png" "$APPDIR/gallery_sniper.png"
cp "$DIR/icon.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/gallery_sniper.png"

# Create Desktop file
cat << 'EOD' > "$APPDIR/gallery_sniper.desktop"
[Desktop Entry]
Name=The Gallery Sniper
Comment=Japanese Hiragana & Katakana Arcade Target Shooter
Exec=gallery_sniper
Icon=gallery_sniper
Terminal=false
Type=Application
Categories=Game;ArcadeGame;Education;
EOD

cp "$APPDIR/gallery_sniper.desktop" "$APPDIR/usr/share/applications/gallery_sniper.desktop"

# Create AppRun
cat << 'EOA' > "$APPDIR/AppRun"
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="${HERE}/usr/bin:${PATH}"
cd "${HERE}/usr/bin"
exec "${HERE}/usr/bin/gallery_sniper" "$@"
EOA

chmod +x "$APPDIR/AppRun"

# 3. Package with appimagetool
echo "=== 3. Packaging Standalone AppImage ==="
TOOL="/home/deck/.local/bin/appimagetool"
if [ ! -x "$TOOL" ]; then
    TOOL="appimagetool"
fi

OUT_FILE="/home/deck/Downloads/Gallery_Sniper-x86_64.AppImage"
rm -f "$OUT_FILE"

echo "Running $TOOL on $APPDIR -> $OUT_FILE..."
ARCH=x86_64 "$TOOL" --no-appstream "$APPDIR" "$OUT_FILE"
chmod +x "$OUT_FILE"

echo "========================================================="
echo " AppImage successfully generated at:                      "
echo "   $OUT_FILE                                             "
echo " Size: $(du -h "$OUT_FILE" | cut -f1)                    "
echo "========================================================="
