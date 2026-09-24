class_name WordsData
extends RefCounted

const GOJUON_POOL = [
	"あ", "い", "う", "え", "お",
	"か", "き", "く", "け", "こ",
	"さ", "し", "す", "せ", "そ",
	"た", "ち", "つ", "て", "と",
	"な", "に", "ぬ", "ね", "の",
	"は", "ひ", "ふ", "へ", "ほ",
	"ま", "み", "む", "め", "も",
	"や", "ゆ", "よ",
	"ら", "り", "る", "れ", "ろ",
	"わ", "を", "ん"
]

const DAKUTEN_POOL = [
	"が", "ぎ", "ぐ", "げ", "ご",
	"ざ", "じ", "ず", "ぜ", "ぞ",
	"だ", "ぢ", "づ", "で", "ど",
	"ば", "び", "ぶ", "べ", "ぼ"
]

const HANDAKUTEN_POOL = [
	"ぱ", "ぴ", "ぷ", "ぺ", "ぽ"
]

const SOKUON_POOL = [
	"っ", "ゃ", "ゅ", "ょ"
]

const CONFUSABLE_MAP = {
	"さ": "き", "き": "さ",
	"は": "ほ", "ほ": "は",
	"め": "ぬ", "ぬ": "め",
	"わ": "れ", "れ": "わ",
	"ね": "れ", "る": "ろ", "ろ": "る",
	"あ": "お", "お": "あ",
	"が": "か", "ぎ": "き", "ぐ": "く", "げ": "け", "ご": "こ",
	"ざ": "さ", "じ": "し", "ず": "す", "ぜ": "せ", "ぞ": "そ",
	"だ": "た", "で": "て", "ど": "と",
	"ば": "は", "び": "ひ", "ぶ": "ふ", "べ": "へ", "ぼ": "ほ",
	"ぱ": "ば", "ぴ": "び", "ぷ": "ぶ", "ぺ": "べ", "ぽ": "ぼ",
	"っ": "つ", "つ": "っ"
}

# --- STAGE 1: Basic Vowels & First 2-Kana Words (Goal: 3) ---
const STAGE1_WORDS = [
	{"romaji": "NEKO", "meaning": "cat", "kana": ["ね", "こ"]},
	{"romaji": "INU", "meaning": "dog", "kana": ["い", "ぬ"]},
	{"romaji": "UMI", "meaning": "sea", "kana": ["う", "み"]},
	{"romaji": "IE", "meaning": "house", "kana": ["い", "え"]},
	{"romaji": "AKI", "meaning": "autumn", "kana": ["あ", "き"]},
	{"romaji": "SORA", "meaning": "sky", "kana": ["そ", "ら"]},
	{"romaji": "YAMA", "meaning": "mountain", "kana": ["や", "ま"]},
	{"romaji": "HANA", "meaning": "flower", "kana": ["は", "な"]},
	{"romaji": "KASA", "meaning": "umbrella", "kana": ["か", "さ"]},
	{"romaji": "KAME", "meaning": "turtle", "kana": ["か", "め"]},
	{"romaji": "TORI", "meaning": "bird", "kana": ["と", "り"]},
	{"romaji": "USHI", "meaning": "cow", "kana": ["う", "し"]},
	{"romaji": "MOMO", "meaning": "peach", "kana": ["も", "も"]},
	{"romaji": "FUYU", "meaning": "winter", "kana": ["ふ", "ゆ"]},
	{"romaji": "HARU", "meaning": "spring", "kana": ["は", "る"]},
	{"romaji": "NATSU", "meaning": "summer", "kana": ["な", "つ"]},
	{"romaji": "TSUKI", "meaning": "moon", "kana": ["つ", "き"]},
	{"romaji": "KAWA", "meaning": "river", "kana": ["か", "わ"]},
	{"romaji": "MORI", "meaning": "forest", "kana": ["も", "り"]},
	{"romaji": "HASHI", "meaning": "bridge", "kana": ["は", "し"]},
	{"romaji": "ASHI", "meaning": "foot", "kana": ["あ", "し"]},
	{"romaji": "KUMO", "meaning": "cloud", "kana": ["く", "も"]},
	{"romaji": "HITO", "meaning": "person", "kana": ["ひ", "と"]}
]

