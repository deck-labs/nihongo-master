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
GAME_VERSION = "1.5.7"
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
    1: "BROAD HIGHWAY // EXPANSIVE STRAIGHTS // CEDAR",
    2: "COASTAL BRIDGE // STEEL SPANS // NARROW PASS",
    3: "TROPICAL BEACH // SHORELINE // COASTAL SWEEPS",
    4: "MOUNTAIN PASS // ROCKY GORGE // S-CURVES",
    5: "NEON EXPRESSWAY // HIGH-SPEED // SKYSCRAPERS",
    6: "VOLCANIC RIDGE // OBSIDIAN CRAGS // FAST APEX",
    7: "FROST GLACIER // POLAR ICEFALL // ICY APEX",
    8: "SAKURA BOULEVARD // SPRING DRIFT // PETALS",
    9: "RED ROCK CANYON // DUSK MESAS // GORGE SWEEPS",
    10: "FUJI SPEEDWAY // GRAND PRIX // GOLDEN APEX",
    11: "SECRET STAGE // ALL 71 KANA // COSMIC AURORA"
}

# ==============================================================================
# 3D HIRAGANA CARDS STAGE CONFIGURATIONS (8 Stages - Godot & Blender Engine)
# ==============================================================================
CARD_TOTAL_STAGES = 8

CARD_STAGE_INFO = {
    1: {
        "title": "BASIC VOWELS",
        "japanese": "基本母音（あ・い・う・え・お）",
        "difficulty": 1,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["あお (Blue)", "いえ (House)", "うえ (Above)", "ねこ (Cat)", "そら (Sky)"],
        "summary": "Master foundational vowels across 3 sets (9 words). Set 1: Pure Vowels • Set 2: Consonant Basics • Set 3: Everyday Nature.",
        "kana_preview": ["あ", "い", "う", "え", "お"]
    },
    2: {
        "title": "KA, SA, TA, NA LINES",
        "japanese": "か・さ・た・な行（子音基礎）",
        "difficulty": 2,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["さかな (Fish)", "つき (Moon)", "たけ (Bamboo)", "いぬ (Dog)", "はな (Flower)"],
        "summary": "Expand into primary consonant syllables across 3 sets (9 words). Decoys include same-line distractors to test phonetic recall.",
        "kana_preview": ["か", "き", "く", "さ", "た", "な"]
    },
    3: {
        "title": "CORE SYLLABLES & LOOKALIKES",
        "japanese": "類似文字・識別（さ/き・わ/れ）",
        "difficulty": 3,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["さくら (Cherry)", "くるま (Car)", "とり (Bird)", "やま (Mountain)", "かわ (River)"],
        "summary": "Form everyday 3-kana terms across 3 sets (9 words) while distinguishing lookalike Kana characters (さ vs き, わ vs れ).",
        "kana_preview": ["さ", "き", "わ", "れ", "ら", "り"]
    },
    4: {
        "title": "VOICED CONSONANTS (DAKUTEN)",
        "japanese": "濁音（が・ざ・だ・ば・ご）",
        "difficulty": 4,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["りんご (Apple)", "みず (Water)", "かぜ (Wind)", "えいが (Movie)", "ともだち (Friend)"],
        "summary": "Identify voiced mark Dakuten across 3 sets (9 words). Hand cards feature unvoiced decoy traps testing mark recognition.",
        "kana_preview": ["が", "ぎ", "ざ", "だ", "ば", "ご"]
    },
    5: {
        "title": "HANDAKUTEN & NASAL 'N'",
        "japanese": "半濁音・撥音（ぱ・ぴ・ん）",
        "difficulty": 5,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["きんぎょ (Goldfish)", "しんぶん (News)", "てんぷら (Tempura)", "えんぴつ (Pencil)", "さんぽ (Stroll)"],
        "summary": "P-sounds with Handakuten (゜) and nasal ん across 3 sets (9 words). Decoys challenge visual distinction with Dakuten.",
        "kana_preview": ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ", "ん"]
    },
    6: {
        "title": "SOKUON & GEMINATE STOPS",
        "japanese": "促音（っ）・詰まる音",
        "difficulty": 6,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["きって (Stamp)", "がっこう (School)", "ざっし (Magazine)", "きっぷ (Ticket)", "しっぽ (Tail)"],
        "summary": "Tackle small 'っ' geminate glottal stops across 3 sets (9 words). Decoys present full 'つ' vs small 'っ' to sharpen precision.",
        "kana_preview": ["っ", "つ", "き", "て", "が", "こ"]
    },
    7: {
        "title": "ADVANCED COMPOUNDS",
        "japanese": "上級語彙・複合表現",
        "difficulty": 7,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["おんがく (Music)", "ひこうき (Plane)", "ちかてつ (Subway)", "びょういん (Clinic)", "りょこう (Trip)"],
        "summary": "Multi-syllable compound words across 3 sets (9 words) combining long vowels, Dakuten, and compound Kana formations.",
        "kana_preview": ["お", "ん", "が", "く", "ひ", "こ"]
    },
    8: {
        "title": "GRAND MASTER GAUNTLET",
        "japanese": "免許皆伝・最終試練",
        "difficulty": 8,
        "sets": 3,
        "total_words": 10,
        "goal": 4,
        "words": ["とうきょう (Tokyo)", "にほんご (Japanese)", "せんせい (Teacher)", "しょうぼうしゃ (Fire Engine)", "ありがとう (Thank You)"],
        "summary": "Ultimate test of Hiragana fluency across 3 sets (10 words total). Authentic vocabulary with all syllabic modifiers and traps.",
        "kana_preview": ["と", "う", "き", "ょ", "に", "ほ"]
    }
}

