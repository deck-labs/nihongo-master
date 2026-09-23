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

const SET1_WORDS = [
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
	{"romaji": "SUSHI", "meaning": "sushi", "kana": ["す", "し"]},
	{"romaji": "HACHI", "meaning": "bee", "kana": ["は", "ち"]},
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

const SET2_WORDS = [
	{"romaji": "SAKANA", "meaning": "fish", "kana": ["さ", "か", "な"]},
	{"romaji": "KURUMA", "meaning": "car", "kana": ["く", "る", "ま"]},
	{"romaji": "YASAI", "meaning": "vegetable", "kana": ["や", "さ", "い"]},
	{"romaji": "KATANA", "meaning": "sword", "kana": ["か", "た", "な"]},
	{"romaji": "SAKURA", "meaning": "cherry blossom", "kana": ["さ", "く", "ら"]},
	{"romaji": "KITSUNE", "meaning": "fox", "kana": ["き", "つ", "ね"]},
	{"romaji": "TANUKI", "meaning": "raccoon dog", "kana": ["た", "ぬ", "き"]},
	{"romaji": "KARASU", "meaning": "crow", "kana": ["か", "ら", "す"]},
	{"romaji": "KUSURI", "meaning": "medicine", "kana": ["く", "す", "り"]},
	{"romaji": "HIKARI", "meaning": "light", "kana": ["ひ", "か", "り"]},
	{"romaji": "SEKAI", "meaning": "world", "kana": ["せ", "か", "い"]},
	{"romaji": "ASAHI", "meaning": "morning sun", "kana": ["あ", "さ", "ひ"]},
	{"romaji": "KOKORO", "meaning": "heart / spirit", "kana": ["こ", "こ", "ろ"]},
	{"romaji": "KAERU", "meaning": "frog", "kana": ["か", "え", "る"]},
	{"romaji": "ATAMA", "meaning": "head", "kana": ["あ", "た", "ま"]},
	{"romaji": "KIMONO", "meaning": "kimono", "kana": ["き", "も", "の"]},
	{"romaji": "TSUKIMI", "meaning": "moon viewing", "kana": ["つ", "き", "み"]},
	{"romaji": "SORA", "meaning": "sky", "kana": ["そ", "ら"]},
	{"romaji": "YAMA", "meaning": "mountain", "kana": ["や", "ま"]},
	{"romaji": "HANA", "meaning": "flower", "kana": ["は", "な"]},
	{"romaji": "NEKO", "meaning": "cat", "kana": ["ね", "こ"]},
	{"romaji": "MINATO", "meaning": "harbor", "kana": ["み", "な", "と"]},
	{"romaji": "KUMOMA", "meaning": "cloud rift", "kana": ["く", "も", "ま"]}
]

const SET3_WORDS = [
	{"romaji": "TABEMONO", "meaning": "food", "kana": ["た", "べ", "も", "の"]},
	{"romaji": "TOMODACHI", "meaning": "friend", "kana": ["と", "も", "だ", "ち"]},
	{"romaji": "KURUMA", "meaning": "car", "kana": ["く", "る", "ま"]},
	{"romaji": "YASAI", "meaning": "vegetable", "kana": ["や", "さ", "い"]},
	{"romaji": "SAKANA", "meaning": "fish", "kana": ["さ", "か", "な"]},
	{"romaji": "SAKURA", "meaning": "cherry blossom", "kana": ["さ", "く", "ら"]},
	{"romaji": "KATANA", "meaning": "sword", "kana": ["か", "た", "な"]},
	{"romaji": "KITSUNE", "meaning": "fox", "kana": ["き", "つ", "ね"]},
	{"romaji": "ASAYAKE", "meaning": "morning glow", "kana": ["あ", "さ", "や", "け"]},
	{"romaji": "HATARAKI", "meaning": "work / function", "kana": ["は", "た", "ら", "き"]},
	{"romaji": "KIMONO", "meaning": "kimono", "kana": ["き", "も", "の"]},
	{"romaji": "TSUKIMI", "meaning": "moon viewing", "kana": ["つ", "き", "み"]},
	{"romaji": "KOKORO", "meaning": "heart / spirit", "kana": ["こ", "こ", "ろ"]},
	{"romaji": "HIKARI", "meaning": "light", "kana": ["ひ", "か", "り"]},
	{"romaji": "SEKAI", "meaning": "world", "kana": ["せ", "か", "い"]},
	{"romaji": "MINATO", "meaning": "harbor", "kana": ["み", "な", "と"]},
	{"romaji": "INOSHISHI", "meaning": "wild boar", "kana": ["い", "の", "し", "し"]},
	{"romaji": "KAMISAMA", "meaning": "deity", "kana": ["か", "み", "さ", "ま"]},
	{"romaji": "YASASHISA", "meaning": "kindness", "kana": ["や", "さ", "し", "さ"]},
	{"romaji": "OMATSURI", "meaning": "festival", "kana": ["お", "ま", "つ", "り"]}
]

const STAGE_SETS = {
	1: {
		"name": "Hiragana Introduction",
		"goal": 3,
		"words": SET1_WORDS
	},
	2: {
		"name": "More Characters",
		"goal": 5,
		"words": SET2_WORDS
	},
	3: {
		"name": "Longer Words",
		"goal": 7,
		"words": SET3_WORDS
	}
}