# --- STAGE 2: Ka, Sa, Ta, Na Lines (Goal: 3) ---
const STAGE2_WORDS = [
	{"romaji": "SUSHI", "meaning": "sushi", "kana": ["す", "し"]},
	{"romaji": "HACHI", "meaning": "bee", "kana": ["は", "ち"]},
	{"romaji": "SAKURA", "meaning": "cherry blossom", "kana": ["さ", "く", "ら"]},
	{"romaji": "KATANA", "meaning": "sword", "kana": ["か", "た", "な"]},
	{"romaji": "KITSUNE", "meaning": "fox", "kana": ["き", "つ", "ね"]},
	{"romaji": "TANUKI", "meaning": "raccoon dog", "kana": ["た", "ぬ", "き"]},
	{"romaji": "KARASU", "meaning": "crow", "kana": ["か", "ら", "す"]},
	{"romaji": "SEKAI", "meaning": "world", "kana": ["せ", "か", "い"]},
	{"romaji": "ASAHI", "meaning": "morning sun", "kana": ["あ", "さ", "ひ"]},
	{"romaji": "KOKORO", "meaning": "heart / spirit", "kana": ["こ", "こ", "ろ"]},
	{"romaji": "KAERU", "meaning": "frog", "kana": ["か", "え", "る"]},
	{"romaji": "ATAMA", "meaning": "head", "kana": ["あ", "た", "ま"]},
	{"romaji": "KIMONO", "meaning": "kimono", "kana": ["き", "も", "の"]},
	{"romaji": "TAKO", "meaning": "octopus", "kana": ["た", "こ"]},
	{"romaji": "SARU", "meaning": "monkey", "kana": ["さ", "る"]},
	{"romaji": "KUTSU", "meaning": "shoes", "kana": ["く", "つ"]},
	{"romaji": "SHIKA", "meaning": "deer", "kana": ["し", "か"]}
]

# --- STAGE 3: Expanded Core Syllables & Subtle Decoys (Goal: 4) ---
const STAGE3_WORDS = [
	{"romaji": "SAKANA", "meaning": "fish", "kana": ["さ", "か", "な"]},
	{"romaji": "KURUMA", "meaning": "car", "kana": ["く", "る", "ま"]},
	{"romaji": "YASAI", "meaning": "vegetable", "kana": ["や", "さ", "い"]},
	{"romaji": "KUSURI", "meaning": "medicine", "kana": ["く", "す", "り"]},
	{"romaji": "HIKARI", "meaning": "light", "kana": ["ひ", "か", "り"]},
	{"romaji": "TSUKIMI", "meaning": "moon viewing", "kana": ["つ", "き", "み"]},
	{"romaji": "MINATO", "meaning": "harbor", "kana": ["み", "な", "と"]},
	{"romaji": "KUMOMA", "meaning": "cloud rift", "kana": ["く", "も", "ま"]},
	{"romaji": "HOTARU", "meaning": "firefly", "kana": ["ほ", "た", "る"]},
	{"romaji": "SUZUME", "meaning": "sparrow", "kana": ["す", "ず", "め"]},
	{"romaji": "KAMOME", "meaning": "seagull", "kana": ["か", "も", "め"]},
	{"romaji": "TAMAGO", "meaning": "egg", "kana": ["た", "ま", "ご"]},
	{"romaji": "MIKAN", "meaning": "orange", "kana": ["み", "か", "ん"]}
]

# --- STAGE 4: Voiced Consonants (Dakuten が, ざ, だ, ば) (Goal: 4) ---
const STAGE4_WORDS = [
	{"romaji": "MIZU", "meaning": "water", "kana": ["み", "ず"]},
	{"romaji": "KAZE", "meaning": "wind", "kana": ["か", "ぜ"]},
	{"romaji": "CHIZU", "meaning": "map", "kana": ["ち", "ず"]},
	{"romaji": "KAGI", "meaning": "key", "kana": ["か", "ぎ"]},
	{"romaji": "EBI", "meaning": "shrimp", "kana": ["え", "び"]},
	{"romaji": "GOHAN", "meaning": "meal / rice", "kana": ["ご", "は", "ん"]},
	{"romaji": "RINGO", "meaning": "apple", "kana": ["り", "ん", "ご"]},
	{"romaji": "TOMODACHI", "meaning": "friend", "kana": ["と", "も", "だ", "ち"]},
	{"romaji": "TABEMONO", "meaning": "food", "kana": ["た", "べ", "も", "の"]},
	{"romaji": "INOSHISHI", "meaning": "wild boar", "kana": ["い", "の", "し", "し"]},
	{"romaji": "KABUTO", "meaning": "helmet", "kana": ["か", "ぶ", "と"]},
	{"romaji": "MEGANE", "meaning": "glasses", "kana": ["め", "が", "ね"]},
	{"romaji": "SUZU", "meaning": "bell", "kana": ["す", "ず"]},
	{"romaji": "BUDOU", "meaning": "grapes", "kana": ["ぶ", "ど", "う"]},
	{"romaji": "ZUBON", "meaning": "trousers", "kana": ["ず", "ぼ", "ん"]},
	{"romaji": "DENWA", "meaning": "telephone", "kana": ["で", "ん", "わ"]}
]