# ==============================================================================
# 3D KATAKANA CARDS STAGE CONFIGURATIONS (8 Stages - Godot & Blender Engine)
# ==============================================================================
KATAKANA_CARD_TOTAL_STAGES = 8

KATAKANA_CARD_STAGE_INFO = {
    1: {
        "title": "BASIC LOANWORDS",
        "japanese": "基本外来語（ア・イ・ウ・エ・オ）",
        "difficulty": 1,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["ドア (Door)", "エア (Air)", "アイス (Ice Cream)", "メモ (Memo)", "バス (Bus)"],
        "summary": "Master fundamental Katakana loanwords across 3 sets (9 words). Set 1: Pure Vowels • Set 2: Everyday Basics • Set 3: Living & Nature.",
        "kana_preview": ["ア", "イ", "ウ", "エ", "オ"]
    },
    2: {
        "title": "KA, SA, TA SYLLABLES",
        "japanese": "カ・サ・タ・ナ行（子音基礎）",
        "difficulty": 2,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["カメラ (Camera)", "タクシー (Taxi)", "トマト (Tomato)", "バナナ (Banana)", "ホテル (Hotel)"],
        "summary": "Expand into core consonant lines across 3 sets (9 words). Decoys include phonetic distractors to sharpen reading speed.",
        "kana_preview": ["カ", "サ", "タ", "ナ", "ラ", "マ"]
    },
    3: {
        "title": "SHI/TSU & SO/N TRAPS",
        "japanese": "類似文字識別（シ/ツ・ソ/ン・ノ/メ）",
        "difficulty": 3,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["シャツ (Shirt)", "ツナ (Tuna)", "ソース (Sauce)", "パン (Bread)", "メロン (Melon)"],
        "summary": "Conquer the famous Katakana lookalikes (シ vs ツ, ソ vs ン, ノ vs メ) across 3 sets (9 words) with targeted trap cards.",
        "kana_preview": ["シ", "ツ", "ソ", "ン", "ノ", "メ"]
    },
    4: {
        "title": "VOICED CONSONANTS (DAKUTEN)",
        "japanese": "濁音（ガ・ザ・ダ・バ・ゴ）",
        "difficulty": 4,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["ガス (Gas)", "ゼロ (Zero)", "ビデオ (Video)", "ドラム (Drum)", "ギター (Guitar)"],
        "summary": "Identify voiced Dakuten marks across 3 sets (9 words). Decoy cards feature unvoiced counterparts to test mark awareness.",
        "kana_preview": ["ガ", "ギ", "ザ", "ダ", "バ", "ゴ"]
    },
    5: {
        "title": "HANDAKUTEN & CHOONPU",
        "japanese": "半濁音・長音「ー」（パ行・伸ばす音）",
        "difficulty": 5,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["パン (Bread)", "ピアノ (Piano)", "コーヒー (Coffee)", "ケーキ (Cake)", "チーズ (Cheese)"],
        "summary": "Practice P-sounds (パ行) and the essential long vowel dash (ー) across 3 sets (9 words) in common cafe and sport words.",
        "kana_preview": ["パ", "ピ", "プ", "ー", "コ", "ケ"]
    },
    6: {
        "title": "SOKUON DOUBLE STOPS",
        "japanese": "促音「ッ」・詰まる音",
        "difficulty": 6,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["コップ (Cup)", "ベッド (Bed)", "サッカー (Soccer)", "ロケット (Rocket)", "チケット (Ticket)"],
        "summary": "Master the small 'ッ' glottal double consonant across 3 sets (9 words). Decoys pit full 'ツ' against small 'ッ'.",
        "kana_preview": ["ッ", "ツ", "コ", "プ", "ベ", "ド"]
    },
    7: {
        "title": "FOREIGN SOUNDS & YOON",
        "japanese": "外来音・拗音（ファ/フィ/シェ/チェ/ティ）",
        "difficulty": 7,
        "sets": 3,
        "total_words": 9,
        "goal": 3,
        "words": ["カフェ (Cafe)", "パーティー (Party)", "チョコ (Chocolate)", "フィルム (Film)", "シェフ (Chef)"],
        "summary": "Specialized modern foreign phonemes (ファ, フィ, ティ, ディ, シェ, チェ) across 3 sets (9 words) for international loanwords.",
        "kana_preview": ["フ", "ェ", "ィ", "テ", "シ", "チ"]
    },
    8: {
        "title": "GRAND MASTER GAUNTLET",
        "japanese": "免許皆伝・最終試練",
        "difficulty": 8,
        "sets": 3,
        "total_words": 10,
        "goal": 4,
        "words": ["ハンバーガー (Hamburger)", "レストラン (Restaurant)", "パスポート (Passport)", "エレベーター (Elevator)", "テーマパーク (Theme Park)"],
        "summary": "The ultimate test of Katakana fluency across 3 sets (10 words). Complex multi-syllable loanwords with all modifier traps.",
        "kana_preview": ["ハ", "ン", "バ", "ー", "ガ", "レ"]
    }
}

