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
	"が": "か", "ぎ": "き", "ぐ": "く", "げ": "け", "ご": "こ",
	"ば": "は", "び": "ひ", "ぶ": "ふ", "べ": "へ", "ぼ": "ほ",
	"ぱ": "ば", "ぴ": "び", "ぷ": "ぶ", "ぺ": "べ", "ぽ": "ぼ"
}

const KATAKANA_GOJUON_POOL = [
	"ア", "イ", "ウ", "エ", "オ",
	"カ", "キ", "ク", "ケ", "コ",
	"サ", "シ", "ス", "セ", "ソ",
	"タ", "チ", "ツ", "テ", "ト",
	"ナ", "ニ", "ヌ", "ネ", "ノ",
	"ハ", "ヒ", "フ", "ヘ", "ホ",
	"マ", "ミ", "ム", "メ", "モ",
	"ヤ", "ユ", "ヨ",
	"ラ", "リ", "ル", "レ", "ロ",
	"ワ", "ヲ", "ン"
]

const KATAKANA_DAKUTEN_POOL = [
	"ガ", "ギ", "グ", "ゲ", "ゴ",
	"ザ", "ジ", "ズ", "ゼ", "ゾ",
	"ダ", "ヂ", "ヅ", "デ", "ド",
	"バ", "ビ", "ブ", "ベ", "ボ"
]

const KATAKANA_HANDAKUTEN_POOL = [
	"パ", "ピ", "プ", "ペ", "ポ"
]

const KATAKANA_SOKUON_POOL = [
	"ッ", "ャ", "ュ", "ョ", "ー"
]

const KATAKANA_CONFUSABLE_MAP = {
	"シ": "ツ", "ツ": "シ",
	"ソ": "ン", "ン": "ソ",
	"ノ": "メ", "メ": "ノ",
	"ク": "ワ", "ワ": "ク",
	"コ": "ユ", "ユ": "コ",
	"チ": "テ", "テ": "チ",
	"ス": "ヌ", "ヌ": "ス",
	"タ": "ク",
	"ア": "マ", "マ": "ア",
	"ロ": "コ",
	"ガ": "カ", "ギ": "キ", "グ": "ク", "ゲ": "ケ", "ゴ": "コ",
	"バ": "ハ", "ビ": "ヒ", "ブ": "フ", "ベ": "ヘ", "ボ": "ホ",
	"パ": "バ", "ピ": "ビ", "プ": "ブ", "ペ": "ベ", "ポ": "ボ"
}

# ==============================================================================
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


# ==============================================================================
# KATAKANA STAGE 1: Basic Vowels & Short Loanwords (ア・イ・ウ・エ・オ)
# ==============================================================================
const KATAKANA_STAGE1_SET1_WORDS = [
	{"romaji": "DOA", "meaning": "door", "kana": ["ド", "ア"]},
	{"romaji": "EA", "meaning": "air", "kana": ["エ", "ア"]},
	{"romaji": "INU", "meaning": "dog", "kana": ["イ", "ヌ"]},
	{"romaji": "AISU", "meaning": "ice cream", "kana": ["ア", "イ", "ス"]},
	{"romaji": "AME", "meaning": "candy", "kana": ["ア", "メ"]},
	{"romaji": "IE", "meaning": "house", "kana": ["イ", "エ"]}
]

const KATAKANA_STAGE1_SET2_WORDS = [
	{"romaji": "GASU", "meaning": "gas", "kana": ["ガ", "ス"]},
	{"romaji": "MEMO", "meaning": "memo", "kana": ["メ", "モ"]},
	{"romaji": "BASU", "meaning": "bus", "kana": ["バ", "ス"]},
	{"romaji": "PIRU", "meaning": "pill", "kana": ["ピ", "ル"]},
	{"romaji": "MONO", "meaning": "mono sound", "kana": ["モ", "ノ"]},
	{"romaji": "RISU", "meaning": "squirrel", "kana": ["リ", "ス"]}
]

