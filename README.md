# Nihongo Master (日本語 マスター)

[![Language](https://img.shields.io/badge/Language-Python%203.13-blue.svg)](https://www.python.org/)
[![Engine](https://img.shields.io/badge/Engine-Pygame%202.6%20%2F%20Godot%204.7-yellow.svg)](https://godotengine.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%2F%20SteamOS%20(Steam%20Deck)-orange.svg)](https://store.steampowered.com/steamdeck)
[![Version](https://img.shields.io/badge/Release-v1.5.4-blueviolet.svg)](https://github.com/deck-labs/nihongo-master/releases/tag/v1.5.4)
[![Characters](https://img.shields.io/badge/Characters-142%20Total%20Kana%20(71%20Hiragana%20%2B%2071%20Katakana)-brightgreen.svg)](#-syllabus--stage-overview)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Download AppImage](https://img.shields.io/badge/Download-Nihongo__Master.AppImage-00C853?style=flat&logo=appimage&logoColor=white)](https://github.com/deck-labs/nihongo-master/releases/download/v1.5.4/Nihongo_Master.AppImage)

The definitive retro Japanese arcade learning suite bundling three distinct game modes for both **Hiragana** and **Katakana** into a single cohesive experience for Steam Deck and Linux.

<div align="center">

<a href="https://github.com/deck-labs/nihongo-master/releases/download/v1.5.4/Nihongo_Master.AppImage">
  <img src="https://img.shields.io/badge/⬇%20DOWNLOAD%20APPIMAGE-Nihongo__Master.AppImage%20(v1.5.4)-00C853?style=for-the-badge&logo=appimage&logoColor=white" height="46" alt="Download AppImage">
</a>

<br>
<sub><b>Standalone Linux Binary:</b> Zero dependencies or installation required. Runs directly on Steam Deck and Linux desktops!</sub>

</div>

---

## ✨ 3 Games in 1 Bundle

1. **🏎️ Retro Arcade Racers (Hiragana & Katakana Fighter)**:
   - High-speed retro highway racer built with Pygame & SDL2.
   - 10 distinct campaign stages + secret **Rainbow Skyway** (Stage 11) 71-Kana Gauntlet.
   - Slipstream drafting (`DRAFT BOOST`), near-miss bonuses, oil slick hazards, rival traffic archetypes, and authentic tire smoke & turbo flame particles.
   - Cruise at 176 KM/H and overdrive turbo boost up to 264 KM/H!

2. **🃏 3D Cards Table (Godot 4 3D)**:
   - Tactile 3D Japanese flashcard game with wooden tatami table aesthetics.
   - 8 progressive stages per Kana mode with authentic vocabulary words and English translations.
   - Interactive card-flipping physics, smooth analog stick navigation, and score combo streaks.

3. **🎯 The Gallery Sniper (射的ギャラリー - Godot 4 2D)**:
   - Festive Japanese festival shooting gallery with 8 progressive difficulty stages.
   - Dynamic target motion physics scaling with each stage: stationary targets, harmonic bobbing, lateral swaying, shelf patrol bouncing, and high-speed sinusoidal wave gauntlet.
   - Analog joystick and mouse crosshair targeting with realistic recoil impulse physics.
   - Distractor decoy targets (scaling from 3 to 7) and English vocabulary meanings (`“ apple ”`).
   - Dedicated in-game Pause Menu and Stage Clear celebration modal with marksman accuracy tracking.

4. **⚙️ Unified Architecture & Quality of Life**:
   - Symmetrical 6-card Main Menu carousel for instantaneous switching between all 6 subgames.
   - Independent Master, Engine, and SFX volume sliders.
   - 16:10 native aspect ratio standard optimized for Steam Deck (1280x800 / 1920x1200).
   - In-game background updater with live download progress and atomic binary replacement.

---

## 📦 Download & Installation

### 🚀 One-Line Terminal Shortcut (Steam Deck & Linux)
```bash
curl -sSL https://raw.githubusercontent.com/deck-labs/nihongo-master/main/download.sh | bash
```

### 📥 Manual Download
```bash
curl -L -o Nihongo_Master.AppImage https://github.com/deck-labs/nihongo-master/releases/download/v1.5.4/Nihongo_Master.AppImage
chmod +x Nihongo_Master.AppImage
./Nihongo_Master.AppImage
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