# ==============================================================================
# THE GALLERY SNIPER (HIRAGANA) STAGE CONFIGURATIONS (8 Stages - Godot 2D Engine)
# ==============================================================================
SNIPER_TOTAL_STAGES = 8

SNIPER_STAGE_INFO = {
    1: {
        "title": "2-KANA FOUNDATIONAL BASICS",
        "japanese": "基本2文字語彙（あお・いえ・うえ・あい・あさ・うみ）",
        "difficulty": 1,
        "words": ["あお (Blue)", "いえ (House)", "うえ (Above)", "あい (Love)", "あさ (Morning)", "うみ (Sea)"],
        "summary": "Short 2-character words with simple vowels and basic consonants. Stationary gallery targets with 3 decoys.",
        "kana_preview": ["あ", "い", "う", "え", "お", "さ"]
    },
    2: {
        "title": "2-KANA FAMILIAR NOUNS",
        "japanese": "基本名詞・動物（ねこ・いぬ・とり・はな・やま・かわ）",
        "difficulty": 2,
        "words": ["ねこ (Cat)", "いぬ (Dog)", "とり (Bird)", "はな (Flower)", "やま (Mountain)", "かわ (River)"],
        "summary": "2-character everyday nouns across core consonant rows (k, s, t, n, h, y, r, w) with 4 decoys.",
        "kana_preview": ["ね", "い", "と", "は", "や", "か"]
    },
    3: {
        "title": "3-KANA SEQUENTIAL SPELLING",
        "japanese": "3文字語彙（さくら・くるま・たまご・こども・ひかり）",
        "difficulty": 3,
        "words": ["さくら (Cherry Blossom)", "くるま (Car)", "たまご (Egg)", "こども (Child)", "ひかり (Light)", "さかな (Fish)"],
        "summary": "Multi-syllable 3-character nouns requiring sequential spelling across three shelf targets with 4 decoys.",
        "kana_preview": ["さ", "く", "た", "こ", "ひ", "ま"]
    },
    4: {
        "title": "VOICED DAKUTEN & NASAL 'ん'",
        "japanese": "濁音・撥音（りんご・みかん・でんわ・てがみ・かぞく）",
        "difficulty": 4,
        "words": ["りんご (Apple)", "みかん (Mandarin)", "でんわ (Phone)", "てがみ (Letter)", "かぞく (Family)", "ともだち (Friend)"],
        "summary": "3 to 4 character words introducing voiced Dakuten (が・ざ・だ・ば) and nasal 'ん' spelling with 5 decoys.",
        "kana_preview": ["が", "ざ", "だ", "ば", "ん", "で"]
    },
    5: {
        "title": "SOKUON SMALL 'っ' & HANDAKUTEN",
        "japanese": "促音「っ」・半濁音（きって・きっぷ・ざっし・てんぷら）",
        "difficulty": 5,
        "words": ["きって (Stamp)", "きっぷ (Ticket)", "ざっし (Magazine)", "しっぽ (Tail)", "てんぷら (Tempura)", "えんぴつ (Pencil)"],
        "summary": "Tricky spelling featuring geminate double consonants (small 'っ') and Handakuten 'P' stops with 5 decoys.",
        "kana_preview": ["っ", "き", "て", "ぷ", "ざ", "え"]
    },
    6: {
        "title": "LONG VOWELS & 4-KANA COMPOUNDS",
        "japanese": "長音・複合語（がっこう・ひこうき・ちかてつ・せんせい）",
        "difficulty": 6,
        "words": ["がっこう (School)", "ひこうき (Airplane)", "ちかてつ (Subway)", "おんがく (Music)", "せんせい (Teacher)", "こうえん (Park)"],
        "summary": "Longer 4-character compound words featuring phonetic vowel elongations (お・う, え・い) with 6 decoys.",
        "kana_preview": ["が", "ひ", "ち", "お", "せ", "こ"]
    },
    7: {
        "title": "CONTRACTED DIGRAPHS (YO-ON)",
        "japanese": "拗音「ゃ・ゅ・ょ」（きんぎょ・りょこう・びょういん）",
        "difficulty": 7,
        "words": ["きんぎょ (Goldfish)", "りょこう (Travel)", "びょういん (Hospital)", "しょうぼう (Firefighting)", "きょうしつ (Classroom)"],
        "summary": "Challenging contracted digraphs combining standard syllables with small ゃ・ゅ・ょ across 4 to 5 kana with 6 decoys.",
        "kana_preview": ["ぎ", "ょ", "り", "び", "し", "ゅ"]
    },
    8: {
        "title": "MASTER SPELLING GAUNTLET (5-7 KANA)",
        "japanese": "達人試練・超長文語彙（ありがとう・とうきょう・しょうぼうしゃ）",
        "difficulty": 8,
        "words": ["ありがとう (Thank You)", "とうきょう (Tokyo)", "としょかん (Library)", "しょうぼうしゃ (Fire Engine)", "きゅうきゅうしゃ (Ambulance)", "しんかんせん (Bullet Train)"],
        "summary": "Maximum length and spelling complexity! Multi-rule 5 to 7-character compound words tested across 7 shelf decoys.",
        "kana_preview": ["あ", "と", "し", "ょ", "き", "ゅ"]
    }
}