const KATAKANA_STAGE1_SET3_WORDS = [
	{"romaji": "KASA", "meaning": "umbrella", "kana": ["カ", "サ"]},
	{"romaji": "TORI", "meaning": "bird", "kana": ["ト", "リ"]},
	{"romaji": "NEKO", "meaning": "cat", "kana": ["ネ", "コ"]},
	{"romaji": "SORA", "meaning": "sky", "kana": ["ソ", "ラ"]},
	{"romaji": "YAMA", "meaning": "mountain", "kana": ["ヤ", "マ"]},
	{"romaji": "HANA", "meaning": "flower", "kana": ["ハ", "ナ"]}
]

# ==============================================================================
# KATAKANA STAGE 2: Ka, Sa, Ta, Na Lines (カ・サ・タ・ナ行)
# ==============================================================================
const KATAKANA_STAGE2_SET1_WORDS = [
	{"romaji": "KASA", "meaning": "umbrella", "kana": ["カ", "サ"]},
	{"romaji": "TAKO", "meaning": "octopus", "kana": ["タ", "コ"]},
	{"romaji": "KAME", "meaning": "turtle", "kana": ["カ", "メ"]},
	{"romaji": "SHIKA", "meaning": "deer", "kana": ["シ", "カ"]},
	{"romaji": "KANI", "meaning": "crab", "kana": ["カ", "ニ"]},
	{"romaji": "NIKO", "meaning": "smile", "kana": ["ニ", "コ"]}
]

const KATAKANA_STAGE2_SET2_WORDS = [
	{"romaji": "KAMERA", "meaning": "camera", "kana": ["カ", "メ", "ラ"]},
	{"romaji": "TAKUSHII", "meaning": "taxi", "kana": ["タ", "ク", "シ", "ー"]},
	{"romaji": "SAKANA", "meaning": "fish", "kana": ["サ", "カ", "ナ"]},
	{"romaji": "KATANA", "meaning": "sword", "kana": ["カ", "タ", "ナ"]},
	{"romaji": "KINOKO", "meaning": "mushroom", "kana": ["キ", "ノ", "コ"]},
	{"romaji": "SUZUME", "meaning": "sparrow", "kana": ["ス", "ズ", "メ"]}
]

const KATAKANA_STAGE2_SET3_WORDS = [
	{"romaji": "TOMATO", "meaning": "tomato", "kana": ["ト", "マ", "ト"]},
	{"romaji": "BANANA", "meaning": "banana", "kana": ["バ", "ナ", "ナ"]},
	{"romaji": "KITSUNE", "meaning": "fox", "kana": ["キ", "ツ", "ネ"]},
	{"romaji": "TANUKI", "meaning": "raccoon dog", "kana": ["タ", "ヌ", "キ"]},
	{"romaji": "KARASU", "meaning": "crow", "kana": ["カ", "ラ", "ス"]},
	{"romaji": "HOTERU", "meaning": "hotel", "kana": ["ホ", "テ", "ル"]}
]

# ==============================================================================
# KATAKANA STAGE 3: Lookalikes & Traps (類似文字：シ/ツ・ソ/ン・ノ/メ)
# ==============================================================================
const KATAKANA_STAGE3_SET1_WORDS = [
	{"romaji": "SHATSU", "meaning": "shirt", "kana": ["シ", "ャ", "ツ"]},
	{"romaji": "TSUNA", "meaning": "tuna", "kana": ["ツ", "ナ"]},
	{"romaji": "SHIIRU", "meaning": "sticker", "kana": ["シ", "ー", "ル"]},
	{"romaji": "TSUAA", "meaning": "tour", "kana": ["ツ", "ア", "ー"]},
	{"romaji": "SHISUTEMU", "meaning": "system", "kana": ["シ", "ス", "テ", "ム"]},
	{"romaji": "TSUURU", "meaning": "tool", "kana": ["ツ", "ー", "ル"]}
]

const KATAKANA_STAGE3_SET2_WORDS = [
	{"romaji": "SOOSU", "meaning": "sauce", "kana": ["ソ", "ー", "ス"]},
	{"romaji": "PAN", "meaning": "bread", "kana": ["パ", "ン"]},
	{"romaji": "SOFA", "meaning": "sofa", "kana": ["ソ", "フ", "ァ"]},
	{"romaji": "SANDO", "meaning": "sandwich", "kana": ["サ", "ン", "ド"]},
	{"romaji": "SOKUSU", "meaning": "socks", "kana": ["ソ", "ッ", "ク", "ス"]},
	{"romaji": "DANSU", "meaning": "dance", "kana": ["ダ", "ン", "ス"]}
]

