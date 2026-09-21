# Nihongo Master (日本語 マスター)

[![Language](https://img.shields.io/badge/Language-Python%203.13-blue.svg)](https://www.python.org/)
[![Engine](https://img.shields.io/badge/Engine-Pygame%202.6%20%2F%20SDL2-yellow.svg)](https://www.pygame.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%2F%20SteamOS%20(Steam%20Deck)-orange.svg)](https://store.steampowered.com/steamdeck)
[![Characters](https://img.shields.io/badge/Characters-142%20Total%20Kana%20(71%20Hiragana%20%2B%2071%20Katakana)-brightgreen.svg)](#-syllabus--stage-overview)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Download AppImage](https://img.shields.io/badge/Download-Latest%20AppImage-00C853?style=flat&logo=appimage&logoColor=white)](https://github.com/deck-labs/nihongo-master/releases/download/v1.0.0/Nihongo_Master-x86_64.AppImage)

The definitive retro Japanese arcade learning experience merging **Hiragana Master** and **Katakana Master** into a single unified high-speed racer. Choose between Hiragana and Katakana right from the home screen, fine-tune audio and display options, and master Japanese reading at speeds up to 264 KM/H!

<div align="center">

<a href="https://github.com/deck-labs/nihongo-master/releases/download/v1.0.0/Nihongo_Master-x86_64.AppImage">
  <img src="https://img.shields.io/badge/⬇%20DOWNLOAD%20APPIMAGE-v1.0.0%20(Linux%20%2F%20Steam%20Deck)-00C853?style=for-the-badge&logo=appimage&logoColor=white" height="46" alt="Download AppImage">
</a>

<br>
<sub><b>Standalone Linux Binary:</b> Zero dependencies or installation required. Runs directly on Steam Deck and Linux desktops!</sub>

</div>

---

## ✨ Key Features

1. **Unified 2-in-1 Arcade Learning**:
   - Seamlessly switch between **Hiragana Master** and **Katakana Master** on the home screen.
   - Separate progress tracking and unlocks for both syllabaries (with auto-import from legacy save files!).
2. **Complete 142-Character Japanese Kana Syllabus**:
   - **71 Hiragana**: 46 Core + 20 Voiced Dakuten (゛) + 5 Semi-Voiced Handakuten (゜).
   - **71 Katakana**: 46 Core + 20 Voiced Dakuten (゛) + 5 Semi-Voiced Handakuten (゜).
3. **10 Distinct Stages + Secret Rainbow Skyway (Stage 11)**:
   - Race through 36,000-meter courses from Cedar Forests to Tokyo Neon Metropolises and Mount Fuji.
   - Conquer Stage 10 without damage to unlock the secret **Rainbow Skyway** 71-Kana Gauntlet!
4. **Enhanced Vehicle Scale & Readability (+15% Scale)**:
   - Orthographic 3D race cars with high-visibility 30pt Japanese font rendering on illuminated roof decal plates.
   - Dual-exhaust turbo flames, dynamic suspension wobble, and authentic vehicle ground contact shadows.
5. **Overdrive Speed Tuning (+10% Boost)**:
   - High-speed thrills: 176 KM/H cruise speed and 264 KM/H turbo overdrive with agile steering responsiveness.
6. **In-Game Audio & Display Options**:
   - Independent Master, Engine, and SFX volume sliders (comfortably initialized to 30% default).
   - Display aspect ratio controls: Auto 16:10 Native (Steam Deck / Widescreen) or Full Stretch.
7. **Seamless In-Game Auto-Updater**:
   - Background GitHub updater checking for new versions directly from the title screen with live download progress and hot-swappable atomic binary replacement.

---

## 📦 Download & Installation

### 🚀 One-Line Terminal Shortcut (Steam Deck & Linux)
```bash
curl -sSL https://raw.githubusercontent.com/deck-labs/nihongo-master/main/download.sh | bash
```

### 📥 Manual Download
```bash
curl -L -o Nihongo_Master-x86_64.AppImage https://github.com/deck-labs/nihongo-master/releases/download/v1.0.0/Nihongo_Master-x86_64.AppImage
chmod +x Nihongo_Master-x86_64.AppImage
./Nihongo_Master-x86_64.AppImage
```

---

## 🏎️ Syllabus & Stage Overview

| Stage | Course Name | Hiragana Mode | Katakana Mode | Sounds / Notes |
| :---: | :--- | :---: | :---: | :--- |
| **01** | **Forest Highway** | `あ` `い` `う` `え` `お` | `ア` `イ` `ウ` `エ` `オ` | `a`, `i`, `u`, `e`, `o` |
| **02** | **Coastal Bridge** | `か`–`こ` + `が`–`ご` | `カ`–`コ` + `ガ`–`ゴ` | `ka`–`ko` + `ga`–`go` (Dakuten) |
| **03** | **Coastal Beach** | `さ`–`そ` + `ざ`–`ぞ` | `サ`–`ソ` + `ザ`–`ゾ` | `sa`–`so` + `za`–`zo` (Dakuten) |
| **04** | **Mountain Pass** | `た`–`と` + `だ`–`ど` | `タ`–`ト` + `ダ`–`ド` | `ta`–`to` + `da`–`do` (Dakuten) |
| **05** | **Neon Metropolis** | `な` `に` `ぬ` `ね` `の` | `ナ` `ニ` `ヌ` `ネ` `ノ` | `na`, `ni`, `nu`, `ne`, `no` |
| **06** | **Volcano Caldera** | `は`–`ほ` + `ば`–`ぼ` + `ぱ`–`ぽ` | `ハ`–`ホ` + `バ`–`ボ` + `パ`–`ポ` | `ha`–`ho` + `ba`–`bo` + `pa`–`po` |
| **07** | **Glacier Tundra** | `ま` `み` `む` `め` `も` | `マ` `ミ` `ム` `メ` `モ` | `ma`, `mi`, `mu`, `me`, `mo` |
| **08** | **Sakura Boulevard** | `ら` `り` `る` `れ` `ろ` | `ラ` `リ` `ル` `レ` `ロ` | `ra`, `ri`, `ru`, `re`, `ro` |
| **09** | **Sunset Canyon** | `や` `ゆ` `よ` `わ` `を` | `ヤ` `ユ` `ヨ` `ワ` `ヲ` | `ya`, `yu`, `yo`, `wa`, `wo` |
| **10** | **Fuji Speedway** | Grand Mixed Review | Grand Mixed Review | Championship Apex |
| **11** | **Rainbow Skyway** | **All 71 Hiragana** | **All 71 Katakana** | ★ Secret Gauntlet (Flawless Clear) ★ |

---

## 🎮 Controls

| Action | Keyboard | Gamepad (Steam Deck / Xbox) |
| :--- | :--- | :--- |
| **Steer Left / Right** | `A` / `D` or `Left` / `Right` | Left Stick / D-Pad |
| **Throttle / Turbo** | `W` / `Up` / `Space` / `Shift` | `A` Button / `RT` / `RB` |
| **Brake** | `S` / `Down` | `B` Button / `LT` |
| **Options / Pause** | `Esc` | `Start` / `Menu` |
| **Menu Select** | `Enter` / `Space` | `A` Button |
| **Quit Game** | `Ctrl + Q` / Title Menu | `Select + Start` (Simultaneous) |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
