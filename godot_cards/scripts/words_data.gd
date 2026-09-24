class_name WordsData
extends RefCounted

const SETS_PER_STAGE: int = 3

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
	"が": "か", "ぎ": "き", "ぐ": "く", "げ": "け",# ==============================================================================
# STAGE 1: Basic Vowels (あ・い・う・え・お)
# ==============================================================================
const STAGE1_SET1_WORDS = [
	{"romaji": "AO", "meaning": "blue", "kana": ["あ", "お"]},
	{"romaji": "IE", "meaning": "house", "kana": ["い", "え"]},
	{"romaji": "UE", "meaning": "above", "kana": ["う", "え"]},
	{"romaji": "AI", "meaning": "love", "kana": ["あ", "い"]},
	{"romaji": "AKI", "meaning": "autumn", "kana": ["あ", "き"]},
	{"romaji": "UMI", "meaning": "sea", "kana": ["う", "み"]}
]

const STAGE1_SET2_WORDS = [
	{"romaji": "NEKO", "meaning": "cat", "kana": ["ね", "こ"]},
	{"romaji": "INU", "meaning": "dog", "kana": ["い", "ぬ"]},
	{"romaji": "SORA", "meaning": "sky", "kana": ["そ", "ら"]},
	{"romaji": "YAMA", "meaning": "mountain", "kana": ["や", "ま"]},
	{"romaji": "HANA", "meaning": "flower", "kana": ["は", "な"]},
	{"romaji": "KASA", "meaning": "umbrella", "kana": ["か", "さ"]}
]

const STAGE1_SET3_WORDS = [
	{"romaji": "KAME", "meaning": "turtle", "kana": ["か", "め"]},
	{"romaji": "TORI", "meaning": "bird", "kana": ["と", "り"]},
	{"romaji": "USHI", "meaning": "cow", "kana": ["う", "し"]},
	{"romaji": "FUYU", "meaning": "winter", "kana": ["ふ", "ゆ"]},
	{"romaji": "HARU", "meaning": "spring", "kana": ["は", "る"]},
	{"romaji": "NATSU", "meaning": "summer", "kana": ["な", "つ"]},
	{"romaji": "TSUKI", "meaning": "moon", "kana": ["つ", "き"]},
	{"romaji": "KAWA", "meaning": "river", "kana": ["か", "わ"]}
]

# ==============================================================================
# STAGE 2: Ka, Sa, Ta, Na Lines (か・さ・た・な行)
# ==============================================================================
const STAGE2_SET1_WORDS = [
	{"romaji": "SUSHI", "meaning": "sushi", "kana": ["す", "し"]},
	{"romaji": "TAKO", "meaning": "octopus", "kana": ["た", "こ"]},
	{"romaji": "SARU", "meaning": "monkey", "kana": ["さ", "る"]},
	{"romaji": "KUTSU", "meaning": "shoes", "kana": ["く", "つ"]},
	{"romaji": "SHIKA", "meaning": "deer", "kana": ["し", "か"]},
	{"romaji": "HACHI", "meaning": "bee", "kana": ["は", "ち"]}
]

const STAGE2_SET2_WORDS = [
	{"romaji": "SAKURA", "meaning": "cherry blossom", "kana": ["さ", "く", "ら"]},
	{"romaji": "KATANA", "meaning": "sword", "kana": ["か", "た", "な"]},
	{"romaji": "KARASU", "meaning": "crow", "kana": ["か", "ら", "す"]},
	{"romaji": "SEKAI", "meaning": "world", "kana": ["せ", "か", "い"]},
	{"romaji": "ASAHI", "meaning": "morning sun", "kana": ["あ", "さ", "ひ"]},
	{"romaji": "ATAMA", "meaning": "head", "kana": ["あ", "た", "ま"]}
]

const STAGE2_SET3_WORDS = [
	{"romaji": "KITSUNE", "meaning": "fox", "kana": ["き", "つ", "ね"]},
	{"romaji": "TANUKI", "meaning": "raccoon dog", "kana": ["た", "ぬ", "き"]},
	{"romaji": "KOKORO", "meaning": "heart / spirit", "kana": ["こ", "こ", "ろ"]},
	{"romaji": "KAERU", "meaning": "frog", "kana": ["か", "え", "る"]},
	{"romaji": "KIMONO", "meaning": "kimono", "kana": ["き", "も", "の"]}
]