const KATAKANA_STAGE3_SET3_WORDS = [
	{"romaji": "MERON", "meaning": "melon", "kana": ["メ", "ロ", "ン"]},
	{"romaji": "NOOTO", "meaning": "notebook", "kana": ["ノ", "ー", "ト"]},
	{"romaji": "WAFURU", "meaning": "waffle", "kana": ["ワ", "ッ", "フ", "ル"]},
	{"romaji": "KURABU", "meaning": "club", "kana": ["ク", "ラ", "ブ"]},
	{"romaji": "METORU", "meaning": "meter", "kana": ["メ", "ー", "ト", "ル"]},
	{"romaji": "WAIN", "meaning": "wine", "kana": ["ワ", "イ", "ン"]}
]

# ==============================================================================
# KATAKANA STAGE 4: Voiced Consonants (濁音：ガ・ザ・ダ・バ・ゴ)
# ==============================================================================
const KATAKANA_STAGE4_SET1_WORDS = [
	{"romaji": "GASU", "meaning": "gas", "kana": ["ガ", "ス"]},
	{"romaji": "ZERO", "meaning": "zero", "kana": ["ゼ", "ロ"]},
	{"romaji": "BASU", "meaning": "bus", "kana": ["バ", "ス"]},
	{"romaji": "GOMU", "meaning": "rubber", "kana": ["ゴ", "ム"]},
	{"romaji": "DOGGU", "meaning": "dog", "kana": ["ド", "ッ", "グ"]},
	{"romaji": "GOMI", "meaning": "trash", "kana": ["ゴ", "ミ"]}
]

const KATAKANA_STAGE4_SET2_WORDS = [
	{"romaji": "BIDEO", "meaning": "video", "kana": ["ビ", "デ", "オ"]},
	{"romaji": "DORAMU", "meaning": "drum", "kana": ["ド", "ラ", "ム"]},
	{"romaji": "GITAA", "meaning": "guitar", "kana": ["ギ", "タ", "ー"]},
	{"romaji": "BUDOU", "meaning": "grape", "kana": ["ブ", "ド", "ウ"]},
	{"romaji": "BERUTO", "meaning": "belt", "kana": ["ベ", "ル", "ト"]},
	{"romaji": "GORUFU", "meaning": "golf", "kana": ["ゴ", "ル", "フ"]}
]

const KATAKANA_STAGE4_SET3_WORDS = [
	{"romaji": "GURASU", "meaning": "glass", "kana": ["グ", "ラ", "ス"]},
	{"romaji": "DAIYA", "meaning": "diamond", "kana": ["ダ", "イ", "ヤ"]},
	{"romaji": "DORAIBAA", "meaning": "driver", "kana": ["ド", "ラ", "イ", "バ", "ー"]},
	{"romaji": "BAIKU", "meaning": "motorbike", "kana": ["バ", "イ", "ク"]},
	{"romaji": "DANSU", "meaning": "dance", "kana": ["ダ", "ン", "ス"]}
]

# ==============================================================================
# KATAKANA STAGE 5: Handakuten & Long Vowels (半濁音・長音「ー」)
# ==============================================================================
const KATAKANA_STAGE5_SET1_WORDS = [
	{"romaji": "PAN", "meaning": "bread", "kana": ["パ", "ン"]},
	{"romaji": "PIANO", "meaning": "piano", "kana": ["ピ", "ア", "ノ"]},
	{"romaji": "PURA", "meaning": "plastic", "kana": ["プ", "ラ"]},
	{"romaji": "PEN", "meaning": "pen", "kana": ["ペ", "ン"]},
	{"romaji": "POSUTO", "meaning": "mailbox", "kana": ["ポ", "ス", "ト"]},
	{"romaji": "POORU", "meaning": "pole", "kana": ["ポ", "ー", "ル"]}
]

