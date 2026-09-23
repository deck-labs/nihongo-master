"""
game_config.py
Game configurations, stage telemetry, Kana pools (Hiragana & Katakana),
and path resolution for Nihongo Master.
"""

import os
import sys

# Virtual Canvas & Display Defaults (Permanent 16:10 Standard)
VIRTUAL_WIDTH = 1920
VIRTUAL_HEIGHT = 1200
SCREEN_WIDTH = VIRTUAL_WIDTH
SCREEN_HEIGHT = VIRTUAL_HEIGHT
TARGET_FPS = 60

# Road & Arcade Viewport Geometry (16:10 1200p Cockpit)
GAME_X = 280.0
GAME_W = 960.0
ROAD_MARGIN = 160.0
ROAD_WIDTH = GAME_W - (ROAD_MARGIN * 2.0)  # 640.0 px wide 4-lane highway
PLAYER_SCREEN_Y = 960.0  # 1200 - 240.0

# Version & Release Metadata
GAME_VERSION = "1.1.0"
GITHUB_REPO = "deck-labs/nihongo-master"
VERSION_CHECK_URL = "https://raw.githubusercontent.com/deck-labs/nihongo-master/main/version.json"
RELEASES_API_URL = "https://api.github.com/repos/deck-labs/nihongo-master/releases/latest"

# Gameplay Settings (+10% Overdrive Tuning)
STAGE_TRACK_LENGTH = 36000.0
GAME_SPEED_SCALE = 0.5
BASE_SPEED = 88.0
TURBO_SPEED = 264.0
SPEED_ACCEL = 132.0
SPEED_DECEL = 80.0
BRAKE_DECEL = 220.0
STEER_SPEED = 462.0
MAX_FUEL = 100.0
FUEL_REWARD = 30.0
FUEL_PENALTY = 15.0
SCORE_REWARD = 50.0

# Total Stages & Secret Stage
TOTAL_STAGES = 10
TOTAL_CAMPAIGN_STAGES = 10
SECRET_STAGE = 11

STAGE_NAMES = {
    1: "FOREST HIGHWAY",
    2: "COASTAL BRIDGE",
    3: "COASTAL BEACH",
    4: "MOUNTAIN PASS",
    5: "NEON METROPOLIS",
    6: "VOLCANO CALDERA",
    7: "GLACIER TUNDRA",
    8: "SAKURA BOULEVARD",
    9: "SUNSET CANYON",
    10: "FUJI SPEEDWAY",
    11: "RAINBOW SKYWAY"
}

STAGE_ENV_NOTES = {
    1: "BROAD HIGHWAY // EXPANSIVE STRAIGHTAWAYS // DENSE CEDAR",
    2: "COASTAL OCEAN BRIDGE // STEEL SPANS // NARROW PASSES",
    3: "TROPICAL BEACH SHORELINE // CONTINUOUS SWEEPS",
    4: "MOUNTAIN PASS // ROCKY GORGE // TIGHT S-CURVES",
    5: "NEON EXPRESSWAY // HIGH-SPEED SWEEPS // SKYSCRAPERS",
    6: "VOLCANIC OBSIDIAN RIDGE // MAGMA CRAGS // FAST APEXES",
    7: "FROST GLACIER // POLAR ICEFALL // ICY APEXES",
    8: "CHERRY BLOSSOM BOULEVARD // SPRING DRIFT // SAKURA PETALS",
    9: "RED ROCK CANYON // DUSK MESAS // HIGH-SPEED GORGE SWEEPS",
    10: "FUJI SPEEDWAY // GRAND CHAMPIONSHIP // GOLDEN APEX",
    11: "SECRET BONUS STAGE // ALL 71 KANA & DAKUTEN GAUNTLET // COSMIC AURORA"
}