# ==============================================================================
# STAGE 3: Expanded Core Syllabary (Gojuon Mastery)
# ==============================================================================
const STAGE3_SET1_WORDS = [
	{"romaji": "SAKANA", "meaning": "fish", "kana": ["さ", "か", "な"]},
	{"romaji": "KURUMA", "meaning": "car", "kana": ["く", "る", "ま"]},
	{"romaji": "YASAI", "meaning": "vegetable", "kana": ["や", "さ", "い"]},
	{"romaji": "MIKAN", "meaning": "orange", "kana": ["み", "か", "ん"]},
	{"romaji": "TAMAGO", "meaning": "egg", "kana": ["た", "ま", "ご"]}
]

const STAGE3_SET2_WORDS = [
	{"romaji": "KUSURI", "meaning": "medicine", "kana": ["く", "す", "り"]},
	{"romaji": "HIKARI", "meaning": "light", "kana": ["ひ", "か", "り"]},
	{"romaji": "TSUKIMI", "meaning": "moon viewing", "kana": ["つ", "き", "み"]},
	{"romaji": "MINATO", "meaning": "harbor", "kana": ["み", "な", "と"]},
	{"romaji": "HOTARU", "meaning": "firefly", "kana": ["ほ", "た", "る"]}
]

const STAGE3_SET3_WORDS = [
	{"romaji": "KUMOMA", "meaning": "cloud rift", "kana": ["く", "も", "ま"]},
	{"romaji": "SUZUME", "meaning": "sparrow", "kana": ["す", "ず", "め"]},
	{"romaji": "KAMOME", "meaning": "seagull", "kana": ["か", "も", "め"]},
	{"romaji": "KARASU", "meaning": "crow", "kana": ["か", "ら", "す"]},
	{"romaji": "KITSUNE", "meaning": "fox", "kana": ["き", "つ", "ね"]}
]

# ==============================================================================
# STAGE 4: Voiced Consonants (Dakuten が, ざ, だ, ば)
# ==============================================================================
const STAGE4_SET1_WORDS = [
	{"romaji": "MIZU", "meaning": "water", "kana": ["み", "ず"]},
	{"romaji": "KAZE", "meaning": "wind", "kana": ["か", "ぜ"]},
	{"romaji": "CHIZU", "meaning": "map", "kana": ["ち", "ず"]},
	{"romaji": "KAGI", "meaning": "key", "kana": ["か", "ぎ"]},
	{"romaji": "EBI", "meaning": "shrimp", "kana": ["え", "び"]},
	{"romaji": "SUZU", "meaning": "bell", "kana": ["す", "ず"]}
]

const STAGE4_SET2_WORDS = [
	{"romaji": "GOHAN", "meaning": "meal / rice", "kana": ["ご", "は", "ん"]},
	{"romaji": "RINGO", "meaning": "apple", "kana": ["り", "ん", "ご"]},
	{"romaji": "MEGANE", "meaning": "glasses", "kana": ["め", "が", "ね"]},
	{"romaji": "BUDOU", "meaning": "grapes", "kana": ["ぶ", "ど", "う"]},
	{"romaji": "ZUBON", "meaning": "trousers", "kana": ["ず", "ぼ", "ん"]},
	{"romaji": "KABUTO", "meaning": "helmet", "kana": ["か", "ぶ", "と"]}
]

const STAGE4_SET3_WORDS = [
	{"romaji": "TOMODACHI", "meaning": "friend", "kana": ["と", "も", "だ", "ち"]},
	{"romaji": "TABEMONO", "meaning": "food", "kana": ["た", "べ", "も", "の"]},
	{"romaji": "INOSHISHI", "meaning": "wild boar", "kana": ["い", "の", "し", "し"]},
	{"romaji": "DENWA", "meaning": "telephone", "kana": ["で", "ん", "わ"]}
]