const KATAKANA_STAGE5_SET2_WORDS = [
	{"romaji": "KOOHII", "meaning": "coffee", "kana": ["コ", "ー", "ヒ", "ー"]},
	{"romaji": "KEEKI", "meaning": "cake", "kana": ["ケ", "ー", "キ"]},
	{"romaji": "CHIIZU", "meaning": "cheese", "kana": ["チ", "ー", "ズ"]},
	{"romaji": "BATAA", "meaning": "butter", "kana": ["バ", "タ", "ー"]},
	{"romaji": "KOORA", "meaning": "cola", "kana": ["コ", "ー", "ラ"]},
	{"romaji": "SUUPU", "meaning": "soup", "kana": ["ス", "ー", "プ"]}
]

const KATAKANA_STAGE5_SET3_WORDS = [
	{"romaji": "SUKII", "meaning": "skiing", "kana": ["ス", "キ", "ー"]},
	{"romaji": "SUKEETO", "meaning": "skating", "kana": ["ス", "ケ", "ー", "ト"]},
	{"romaji": "POOSUTAA", "meaning": "poster", "kana": ["ポ", "ス", "タ", "ー"]},
	{"romaji": "SUPOOTSU", "meaning": "sports", "kana": ["ス", "ポ", "ー", "ツ"]},
	{"romaji": "BOORU", "meaning": "ball", "kana": ["ボ", "ー", "ル"]}
]

# ==============================================================================
# KATAKANA STAGE 6: Sokuon & Double Consonants (促音「ッ」)
# ==============================================================================
const KATAKANA_STAGE6_SET1_WORDS = [
	{"romaji": "KOPPU", "meaning": "cup", "kana": ["コ", "ッ", "プ"]},
	{"romaji": "BEDDO", "meaning": "bed", "kana": ["ベ", "ッ", "ド"]},
	{"romaji": "KIPPU", "meaning": "ticket", "kana": ["キ", "ッ", "プ"]},
	{"romaji": "BAGGU", "meaning": "bag", "kana": ["バ", "ッ", "グ"]},
	{"romaji": "PETTO", "meaning": "pet", "kana": ["ペ", "ッ", "ト"]},
	{"romaji": "KITTE", "meaning": "stamp", "kana": ["キ", "ッ", "テ"]}
]

const KATAKANA_STAGE6_SET2_WORDS = [
	{"romaji": "SAKKAA", "meaning": "soccer", "kana": ["サ", "ッ", "カ", "ー"]},
	{"romaji": "ROKETTO", "meaning": "rocket", "kana": ["ロ", "ケ", "ッ", "ト"]},
	{"romaji": "POKETTO", "meaning": "pocket", "kana": ["ポ", "ケ", "ッ", "ト"]},
	{"romaji": "TISSHU", "meaning": "tissue", "kana": ["テ", "ィ", "ッ", "シ", "ュ"]},
	{"romaji": "NETTO", "meaning": "internet", "kana": ["ネ", "ッ", "ト"]},
	{"romaji": "CHIKETTO", "meaning": "ticket", "kana": ["チ", "ケ", "ッ", "ト"]}
]

const KATAKANA_STAGE6_SET3_WORDS = [
	{"romaji": "SUITCHI", "meaning": "switch", "kana": ["ス", "イ", "ッ", "チ"]},
	{"romaji": "SANDARU", "meaning": "sandals", "kana": ["サ", "ン", "ダ", "ル"]},
	{"romaji": "KITCHIN", "meaning": "kitchen", "kana": ["キ", "ッ", "チ", "ン"]},
	{"romaji": "PASOKON", "meaning": "computer", "kana": ["パ", "ソ", "コ", "ン"]},
	{"romaji": "MATCHI", "meaning": "match", "kana": ["マ", "ッ", "チ"]}
]

# ==============================================================================
# KATAKANA STAGE 7: Foreign Sounds & Small Yōn (外来音：ファ/フィ/シェ/チェ/ティ)
# ==============================================================================
const KATAKANA_STAGE7_SET1_WORDS = [
	{"romaji": "KAFE", "meaning": "cafe", "kana": ["カ", "フ", "ェ"]},
	{"romaji": "FIRUMU", "meaning": "film", "kana": ["フ", "ィ", "ル", "ム"]},
	{"romaji": "FAN", "meaning": "fan", "kana": ["フ", "ァ", "ン"]},
	{"romaji": "FOOKU", "meaning": "fork", "kana": ["フ", "ォ", "ー", "ク"]},
	{"romaji": "SHEFU", "meaning": "chef", "kana": ["シ", "ェ", "フ"]},
	{"romaji": "FAITAA", "meaning": "fighter", "kana": ["フ", "ァ", "イ", "タ", "ー"]}
]