# ==============================================================================
# THE GALLERY SNIPER (KATAKANA) STAGE CONFIGURATIONS (8 Stages - Godot 2D Engine)
# ==============================================================================
KATAKANA_SNIPER_TOTAL_STAGES = 8

KATAKANA_SNIPER_STAGE_INFO = {
    1: {
        "title": "2-KANA NOVICE LOANWORDS",
        "japanese": "基本2文字外来語（ドア・エア・メモ・バス・ペン・ガス）",
        "difficulty": 1,
        "words": ["ドア (Door)", "エア (Air)", "メモ (Memo)", "バス (Bus)", "ペン (Pen)", "ガス (Gas)"],
        "summary": "Shortest 2-character foundational loanwords with simple phonetics. Stationary targets with 3 decoys.",
        "kana_preview": ["ド", "ア", "エ", "メ", "バ", "ペ"]
    },
    2: {
        "title": "2-3 KANA ELEMENTARY FOOD & OBJECTS",
        "japanese": "初級外来語（パン・アイス・トマト・バナナ・カメラ）",
        "difficulty": 2,
        "words": ["パン (Bread)", "アイス (Ice Cream)", "トマト (Tomato)", "バナナ (Banana)", "カメラ (Camera)", "ミルク (Milk)"],
        "summary": "Everyday 2 to 3-character international loanwords covering standard syllables with 4 decoys.",
        "kana_preview": ["パ", "ア", "ト", "バ", "カ", "ミ"]
    },
    3: {
        "title": "CHOONPU LONG VOWEL DASH 'ー'",
        "japanese": "長音記号「ー」（ケーキ・コーヒー・ノート・タオル・ソファー）",
        "difficulty": 3,
        "words": ["ケーキ (Cake)", "コーヒー (Coffee)", "ノート (Notebook)", "タオル (Towel)", "ソファー (Sofa)", "チーズ (Cheese)"],
        "summary": "3 to 4 character loanwords requiring correct placement of the long vowel mark (ー) with 4 decoys.",
        "kana_preview": ["ー", "ケ", "コ", "ノ", "タ", "ソ"]
    },
    4: {
        "title": "SOKUON SMALL 'ッ' DOUBLE STOPS",
        "japanese": "促音「ッ」（ベッド・コップ・カップ・ロッカー・マッチ）",
        "difficulty": 4,
        "words": ["ベッド (Bed)", "コップ (Cup)", "カップ (Mug)", "ロッカー (Locker)", "マッチ (Match)", "ベル (Bell)"],
        "summary": "Tricky spelling with geminate small 'ッ' consonant stops in common foreign words with 5 decoys.",
        "kana_preview": ["ッ", "ベ", "コ", "カ", "ロ", "マ"]
    },
    5: {
        "title": "VOICED LOANWORDS & TECH VOCABULARY",
        "japanese": "濁音・家電技術（ピアノ・ピザ・パソコン・ポスト・プリン）",
        "difficulty": 5,
        "words": ["ピアノ (Piano)", "ピザ (Pizza)", "パソコン (PC)", "ポスト (Mailbox)", "プリン (Pudding)", "テレビ (TV)"],
        "summary": "3 to 4 character technology and lifestyle terms featuring Handakuten (パ行) and Dakuten marks with 5 decoys.",
        "kana_preview": ["ピ", "パ", "ポ", "プ", "テ", "ビ"]
    },
    6: {
        "title": "DUAL RULE: LONG VOWELS + SOKUON",
        "japanese": "長音＋促音複合語（ラーメン・スケート・スプーン・ロケット）",
        "difficulty": 6,
        "words": ["ラーメン (Ramen)", "スケート (Skate)", "スプーン (Spoon)", "ロケット (Rocket)", "テーブル (Table)", "タクシー (Taxi)"],
        "summary": "4-character compound loanwords combining long vowel lines (ー) with small 'ッ' stops across 6 decoys.",
        "kana_preview": ["ー", "ッ", "ラ", "ス", "ロ", "テ"]
    },
    7: {
        "title": "EXTENDED DIGRAPHS & MODERN LOANWORDS",
        "japanese": "外来音・長音（ジュース・シャツ・スパゲッティ・チョコレート）",
        "difficulty": 7,
        "words": ["スマホ (Smartphone)", "アニメ (Anime)", "ジュース (Juice)", "シャツ (Shirt)", "スパゲッティ (Spaghetti)", "チョコレート (Chocolate)"],
        "summary": "Complex foreign phonetics combining contracted digraphs (ジュ, シャ, チョ, ティ) across 4 to 6 characters with 6 decoys.",
        "kana_preview": ["ジ", "シ", "チ", "ュ", "ャ", "ョ"]
    },
    8: {
        "title": "MASTER KATAKANA GAUNTLET (5-7 KANA)",
        "japanese": "免許皆伝・超長文外来語（レストラン・エレベーター・エスカレーター）",
        "difficulty": 8,
        "words": ["レストラン (Restaurant)", "エレベーター (Elevator)", "エスカレーター (Escalator)", "コンピュータ (Computer)", "サンドイッチ (Sandwich)", "アイスクリーム (Ice Cream)"],
        "summary": "The ultimate Katakana spelling test! 5 to 7-character complex loanwords challenging memory and quick targeting with 7 decoys.",
        "kana_preview": ["レ", "エ", "ス", "コ", "サ", "ア"]
    }
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
COLOR_BG            = (24, 31, 42)    # Eye-friendly soft dark slate
COLOR_PANEL_BG      = (28, 37, 52)    # Elevated slate container
COLOR_PANEL_BORDER  = (45, 95, 155)   # Muted slate-cyan border
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
COLOR_WHITE         = (228, 234, 242) # Soft off-white to eliminate halation
COLOR_BLACK         = (0, 0, 0)
COLOR_BEZEL         = (20, 26, 36)    # Soft charcoal letterbox
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