# ==============================================================================
# HIRAGANA SYLLABARY DEFINITIONS (46 Core + 20 Dakuten + 5 Handakuten = 71 Total)
# ==============================================================================
ALL_46_HIRAGANA = [
    # A-line
    {"kana": "あ", "romaji": "a"},
    {"kana": "い", "romaji": "i"},
    {"kana": "う", "romaji": "u"},
    {"kana": "え", "romaji": "e"},
    {"kana": "お", "romaji": "o"},
    # Ka-line
    {"kana": "か", "romaji": "ka"},
    {"kana": "き", "romaji": "ki"},
    {"kana": "く", "romaji": "ku"},
    {"kana": "け", "romaji": "ke"},
    {"kana": "こ", "romaji": "ko"},
    # Sa-line
    {"kana": "さ", "romaji": "sa"},
    {"kana": "し", "romaji": "shi"},
    {"kana": "す", "romaji": "su"},
    {"kana": "せ", "romaji": "se"},
    {"kana": "そ", "romaji": "so"},
    # Ta-line
    {"kana": "た", "romaji": "ta"},
    {"kana": "ち", "romaji": "chi"},
    {"kana": "つ", "romaji": "tsu"},
    {"kana": "て", "romaji": "te"},
    {"kana": "と", "romaji": "to"},
    # Na-line
    {"kana": "な", "romaji": "na"},
    {"kana": "に", "romaji": "ni"},
    {"kana": "ぬ", "romaji": "nu"},
    {"kana": "ね", "romaji": "ne"},
    {"kana": "の", "romaji": "no"},
    # Ha-line
    {"kana": "は", "romaji": "ha"},
    {"kana": "ひ", "romaji": "hi"},
    {"kana": "ふ", "romaji": "fu"},
    {"kana": "へ", "romaji": "he"},
    {"kana": "ほ", "romaji": "ho"},
    # Ma-line
    {"kana": "ま", "romaji": "ma"},
    {"kana": "み", "romaji": "mi"},
    {"kana": "む", "romaji": "mu"},
    {"kana": "め", "romaji": "me"},
    {"kana": "も", "romaji": "mo"},
    # Ya-line
    {"kana": "や", "romaji": "ya"},
    {"kana": "ゆ", "romaji": "yu"},
    {"kana": "よ", "romaji": "yo"},
    # Ra-line
    {"kana": "ら", "romaji": "ra"},
    {"kana": "り", "romaji": "ri"},
    {"kana": "る", "romaji": "ru"},
    {"kana": "れ", "romaji": "re"},
    {"kana": "ろ", "romaji": "ro"},
    # Wa-line & N
    {"kana": "わ", "romaji": "wa"},
    {"kana": "を", "romaji": "wo"},
    {"kana": "ん", "romaji": "n"}
]

DAKUTEN_HIRAGANA = [
    # G-line (Ka + Ten-Ten)
    {"kana": "が", "romaji": "ga"},
    {"kana": "ぎ", "romaji": "gi"},
    {"kana": "ぐ", "romaji": "gu"},
    {"kana": "げ", "romaji": "ge"},
    {"kana": "ご", "romaji": "go"},
    # Z-line (Sa + Ten-Ten)
    {"kana": "ざ", "romaji": "za"},
    {"kana": "じ", "romaji": "ji"},
    {"kana": "ず", "romaji": "zu"},
    {"kana": "ぜ", "romaji": "ze"},
    {"kana": "ぞ", "romaji": "zo"},
    # D-line (Ta + Ten-Ten)
    {"kana": "だ", "romaji": "da"},
    {"kana": "ぢ", "romaji": "di"},
    {"kana": "づ", "romaji": "du"},
    {"kana": "で", "romaji": "de"},
    {"kana": "ど", "romaji": "do"},
    # B-line (Ha + Ten-Ten)
    {"kana": "ば", "romaji": "ba"},
    {"kana": "び", "romaji": "bi"},
    {"kana": "ぶ", "romaji": "bu"},
    {"kana": "べ", "romaji": "be"},
    {"kana": "ぼ", "romaji": "bo"},
]