const KATAKANA_STAGE7_SET2_WORDS = [
	{"romaji": "PAATII", "meaning": "party", "kana": ["パ", "ー", "テ", "ィ", "ー"]},
	{"romaji": "DISUKO", "meaning": "disco", "kana": ["デ", "ィ", "ス", "コ"]},
	{"romaji": "CHOKO", "meaning": "chocolate", "kana": ["チ", "ョ", "コ"]},
	{"romaji": "JUUSU", "meaning": "juice", "kana": ["ジ", "ュ", "ー", "ス"]},
	{"romaji": "SHATSU", "meaning": "shirt", "kana": ["シ", "ャ", "ツ"]},
	{"romaji": "CHERII", "meaning": "cherry", "kana": ["チ", "ェ", "リ", "ー"]}
]

const KATAKANA_STAGE7_SET3_WORDS = [
	{"romaji": "MENYUU", "meaning": "menu", "kana": ["メ", "ニ", "ュ", "ー"]},
	{"romaji": "DYUETTO", "meaning": "duet", "kana": ["デ", "ュ", "エ", "ッ", "ト"]},
	{"romaji": "WINDOU", "meaning": "window", "kana": ["ウ", "ィ", "ン", "ド", "ウ"]},
	{"romaji": "SANDOITCHI", "meaning": "sandwich", "kana": ["サ", "ン", "ド", "イ", "ッ", "チ"]},
	{"romaji": "CHUURIPPU", "meaning": "tulip", "kana": ["チ", "ュ", "ー", "リ", "ッ", "プ"]}
]

# ==============================================================================
# KATAKANA STAGE 8: Grand Master Gauntlet (免許皆伝・最終試練)
# ==============================================================================
const KATAKANA_STAGE8_SET1_WORDS = [
	{"romaji": "HAMBAAGAA", "meaning": "hamburger", "kana": ["ハ", "ン", "バ", "ー", "ガ", "ー"]},
	{"romaji": "RESUTORAN", "meaning": "restaurant", "kana": ["レ", "ス", "ト", "ラ", "ン"]},
	{"romaji": "PASUPOOTO", "meaning": "passport", "kana": ["パ", "ス", "ポ", "ー", "ト"]},
	{"romaji": "ROBOTTO", "meaning": "robot", "kana": ["ロ", "ボ", "ッ", "ト"]},
	{"romaji": "SUKEETO", "meaning": "skating", "kana": ["ス", "ケ", "ー", "ト"]}
]

const KATAKANA_STAGE8_SET2_WORDS = [
	{"romaji": "EREBEETAA", "meaning": "elevator", "kana": ["エ", "レ", "ベ", "ー", "タ", "ー"]},
	{"romaji": "SUPAGETTI", "meaning": "spaghetti", "kana": ["ス", "パ", "ゲ", "ッ", "テ", "ィ"]},
	{"romaji": "DESUKU", "meaning": "desk", "kana": ["デ", "ス", "ク"]},
	{"romaji": "TAKUSHII", "meaning": "taxi", "kana": ["タ", "ク", "シ", "ー"]},
	{"romaji": "GITAASUTO", "meaning": "guitarist", "kana": ["ギ", "タ", "リ", "ス", "ト"]}
]

const KATAKANA_STAGE8_SET3_WORDS = [
	{"romaji": "TEEMAPAAKU", "meaning": "theme park", "kana": ["テ", "ー", "マ", "パ", "ー", "ク"]},
	{"romaji": "EAKON", "meaning": "air conditioner", "kana": ["エ", "ア", "コ", "ン"]},
	{"romaji": "KONBINI", "meaning": "convenience store", "kana": ["コ", "ン", "ビ", "ニ"]},
	{"romaji": "CHOKOREETO", "meaning": "chocolate", "kana": ["チ", "ョ", "コ", "レ", "ー", "ト"]},
	{"romaji": "PURORASU", "meaning": "pro wrestler", "kana": ["プ", "ロ", "レ", "ス"]}
]