# --- STAGE 5: Handakuten & Nasal 'N' (ぱ, ぴ, ぷ, ぺ, ぽ, ん) (Goal: 4) ---
const STAGE5_WORDS = [
	{"romaji": "PAN", "meaning": "bread", "kana": ["ぱ", "ん"]},
	{"romaji": "SANPO", "meaning": "walk / stroll", "kana": ["さ", "ん", "ぽ"]},
	{"romaji": "ENPITSU", "meaning": "pencil", "kana": ["え", "ん", "ぴ", "つ"]},
	{"romaji": "SHINBUN", "meaning": "newspaper", "kana": ["し", "ん", "ぶ", "ん"]},
	{"romaji": "PIANO", "meaning": "piano", "kana": ["ぴ", "あ", "の"]},
	{"romaji": "BENTOU", "meaning": "bento box", "kana": ["べ", "ん", "と", "う"]},
	{"romaji": "TENPURA", "meaning": "tempura", "kana": ["て", "ん", "ぷ", "ら"]},
	{"romaji": "SUPUUN", "meaning": "spoon", "kana": ["す", "ぷ", "ー", "ん"]},
	{"romaji": "KAMISAMA", "meaning": "deity", "kana": ["か", "み", "さ", "ま"]},
	{"romaji": "KAPPA", "meaning": "river imp", "kana": ["か", "っ", "ぱ"]},
	{"romaji": "KIPPU", "meaning": "ticket", "kana": ["き", "っ", "ぷ"]}
]

# --- STAGE 6: Sokuon (Small つ) & Long Vowels (Goal: 5) ---
const STAGE6_WORDS = [
	{"romaji": "KIPPU", "meaning": "ticket", "kana": ["き", "っ", "ぷ"]},
	{"romaji": "GAKKOU", "meaning": "school", "kana": ["が", "っ", "こ", "う"]},
	{"romaji": "KITTE", "meaning": "stamp", "kana": ["き", "っ", "て"]},
	{"romaji": "ZASSHI", "meaning": "magazine", "kana": ["ざ", "っ", "し"]},
	{"romaji": "NIKKI", "meaning": "diary", "kana": ["に", "っ", "き"]},
	{"romaji": "KOPPU", "meaning": "glass / cup", "kana": ["こ", "っ", "ぷ"]},
	{"romaji": "OTTO", "meaning": "husband", "kana": ["お", "っ", "と"]},
	{"romaji": "SHIPPO", "meaning": "tail", "kana": ["し", "っ", "ぽ"]},
	{"romaji": "KEKKON", "meaning": "marriage", "kana": ["け", "っ", "こ", "ん"]},
	{"romaji": "HAPPOU", "meaning": "all directions", "kana": ["は", "っ", "ぽ", "う"]},
	{"romaji": "ISSHO", "meaning": "together", "kana": ["い", "っ", "し", "ょ"]},
	{"romaji": "CHIKATETSU", "meaning": "subway", "kana": ["ち", "か", "て", "つ"]}
]

# --- STAGE 7: Advanced Compounds & Cultural Vocabulary (Goal: 5) ---
const STAGE7_WORDS = [
	{"romaji": "ARIGATOU", "meaning": "thank you", "kana": ["あ", "り", "が", "と", "う"]},
	{"romaji": "SAYOUNARA", "meaning": "goodbye", "kana": ["さ", "よ", "う", "な", "ら"]},
	{"romaji": "OMATSURI", "meaning": "festival", "kana": ["お", "ま", "つ", "り"]},
	{"romaji": "YASASHISA", "meaning": "kindness", "kana": ["や", "さ", "し", "さ"]},
	{"romaji": "HATARAKI", "meaning": "work / function", "kana": ["は", "た", "ら", "き"]},
	{"romaji": "ASAYAKE", "meaning": "morning glow", "kana": ["あ", "さ", "や", "け"]},
	{"romaji": "SUBARASHII", "meaning": "magnificent", "kana": ["す", "ば", "ら", "し", "い"]},
	{"romaji": "ITADAKIMASU", "meaning": "bon appetit", "kana": ["い", "た", "だ", "き", "ま", "す"]},
	{"romaji": "DAIKOUKAI", "meaning": "great voyage", "kana": ["だ", "い", "こ", "う", "か", "い"]},
	{"romaji": "HOSHIZORA", "meaning": "starry sky", "kana": ["ほ", "し", "ぞ", "ら"]},
	{"romaji": "FUJISAN", "meaning": "Mount Fuji", "kana": ["ふ", "じ", "さ", "ん"]},
	{"romaji": "NAMIOTO", "meaning": "wave sound", "kana": ["な", "み", "お", "と"]}
]