HANDAKUTEN_HIRAGANA = [
    # P-line (Ha + Maru)
    {"kana": "ぱ", "romaji": "pa"},
    {"kana": "ぴ", "romaji": "pi"},
    {"kana": "ぷ", "romaji": "pu"},
    {"kana": "ぺ", "romaji": "pe"},
    {"kana": "ぽ", "romaji": "po"},
]

ALL_71_HIRAGANA = ALL_46_HIRAGANA + DAKUTEN_HIRAGANA + HANDAKUTEN_HIRAGANA

HIRAGANA_STAGE_KANA = {
    1: [
        {"kana": "あ", "romaji": "a"},
        {"kana": "い", "romaji": "i"},
        {"kana": "う", "romaji": "u"},
        {"kana": "え", "romaji": "e"},
        {"kana": "お", "romaji": "o"}
    ],
    2: [
        {"kana": "か", "romaji": "ka"},
        {"kana": "き", "romaji": "ki"},
        {"kana": "く", "romaji": "ku"},
        {"kana": "け", "romaji": "ke"},
        {"kana": "こ", "romaji": "ko"},
        {"kana": "が", "romaji": "ga"},
        {"kana": "ぎ", "romaji": "gi"},
        {"kana": "ぐ", "romaji": "gu"},
        {"kana": "げ", "romaji": "ge"},
        {"kana": "ご", "romaji": "go"}
    ],
    3: [
        {"kana": "さ", "romaji": "sa"},
        {"kana": "し", "romaji": "shi"},
        {"kana": "す", "romaji": "su"},
        {"kana": "せ", "romaji": "se"},
        {"kana": "そ", "romaji": "so"},
        {"kana": "ざ", "romaji": "za"},
        {"kana": "じ", "romaji": "ji"},
        {"kana": "ず", "romaji": "zu"},
        {"kana": "ぜ", "romaji": "ze"},
        {"kana": "ぞ", "romaji": "zo"}
    ],
    4: [
        {"kana": "た", "romaji": "ta"},
        {"kana": "ち", "romaji": "chi"},
        {"kana": "つ", "romaji": "tsu"},
        {"kana": "て", "romaji": "te"},
        {"kana": "と", "romaji": "to"},
        {"kana": "だ", "romaji": "da"},
        {"kana": "ぢ", "romaji": "di"},
        {"kana": "づ", "romaji": "du"},
        {"kana": "で", "romaji": "de"},
        {"kana": "ど", "romaji": "do"}
    ],
    5: [
        {"kana": "な", "romaji": "na"},
        {"kana": "に", "romaji": "ni"},
        {"kana": "ぬ", "romaji": "nu"},
        {"kana": "ね", "romaji": "ne"},
        {"kana": "の", "romaji": "no"}
    ],
    6: [
        {"kana": "は", "romaji": "ha"},
        {"kana": "ひ", "romaji": "hi"},
        {"kana": "ふ", "romaji": "fu"},
        {"kana": "へ", "romaji": "he"},
        {"kana": "ほ", "romaji": "ho"},
        {"kana": "ば", "romaji": "ba"},
        {"kana": "び", "romaji": "bi"},
        {"kana": "ぶ", "romaji": "bu"},
        {"kana": "べ", "romaji": "be"},
        {"kana": "ぼ", "romaji": "bo"},
        {"kana": "ぱ", "romaji": "pa"},
        {"kana": "ぴ", "romaji": "pi"},
        {"kana": "ぷ", "romaji": "pu"},
        {"kana": "ぺ", "romaji": "pe"},
        {"kana": "ぽ", "romaji": "po"}
    ],
    7: [
        {"kana": "ま", "romaji": "ma"},
        {"kana": "み", "romaji": "mi"},
        {"kana": "む", "romaji": "mu"},
        {"kana": "め", "romaji": "me"},
        {"kana": "も", "romaji": "mo"}
    ],
    8: [
        {"kana": "ら", "romaji": "ra"},
        {"kana": "り", "romaji": "ri"},
        {"kana": "る", "romaji": "ru"},
        {"kana": "れ", "romaji": "re"},
        {"kana": "ろ", "romaji": "ro"}
    ],
    9: [
        {"kana": "や", "romaji": "ya"},
        {"kana": "ゆ", "romaji": "yu"},
        {"kana": "よ", "romaji": "yo"},
        {"kana": "わ", "romaji": "wa"},
        {"kana": "を", "romaji": "wo"}
    ],
    10: [
        {"kana": "ん", "romaji": "n"},
        {"kana": "わ", "romaji": "wa"},
        {"kana": "れ", "romaji": "re"},
        {"kana": "ね", "romaji": "ne"},
        {"kana": "る", "romaji": "ru"},
        {"kana": "ろ", "romaji": "ro"},
        {"kana": "が", "romaji": "ga"},
        {"kana": "ざ", "romaji": "za"},
        {"kana": "だ", "romaji": "da"},
        {"kana": "ば", "romaji": "ba"},
        {"kana": "ぱ", "romaji": "pa"}
    ],
    11: ALL_71_HIRAGANA
}