# ==============================================================================
# KATAKANA STAGE SPECIFICATIONS & SET CURRICULUM
# ==============================================================================
const KATAKANA_STAGE_DATA = {
	1: {
		"name": "Basic Loanwords",
		"difficulty": "BEGINNER (★☆☆☆☆☆☆☆)",
		"sets": {
			1: {"name": "Set 1: Pure Vowels", "goal": 3, "words": KATAKANA_STAGE1_SET1_WORDS, "decoy_mode": "random"},
			2: {"name": "Set 2: Everyday Basics", "goal": 3, "words": KATAKANA_STAGE1_SET2_WORDS, "decoy_mode": "similar"},
			3: {"name": "Set 3: Living & Nature", "goal": 3, "words": KATAKANA_STAGE1_SET3_WORDS, "decoy_mode": "lookalike"}
		}
	},
	2: {
		"name": "Ka, Sa, Ta Syllables",
		"difficulty": "NOVICE (★★☆☆☆☆☆☆)",
		"sets": {
			1: {"name": "Set 1: Short Consonants", "goal": 3, "words": KATAKANA_STAGE2_SET1_WORDS, "decoy_mode": "random"},
			2: {"name": "Set 2: Core Consonant Lines", "goal": 3, "words": KATAKANA_STAGE2_SET2_WORDS, "decoy_mode": "similar"},
			3: {"name": "Set 3: Fluid Syllables", "goal": 3, "words": KATAKANA_STAGE2_SET3_WORDS, "decoy_mode": "lookalike"}
		}
	},
	3: {
		"name": "Shi/Tsu & So/N Traps",
		"difficulty": "INTERMEDIATE (★★★☆☆☆☆☆)",
		"sets": {
			1: {"name": "Set 1: Shi vs Tsu Duals", "goal": 3, "words": KATAKANA_STAGE3_SET1_WORDS, "decoy_mode": "lookalike"},
			2: {"name": "Set 2: So vs N Traps", "goal": 3, "words": KATAKANA_STAGE3_SET2_WORDS, "decoy_mode": "lookalike"},
			3: {"name": "Set 3: No vs Me Lookalikes", "goal": 3, "words": KATAKANA_STAGE3_SET3_WORDS, "decoy_mode": "lookalike"}
		}
	},
	4: {
		"name": "Voiced Dakuten",
		"difficulty": "ADVANCED (★★★★☆☆☆☆)",
		"sets": {
			1: {"name": "Set 1: 2-Kana Dakuten", "goal": 3, "words": KATAKANA_STAGE4_SET1_WORDS, "decoy_mode": "dakuten"},
			2: {"name": "Set 2: 3-Kana Dakuten", "goal": 3, "words": KATAKANA_STAGE4_SET2_WORDS, "decoy_mode": "dakuten"},
			3: {"name": "Set 3: Multi-Voiced Compounds", "goal": 3, "words": KATAKANA_STAGE4_SET3_WORDS, "decoy_mode": "dakuten"}
		}
	},
	5: {
		"name": "Handakuten & Choonpu",
		"difficulty": "EXPERT (★★★★★☆☆☆)",
		"sets": {
			1: {"name": "Set 1: P-Sounds (Handakuten)", "goal": 3, "words": KATAKANA_STAGE5_SET1_WORDS, "decoy_mode": "handakuten"},
			2: {"name": "Set 2: Cafe Long Vowels", "goal": 3, "words": KATAKANA_STAGE5_SET2_WORDS, "decoy_mode": "handakuten"},
			3: {"name": "Set 3: Sports & Transports", "goal": 3, "words": KATAKANA_STAGE5_SET3_WORDS, "decoy_mode": "handakuten"}
		}
	},
	6: {
		"name": "Sokuon Double Stops",
		"difficulty": "HEROIC (★★★★★★☆☆)",
		"sets": {
			1: {"name": "Set 1: Everyday Sokuon", "goal": 3, "words": KATAKANA_STAGE6_SET1_WORDS, "decoy_mode": "sokuon"},
			2: {"name": "Set 2: Sports & Tech Stops", "goal": 3, "words": KATAKANA_STAGE6_SET2_WORDS, "decoy_mode": "sokuon"},
			3: {"name": "Set 3: Compound Sokuon", "goal": 3, "words": KATAKANA_STAGE6_SET3_WORDS, "decoy_mode": "sokuon"}
		}
	},
	7: {
		"name": "Foreign Sounds & Yoon",
		"difficulty": "MASTER (★★★★★★★☆)",
		"sets": {
			1: {"name": "Set 1: Fa, Fi, Fe, Fo", "goal": 3, "words": KATAKANA_STAGE7_SET1_WORDS, "decoy_mode": "advanced"},
			2: {"name": "Set 2: Ti, Di, Che, She", "goal": 3, "words": KATAKANA_STAGE7_SET2_WORDS, "decoy_mode": "advanced"},
			3: {"name": "Set 3: Advanced Foreign Yōn", "goal": 3, "words": KATAKANA_STAGE7_SET3_WORDS, "decoy_mode": "advanced"}
		}
	},
	8: {
		"name": "Grand Master Gauntlet",
		"difficulty": "GRANDMASTER (★★★★★★★★)",
		"sets": {
			1: {"name": "Set 1: Global Loanword Icons", "goal": 3, "words": KATAKANA_STAGE8_SET1_WORDS, "decoy_mode": "master"},
			2: {"name": "Set 2: Travel & Technology", "goal": 3, "words": KATAKANA_STAGE8_SET2_WORDS, "decoy_mode": "master"},
			3: {"name": "Set 3: Ultimate Katakana Champions", "goal": 4, "words": KATAKANA_STAGE8_SET3_WORDS, "decoy_mode": "master"}
		}
	}
}