# ==============================================================================
# STAGE 5: Handakuten & Nasal 'N' (ぱ, ぴ, ぷ, ぺ, ぽ, ん)
# ==============================================================================
const STAGE5_SET1_WORDS = [
	{"romaji": "PAN", "meaning": "bread", "kana": ["ぱ", "ん"]},
	{"romaji": "SANPO", "meaning": "walk / stroll", "kana": ["さ", "ん", "ぽ"]},
	{"romaji": "PIANO", "meaning": "piano", "kana": ["ぴ", "あ", "の"]},
	{"romaji": "KIPPU", "meaning": "ticket", "kana": ["き", "っ", "ぷ"]}
]

const STAGE5_SET2_WORDS = [
	{"romaji": "ENPITSU", "meaning": "pencil", "kana": ["え", "ん", "ぴ", "つ"]},
	{"romaji": "BENTOU", "meaning": "bento box", "kana": ["べ", "ん", "と", "う"]},
	{"romaji": "TENPURA", "meaning": "tempura", "kana": ["て", "ん", "ぷ", "ら"]},
	{"romaji": "SHINBUN", "meaning": "newspaper", "kana": ["し", "ん", "ぶ", "ん"]}
]

const STAGE5_SET3_WORDS = [
	{"romaji": "SUPUUN", "meaning": "spoon", "kana": ["す", "ぷ", "ー", "ん"]},
	{"romaji": "KAMISAMA", "meaning": "deity", "kana": ["か", "み", "さ", "ま"]},
	{"romaji": "KAPPA", "meaning": "river imp", "kana": ["か", "っ", "ぱ"]},
	{"romaji": "KIPPU", "meaning": "ticket", "kana": ["き", "っ", "ぷ"]}
]

# ==============================================================================
# STAGE 6: Sokuon (Small つ) & Double Consonants
# ==============================================================================
const STAGE6_SET1_WORDS = [
	{"romaji": "KIPPU", "meaning": "ticket", "kana": ["き", "っ", "ぷ"]},
	{"romaji": "KITTE", "meaning": "stamp", "kana": ["き", "っ", "て"]},
	{"romaji": "NIKKI", "meaning": "diary", "kana": ["に", "っ", "き"]},
	{"romaji": "KOPPU", "meaning": "glass / cup", "kana": ["こ", "っ", "ぷ"]},
	{"romaji": "OTTO", "meaning": "husband", "kana": ["お", "っ", "と"]}
]

const STAGE6_SET2_WORDS = [
	{"romaji": "GAKKOU", "meaning": "school", "kana": ["が", "っ", "こ", "う"]},
	{"romaji": "ZASSHI", "meaning": "magazine", "kana": ["ざ", "っ", "し"]},
	{"romaji": "SHIPPO", "meaning": "tail", "kana": ["し", "っ", "ぽ"]},
	{"romaji": "ISSHO", "meaning": "together", "kana": ["い", "っ", "し", "ょ"]}
]

const STAGE6_SET3_WORDS = [
	{"romaji": "KEKKON", "meaning": "marriage", "kana": ["け", "っ", "こ", "ん"]},
	{"romaji": "HAPPOU", "meaning": "all directions", "kana": ["は", "っ", "ぽ", "う"]},
	{"romaji": "CHIKATETSU", "meaning": "subway", "kana": ["ち", "か", "て", "つ"]}
]

# ==============================================================================
# STAGE 7: Advanced Compounds & Cultural Vocabulary
# ==============================================================================
const STAGE7_SET1_WORDS = [
	{"romaji": "OMATSURI", "meaning": "festival", "kana": ["お", "ま", "つ", "り"]},
	{"romaji": "YASASHISA", "meaning": "kindness", "kana": ["や", "さ", "し", "さ"]},
	{"romaji": "HATARAKI", "meaning": "work / function", "kana": ["は", "た", "ら", "き"]},
	{"romaji": "ASAYAKE", "meaning": "morning glow", "kana": ["あ", "さ", "や", "け"]},
	{"romaji": "HOSHIZORA", "meaning": "starry sky", "kana": ["ほ", "し", "ぞ", "ら"]}
]

const STAGE7_SET2_WORDS = [
	{"romaji": "FUJISAN", "meaning": "Mount Fuji", "kana": ["ふ", "じ", "さ", "ん"]},
	{"romaji": "NAMIOTO", "meaning": "wave sound", "kana": ["な", "み", "お", "と"]},
	{"romaji": "ARIGATOU", "meaning": "thank you", "kana": ["あ", "り", "が", "と", "う"]},
	{"romaji": "SAYOUNARA", "meaning": "goodbye", "kana": ["さ", "よ", "う", "な", "ら"]}
]