# ==============================================================================
# KATAKANA SYLLABARY DEFINITIONS (46 Core + 20 Dakuten + 5 Handakuten = 71 Total)
# ==============================================================================
ALL_46_KATAKANA = [
    # A-line
    {"kana": "ア", "romaji": "a"},
    {"kana": "イ", "romaji": "i"},
    {"kana": "ウ", "romaji": "u"},
    {"kana": "エ", "romaji": "e"},
    {"kana": "オ", "romaji": "o"},
    # Ka-line
    {"kana": "カ", "romaji": "ka"},
    {"kana": "キ", "romaji": "ki"},
    {"kana": "ク", "romaji": "ku"},
    {"kana": "ケ", "romaji": "ke"},
    {"kana": "コ", "romaji": "ko"},
    # Sa-line
    {"kana": "サ", "romaji": "sa"},
    {"kana": "シ", "romaji": "shi"},
    {"kana": "ス", "romaji": "su"},
    {"kana": "セ", "romaji": "se"},
    {"kana": "ソ", "romaji": "so"},
    # Ta-line
    {"kana": "タ", "romaji": "ta"},
    {"kana": "チ", "romaji": "chi"},
    {"kana": "ツ", "romaji": "tsu"},
    {"kana": "テ", "romaji": "te"},
    {"kana": "ト", "romaji": "to"},
    # Na-line
    {"kana": "ナ", "romaji": "na"},
    {"kana": "ニ", "romaji": "ni"},
    {"kana": "ヌ", "romaji": "nu"},
    {"kana": "ネ", "romaji": "ne"},
    {"kana": "ノ", "romaji": "no"},
    # Ha-line
    {"kana": "ハ", "romaji": "ha"},
    {"kana": "ヒ", "romaji": "hi"},
    {"kana": "フ", "romaji": "fu"},
    {"kana": "ヘ", "romaji": "he"},
    {"kana": "ホ", "romaji": "ho"},
    # Ma-line
    {"kana": "マ", "romaji": "ma"},
    {"kana": "ミ", "romaji": "mi"},
    {"kana": "ム", "romaji": "mu"},
    {"kana": "メ", "romaji": "me"},
    {"kana": "モ", "romaji": "mo"},
    # Ya-line
    {"kana": "ヤ", "romaji": "ya"},
    {"kana": "ユ", "romaji": "yu"},
    {"kana": "ヨ", "romaji": "yo"},
    # Ra-line
    {"kana": "ラ", "romaji": "ra"},
    {"kana": "リ", "romaji": "ri"},
    {"kana": "ル", "romaji": "ru"},
    {"kana": "レ", "romaji": "re"},
    {"kana": "ロ", "romaji": "ro"},
    # Wa-line & N
    {"kana": "ワ", "romaji": "wa"},
    {"kana": "ヲ", "romaji": "wo"},
    {"kana": "ン", "romaji": "n"}
]