static func get_stage_set_data(stage_idx: int, set_idx: int, mode: String = "hiragana") -> Dictionary:
	var data_map = KATAKANA_STAGE_DATA if mode == "katakana" else STAGE_DATA
	var s_data = data_map.get(stage_idx, data_map[1])
	var sets_map: Dictionary = s_data.get("sets", {})
	if sets_map.has(set_idx):
		return sets_map[set_idx]
	var default_words = KATAKANA_STAGE1_SET1_WORDS if mode == "katakana" else STAGE1_SET1_WORDS
	return sets_map.get(1, {"name": "Set 1", "goal": 3, "words": default_words, "decoy_mode": "random"})

static func get_confusable_map(mode: String = "hiragana") -> Dictionary:
	return KATAKANA_CONFUSABLE_MAP if mode == "katakana" else CONFUSABLE_MAP

static func get_pools(stage_idx: int, decoy_mode: String, mode: String = "hiragana") -> Array:
	if mode == "katakana":
		if stage_idx >= 7 or decoy_mode in ["master", "advanced"]:
			return KATAKANA_SOKUON_POOL + KATAKANA_HANDAKUTEN_POOL + KATAKANA_DAKUTEN_POOL + KATAKANA_GOJUON_POOL
		elif stage_idx == 6 or decoy_mode == "sokuon":
			return KATAKANA_SOKUON_POOL + KATAKANA_DAKUTEN_POOL + KATAKANA_GOJUON_POOL
		elif stage_idx == 5 or decoy_mode == "handakuten":
			return KATAKANA_HANDAKUTEN_POOL + KATAKANA_DAKUTEN_POOL + KATAKANA_GOJUON_POOL
		elif stage_idx == 4 or decoy_mode == "dakuten":
			return KATAKANA_DAKUTEN_POOL + KATAKANA_GOJUON_POOL
		else:
			return KATAKANA_GOJUON_POOL.duplicate()
	else:
		if stage_idx >= 7 or decoy_mode in ["master", "advanced"]:
			return SOKUON_POOL + HANDAKUTEN_POOL + DAKUTEN_POOL + GOJUON_POOL
		elif stage_idx == 6 or decoy_mode == "sokuon":
			return SOKUON_POOL + DAKUTEN_POOL + GOJUON_POOL
		elif stage_idx == 5 or decoy_mode == "handakuten":
			return HANDAKUTEN_POOL + DAKUTEN_POOL + GOJUON_POOL
		elif stage_idx == 4 or decoy_mode == "dakuten":
			return DAKUTEN_POOL + GOJUON_POOL
		else:
			return GOJUON_POOL.duplicate()