const STAGE7_SET3_WORDS = [
	{"romaji": "SUBARASHII", "meaning": "magnificent", "kana": ["す", "ば", "ら", "し", "い"]},
	{"romaji": "ITADAKIMASU", "meaning": "bon appetit", "kana": ["い", "た", "だ", "き", "ま", "す"]},
	{"romaji": "DAIKOUKAI", "meaning": "great voyage", "kana": ["だ", "い", "こ", "う", "か", "い"]}
]

# ==============================================================================
# STAGE 8: Grand Master Gauntlet
# ==============================================================================
const STAGE8_SET1_WORDS = [
	{"romaji": "NIHONGO", "meaning": "Japanese language", "kana": ["に", "ほ", "ん", "ご"]},
	{"romaji": "SAKURA", "meaning": "cherry blossom", "kana": ["さ", "く", "ら"]},
	{"romaji": "HIKARI", "meaning": "light", "kana": ["ひ", "か", "り"]},
	{"romaji": "KOKORO", "meaning": "heart / spirit", "kana": ["こ", "こ", "ろ"]},
	{"romaji": "SANPO", "meaning": "walk / stroll", "kana": ["さ", "ん", "ぽ"]}
]

const STAGE8_SET2_WORDS = [
	{"romaji": "SHINKANSEN", "meaning": "bullet train", "kana": ["し", "ん", "か", "ん", "せ", "ん"]},
	{"romaji": "TOMODACHI", "meaning": "friend", "kana": ["と", "も", "だ", "ち"]},
	{"romaji": "GAKKOU", "meaning": "school", "kana": ["が", "っ", "こ", "う"]},
	{"romaji": "ENPITSU", "meaning": "pencil", "kana": ["え", "ん", "ぴ", "つ"]},
	{"romaji": "BENTOU", "meaning": "bento box", "kana": ["べ", "ん", "と", "う"]}
]

const STAGE8_SET3_WORDS = [
	{"romaji": "ARIGATOU", "meaning": "thank you", "kana": ["あ", "り", "が", "と", "う"]},
	{"romaji": "SUBARASHII", "meaning": "magnificent", "kana": ["す", "ば", "ら", "し", "い"]},
	{"romaji": "ITADAKIMASU", "meaning": "gratitude", "kana": ["い", "た", "だ", "き", "ま", "す"]},
	{"romaji": "DAIKOUKAI", "meaning": "great voyage", "kana": ["だ", "い", "こ", "う", "か", "い"]},
	{"romaji": "INOSHISHI", "meaning": "wild boar", "kana": ["い", "の", "し", "し"]}
]