# --- STAGE 8: Grand Master Gauntlet (Goal: 6) ---
const STAGE8_WORDS = [
	{"romaji": "NIHONGO", "meaning": "Japanese language", "kana": ["に", "ほ", "ん", "ご"]},
	{"romaji": "SHINKANSEN", "meaning": "bullet train", "kana": ["し", "ん", "か", "ん", "せ", "ん"]},
	{"romaji": "ARIGATOU", "meaning": "thank you", "kana": ["あ", "り", "が", "と", "う"]},
	{"romaji": "SUBARASHII", "meaning": "magnificent", "kana": ["す", "ば", "ら", "し", "い"]},
	{"romaji": "TOMODACHI", "meaning": "friend", "kana": ["と", "も", "だ", "ち"]},
	{"romaji": "KOKORO", "meaning": "heart / spirit", "kana": ["こ", "こ", "ろ"]},
	{"romaji": "SAKURA", "meaning": "cherry blossom", "kana": ["さ", "く", "ら"]},
	{"romaji": "HIKARI", "meaning": "light", "kana": ["ひ", "か", "り"]},
	{"romaji": "INOSHISHI", "meaning": "wild boar", "kana": ["い", "の", "し", "し"]},
	{"romaji": "ENPITSU", "meaning": "pencil", "kana": ["え", "ん", "ぴ", "つ"]},
	{"romaji": "GAKKOU", "meaning": "school", "kana": ["が", "っ", "こ", "う"]},
	{"romaji": "ITADAKIMASU", "meaning": "gratitude", "kana": ["い", "た", "だ", "き", "ま", "す"]},
	{"romaji": "DAIKOUKAI", "meaning": "great voyage", "kana": ["だ", "い", "こ", "う", "か", "い"]},
	{"romaji": "FUJISAN", "meaning": "Mount Fuji", "kana": ["ふ", "じ", "さ", "ん"]},
	{"romaji": "TABEMONO", "meaning": "food", "kana": ["た", "べ", "も", "の"]},
	{"romaji": "BENTOU", "meaning": "bento box", "kana": ["べ", "ん", "と", "う"]},
	{"romaji": "ZASSHI", "meaning": "magazine", "kana": ["ざ", "っ", "し"]},
	{"romaji": "SANPO", "meaning": "walk / stroll", "kana": ["さ", "ん", "ぽ"]}
]

const STAGE_DATA = {
	1: {
		"name": "Basic Vowels",
		"difficulty": "BEGINNER (★☆☆☆☆☆☆☆)",
		"goal": 3,
		"words": STAGE1_WORDS,
		"decoy_mode": "random"
	},
	2: {
		"name": "Ka, Sa, Ta Combat",
		"difficulty": "NOVICE (★★☆☆☆☆☆☆)",
		"goal": 3,
		"words": STAGE2_WORDS,
		"decoy_mode": "similar"
	},
	3: {
		"name": "Expanded Syllabary",
		"difficulty": "INTERMEDIATE (★★★☆☆☆☆☆)",
		"goal": 4,
		"words": STAGE3_WORDS,
		"decoy_mode": "lookalike"
	},
	4: {
		"name": "Voiced Dakuten",
		"difficulty": "ADVANCED (★★★★☆☆☆☆)",
		"goal": 4,
		"words": STAGE4_WORDS,
		"decoy_mode": "dakuten"
	},
	5: {
		"name": "Handakuten & Plosives",
		"difficulty": "EXPERT (★★★★★☆☆☆)",
		"goal": 4,
		"words": STAGE5_WORDS,
		"decoy_mode": "handakuten"
	},
	6: {
		"name": "Sokuon & Double Consonants",
		"difficulty": "HEROIC (★★★★★★☆☆)",
		"goal": 5,
		"words": STAGE6_WORDS,
		"decoy_mode": "sokuon"
	},
	7: {
		"name": "Advanced Compounds",
		"difficulty": "MASTER (★★★★★★★☆)",
		"goal": 5,
		"words": STAGE7_WORDS,
		"decoy_mode": "advanced"
	},
	8: {
		"name": "Grand Master Gauntlet",
		"difficulty": "GRANDMASTER (★★★★★★★★)",
		"goal": 6,
		"words": STAGE8_WORDS,
		"decoy_mode": "master"
	}
}

# Backwards compatibility alias
const STAGE_SETS = STAGE_DATA