DAKUTEN_KATAKANA = [
    # G-line (Ka + Ten-Ten)
    {"kana": "ガ", "romaji": "ga"},
    {"kana": "ギ", "romaji": "gi"},
    {"kana": "グ", "romaji": "gu"},
    {"kana": "ゲ", "romaji": "ge"},
    {"kana": "ゴ", "romaji": "go"},
    # Z-line (Sa + Ten-Ten)
    {"kana": "ザ", "romaji": "za"},
    {"kana": "ジ", "romaji": "ji"},
    {"kana": "ズ", "romaji": "zu"},
    {"kana": "ゼ", "romaji": "ze"},
    {"kana": "ゾ", "romaji": "zo"},
    # D-line (Ta + Ten-Ten)
    {"kana": "ダ", "romaji": "da"},
    {"kana": "ヂ", "romaji": "di"},
    {"kana": "ヅ", "romaji": "du"},
    {"kana": "デ", "romaji": "de"},
    {"kana": "ド", "romaji": "do"},
    # B-line (Ha + Ten-Ten)
    {"kana": "バ", "romaji": "ba"},
    {"kana": "ビ", "romaji": "bi"},
    {"kana": "ブ", "romaji": "bu"},
    {"kana": "ベ", "romaji": "be"},
    {"kana": "ボ", "romaji": "bo"},
]

HANDAKUTEN_KATAKANA = [
    # P-line (Ha + Maru)
    {"kana": "パ", "romaji": "pa"},
    {"kana": "ピ", "romaji": "pi"},
    {"kana": "プ", "romaji": "pu"},
    {"kana": "ペ", "romaji": "pe"},
    {"kana": "ポ", "romaji": "po"},
]

ALL_71_KATAKANA = ALL_46_KATAKANA + DAKUTEN_KATAKANA + HANDAKUTEN_KATAKANA