# ==============================================================================
# STAGE SPECIFICATIONS & SET CURRICULUM
# ==============================================================================
const STAGE_DATA = {
	1: {
		"name": "Basic Vowels",
		"difficulty": "BEGINNER (★☆☆☆☆☆☆☆)",
		"sets": {
			1: {"name": "Set 1: Pure Vowels", "goal": 3, "words": STAGE1_SET1_WORDS, "decoy_mode": "random"},
			2: {"name": "Set 2: Consonant Basics", "goal": 3, "words": STAGE1_SET2_WORDS, "decoy_mode": "similar"},
			3: {"name": "Set 3: Everyday Nature", "goal": 3, "words": STAGE1_SET3_WORDS, "decoy_mode": "lookalike"}
		}
	},
	2: {
		"name": "Ka, Sa, Ta Combat",
		"difficulty": "NOVICE (★★☆☆☆☆☆☆)",
		"sets": {
			1: {"name": "Set 1: Short Consonants", "goal": 3, "words": STAGE2_SET1_WORDS, "decoy_mode": "random"},
			2: {"name": "Set 2: Core Consonant Lines", "goal": 3, "words": STAGE2_SET2_WORDS, "decoy_mode": "similar"},
			3: {"name": "Set 3: Fluid Syllables", "goal": 3, "words": STAGE2_SET3_WORDS, "decoy_mode": "lookalike"}
		}
	},
	3: {
		"name": "Expanded Syllabary",
		"difficulty": "INTERMEDIATE (★★★☆☆☆☆☆)",
		"sets": {
			1: {"name": "Set 1: Food & Travel", "goal": 3, "words": STAGE3_SET1_WORDS, "decoy_mode": "similar"},
			2: {"name": "Set 2: Town & Everyday Life", "goal": 3, "words": STAGE3_SET2_WORDS, "decoy_mode": "lookalike"},
			3: {"name": "Set 3: Wildlife Lookalikes", "goal": 3, "words": STAGE3_SET3_WORDS, "decoy_mode": "lookalike"}
		}
	},
	4: {
		"name": "Voiced Dakuten",
		"difficulty": "ADVANCED (★★★★☆☆☆☆)",
		"sets": {
			1: {"name": "Set 1: 2-Kana Dakuten", "goal": 3, "words": STAGE4_SET1_WORDS, "decoy_mode": "dakuten"},
			2: {"name": "Set 2: 3-Kana Dakuten", "goal": 3, "words": STAGE4_SET2_WORDS, "decoy_mode": "dakuten"},
			3: {"name": "Set 3: Multi-Voiced Compounds", "goal": 3, "words": STAGE4_SET3_WORDS, "decoy_mode": "dakuten"}
		}
	},
	5: {
		"name": "Handakuten & Plosives",
		"difficulty": "EXPERT (★★★★★☆☆☆)",
		"sets": {
			1: {"name": "Set 1: 2-Kana Handakuten", "goal": 3, "words": STAGE5_SET1_WORDS, "decoy_mode": "handakuten"},
			2: {"name": "Set 2: 3-Kana Bento & School", "goal": 3, "words": STAGE5_SET2_WORDS, "decoy_mode": "handakuten"},
			3: {"name": "Set 3: Long Vowels & Plosives", "goal": 3, "words": STAGE5_SET3_WORDS, "decoy_mode": "handakuten"}
		}
	},
	6: {
		"name": "Sokuon & Double Consonants",
		"difficulty": "HEROIC (★★★★★★☆☆)",
		"sets": {
			1: {"name": "Set 1: Everyday Sokuon", "goal": 3, "words": STAGE6_SET1_WORDS, "decoy_mode": "sokuon"},
			2: {"name": "Set 2: School & Reading Sokuon", "goal": 3, "words": STAGE6_SET2_WORDS, "decoy_mode": "sokuon"},
			3: {"name": "Set 3: Advanced Double Consonants", "goal": 3, "words": STAGE6_SET3_WORDS, "decoy_mode": "sokuon"}
		}
	},
	7: {
		"name": "Advanced Compounds",
		"difficulty": "MASTER (★★★★★★★☆)",
		"sets": {
			1: {"name": "Set 1: Cultural Vocabulary", "goal": 3, "words": STAGE7_SET1_WORDS, "decoy_mode": "advanced"},
			2: {"name": "Set 2: Expressions & Greetings", "goal": 3, "words": STAGE7_SET2_WORDS, "decoy_mode": "advanced"},
			3: {"name": "Set 3: Master Compounds", "goal": 3, "words": STAGE7_SET3_WORDS, "decoy_mode": "advanced"}
		}
	},
	8: {
		"name": "Grand Master Gauntlet",
		"difficulty": "GRANDMASTER (★★★★★★★★)",
		"sets": {
			1: {"name": "Set 1: Iconic Japanese Mastery", "goal": 3, "words": STAGE8_SET1_WORDS, "decoy_mode": "master"},
			2: {"name": "Set 2: Sokuon & Dakuten Gauntlet", "goal": 3, "words": STAGE8_SET2_WORDS, "decoy_mode": "master"},
			3: {"name": "Set 3: Ultimate Japanese Expressions", "goal": 4, "words": STAGE8_SET3_WORDS, "decoy_mode": "master"}
		}
	}
}

# Backwards compatibility alias
const STAGE_SETS = STAGE_DATA

static func get_stage_set_data(stage_idx: int, set_idx: int) -> Dictionary:
	var s_data = STAGE_DATA.get(stage_idx, STAGE_DATA[1])
	var sets_map: Dictionary = s_data.get("sets", {})
	if sets_map.has(set_idx):
		return sets_map[set_idx]
	return sets_map.get(1, {"name": "Set 1", "goal": 3, "words": STAGE1_SET1_WORDS, "decoy_mode": "random"})