KATAKANA_STAGE_KANA = {
    1: [
        {"kana": "ア", "romaji": "a"},
        {"kana": "イ", "romaji": "i"},
        {"kana": "ウ", "romaji": "u"},
        {"kana": "エ", "romaji": "e"},
        {"kana": "オ", "romaji": "o"}
    ],
    2: [
        {"kana": "カ", "romaji": "ka"},
        {"kana": "キ", "romaji": "ki"},
        {"kana": "ク", "romaji": "ku"},
        {"kana": "ケ", "romaji": "ke"},
        {"kana": "コ", "romaji": "ko"},
        {"kana": "ガ", "romaji": "ga"},
        {"kana": "ギ", "romaji": "gi"},
        {"kana": "グ", "romaji": "gu"},
        {"kana": "ゲ", "romaji": "ge"},
        {"kana": "ゴ", "romaji": "go"}
    ],
    3: [
        {"kana": "サ", "romaji": "sa"},
        {"kana": "シ", "romaji": "shi"},
        {"kana": "ス", "romaji": "su"},
        {"kana": "セ", "romaji": "se"},
        {"kana": "ソ", "romaji": "so"},
        {"kana": "ザ", "romaji": "za"},
        {"kana": "ジ", "romaji": "ji"},
        {"kana": "ズ", "romaji": "zu"},
        {"kana": "ゼ", "romaji": "ze"},
        {"kana": "ゾ", "romaji": "zo"}
    ],
    4: [
        {"kana": "タ", "romaji": "ta"},
        {"kana": "チ", "romaji": "chi"},
        {"kana": "ツ", "romaji": "tsu"},
        {"kana": "テ", "romaji": "te"},
        {"kana": "ト", "romaji": "to"},
        {"kana": "ダ", "romaji": "da"},
        {"kana": "ヂ", "romaji": "di"},
        {"kana": "ヅ", "romaji": "du"},
        {"kana": "デ", "romaji": "de"},
        {"kana": "ド", "romaji": "do"}
    ],
    5: [
        {"kana": "ナ", "romaji": "na"},
        {"kana": "ニ", "romaji": "ni"},
        {"kana": "ヌ", "romaji": "nu"},
        {"kana": "ネ", "romaji": "ne"},
        {"kana": "ノ", "romaji": "no"}
    ],
    6: [
        {"kana": "ハ", "romaji": "ha"},
        {"kana": "ヒ", "romaji": "hi"},
        {"kana": "フ", "romaji": "fu"},
        {"kana": "ヘ", "romaji": "he"},
        {"kana": "ホ", "romaji": "ho"},
        {"kana": "バ", "romaji": "ba"},
        {"kana": "ビ", "romaji": "bi"},
        {"kana": "ブ", "romaji": "bu"},
        {"kana": "ベ", "romaji": "be"},
        {"kana": "ボ", "romaji": "bo"},
        {"kana": "パ", "romaji": "pa"},
        {"kana": "ピ", "romaji": "pi"},
        {"kana": "プ", "romaji": "pu"},
        {"kana": "ペ", "romaji": "pe"},
        {"kana": "ポ", "romaji": "po"}
    ],
    7: [
        {"kana": "マ", "romaji": "ma"},
        {"kana": "ミ", "romaji": "mi"},
        {"kana": "ム", "romaji": "mu"},
        {"kana": "メ", "romaji": "me"},
        {"kana": "モ", "romaji": "mo"}
    ],
    8: [
        {"kana": "ラ", "romaji": "ra"},
        {"kana": "リ", "romaji": "ri"},
        {"kana": "ル", "romaji": "ru"},
        {"kana": "レ", "romaji": "re"},
        {"kana": "ロ", "romaji": "ro"}
    ],
    9: [
        {"kana": "ヤ", "romaji": "ya"},
        {"kana": "ユ", "romaji": "yu"},
        {"kana": "ヨ", "romaji": "yo"},
        {"kana": "ワ", "romaji": "wa"},
        {"kana": "ヲ", "romaji": "wo"}
    ],
    10: [
        {"kana": "ン", "romaji": "n"},
        {"kana": "ワ", "romaji": "wa"},
        {"kana": "レ", "romaji": "re"},
        {"kana": "ネ", "romaji": "ne"},
        {"kana": "ル", "romaji": "ru"},
        {"kana": "ロ", "romaji": "ro"},
        {"kana": "ガ", "romaji": "ga"},
        {"kana": "ザ", "romaji": "za"},
        {"kana": "ダ", "romaji": "da"},
        {"kana": "バ", "romaji": "ba"},
        {"kana": "パ", "romaji": "pa"}
    ],
    11: ALL_71_KATAKANA
}

TOTAL_GAUNTLET_KANA = 71

# Backward compatibility / generic aliases
STAGE_KANA = HIRAGANA_STAGE_KANA

def get_stage_kana(game_mode: str, stage: int) -> list[dict]:
    """Retrieve the kana list for the specified game mode and stage."""
    mapping = KATAKANA_STAGE_KANA if game_mode == "katakana" else HIRAGANA_STAGE_KANA
    return mapping.get(stage, mapping[1])

def get_gauntlet_kana(game_mode: str) -> list[dict]:
    """Retrieve all 71 kana for the specified game mode gauntlet."""
    return ALL_71_KATAKANA if game_mode == "katakana" else ALL_71_HIRAGANA

TRAFFIC_COLORS = ["blue", "green", "yellow", "purple", "cyan", "orange"]

# Visual Colors & Palette (RGB tuples)
COLOR_BG            = (15, 18, 24)
COLOR_PANEL_BG      = (10, 20, 36)
COLOR_PANEL_BORDER  = (0, 115, 191)
COLOR_WATER_DEEP    = (14, 48, 95)
COLOR_WATER_MID     = (24, 80, 145)
COLOR_WATER_SWELL   = (40, 115, 185)
COLOR_WATER_FOAM    = (215, 240, 255)
COLOR_BRIDGE_SHADOW = (8, 22, 42)
COLOR_WALKWAY_DARK  = (95, 100, 105)
COLOR_RAILING       = (190, 198, 205)
COLOR_BARRIER_RED   = (225, 45, 45)
COLOR_GOLD          = (255, 215, 0)
COLOR_CYAN          = (0, 217, 255)
COLOR_WHITE         = (255, 255, 255)
COLOR_BLACK         = (0, 0, 0)
COLOR_BEZEL         = (5, 8, 14)
COLOR_NEON_PURPLE   = (175, 45, 245)
COLOR_NEON_AMBER    = (255, 165, 0)
COLOR_NEON_CYAN     = (0, 235, 255)

def get_base_dir() -> str:
    """Resolve base directory whether running as source or frozen PyInstaller/AppImage bundle."""
    if getattr(sys, 'frozen', False):
        return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.isdir(os.path.join(cur_dir, 'assets')):
        return cur_dir
    parent_dir = os.path.dirname(cur_dir)
    if os.path.isdir(os.path.join(parent_dir, 'assets')):
        return parent_dir
    return cur_dir

def get_asset_path(subpath: str) -> str:
    """Return absolute path to an asset."""
    return os.path.join(get_base_dir(), 'assets', subpath)

def detect_maximum_resolution() -> tuple[int, int]:
    """Detect the maximum resolution supported by the system display."""
    import pygame
    candidates = []

    try:
        get_desktop_sizes = getattr(pygame.display, "get_desktop_sizes", None)
        if callable(get_desktop_sizes):
            sizes = get_desktop_sizes()
            if sizes:
                for sz in sizes:
                    if isinstance(sz, (tuple, list)) and len(sz) >= 2:
                        candidates.append((int(sz[0]), int(sz[1])))
    except Exception as e:
        print(f"[Display] Note querying desktop sizes: {e}")

    try:
        modes = pygame.display.list_modes()
        if modes and modes != -1:
            for m in modes:
                if isinstance(m, (tuple, list)) and len(m) >= 2:
                    candidates.append((int(m[0]), int(m[1])))
    except Exception as e:
        print(f"[Display] Note querying list_modes: {e}")

    try:
        info = pygame.display.Info()
        if info.current_w > 0 and info.current_h > 0:
            candidates.append((int(info.current_w), int(info.current_h)))
    except Exception as e:
        print(f"[Display] Note querying display info: {e}")

    valid_candidates = [
        (w, h) for (w, h) in candidates
        if w >= 640 and h >= 400
    ]

    if valid_candidates:
        best = max(valid_candidates, key=lambda s: (s[0] * s[1], s[0]))
        return best

    return (VIRTUAL_WIDTH, VIRTUAL_HEIGHT)

def compute_aspect_ratio(w: int, h: int) -> tuple[float, str]:
    """Compute aspect ratio float and descriptive label."""
    if h <= 0:
        return (16.0 / 9.0, "16:9")
    ratio = w / h
    if abs(ratio - (16.0 / 10.0)) < 0.04:
        return (16.0 / 10.0, "16:10 (Native / Steam Deck)")
    elif abs(ratio - (16.0 / 9.0)) < 0.04:
        return (16.0 / 9.0, "16:9 (Standard HDTV / Monitor)")
    elif abs(ratio - (4.0 / 3.0)) < 0.04:
        return (4.0 / 3.0, "4:3 (Classic CRT Arcade)")
    elif abs(ratio - (21.0 / 9.0)) < 0.12:
        return (21.0 / 9.0, "21:9 (Ultrawide)")
    elif abs(ratio - (32.0 / 9.0)) < 0.15:
        return (32.0 / 9.0, "32:9 (Super Ultrawide)")
    else:
        return (ratio, f"Custom ({w}x{h})")

def get_virtual_dimensions(w: int = 1920, h: int = 1200, aspect_mode: str = "auto") -> tuple[int, int]:
    """Calculate virtual canvas dimensions. Nihongo Master permanently runs in 16:10 standard (1920x1200)."""
    return (1920, 1200)
