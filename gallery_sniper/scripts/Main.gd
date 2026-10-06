extends Node2D
## Main.gd
## The Gallery Sniper - Core Game Controller
## Manages 2 separate Kana game versions (Hiragana & Katakana), vocabulary dictionaries,
## target spawning, scoring, and gamepad/mouse shooting.

@export var target_scene: PackedScene = preload("res://scenes/target.tscn")

enum KanaMode { HIRAGANA, KATAKANA }
var current_mode: KanaMode = KanaMode.HIRAGANA

## 1. Separate Hiragana Vocabulary Dictionary
var hiragana_dictionary: Dictionary = {
	"ringo": {"kana": ["り", "ん", "ご"], "meaning": "apple"},
	"sakura": {"kana": ["さ", "く", "ら"], "meaning": "cherry blossom"},
	"kuruma": {"kana": ["く", "る", "ま"], "meaning": "car"},
	"neko": {"kana": ["ね", "こ"], "meaning": "cat"},
	"inu": {"kana": ["い", "ぬ"], "meaning": "dog"},
	"sushi": {"kana": ["す", "し"], "meaning": "sushi"},
	"tori": {"kana": ["と", "り"], "meaning": "bird"},
	"kame": {"kana": ["か", "め"], "meaning": "turtle"},
	"hana": {"kana": ["は", "な"], "meaning": "flower"},
	"mizu": {"kana": ["み", "ず"], "meaning": "water"},
	"yama": {"kana": ["や", "ま"], "meaning": "mountain"},
	"kawa": {"kana": ["か", "わ"], "meaning": "river"},
	"sora": {"kana": ["そ", "ら"], "meaning": "sky"},
	"tsuki": {"kana": ["つ", "き"], "meaning": "moon"},
	"hoshi": {"kana": ["ほ", "し"], "meaning": "star"}
}

## 2. Separate Katakana Vocabulary Dictionary
var katakana_dictionary: Dictionary = {
	"terebi": {"kana": ["テ", "レ", "ビ"], "meaning": "television"},
	"ramen": {"kana": ["ラ", "ー", "メ", "ン"], "meaning": "ramen"},
	"kohii": {"kana": ["コ", "ー", "ヒ", "ー"], "meaning": "coffee"},
	"basu": {"kana": ["バ", "ス"], "meaning": "bus"},
	"kamera": {"kana": ["カ", "メ", "ラ"], "meaning": "camera"},
	"anime": {"kana": ["ア", "ニ", "メ"], "meaning": "anime"},
	"pan": {"kana": ["パ", "ン"], "meaning": "bread"},
	"aisu": {"kana": ["ア", "イ", "ス"], "meaning": "ice cream"},
	"keeki": {"kana": ["ケ", "ー", "キ"], "meaning": "cake"},
	"taoru": {"kana": ["タ", "オ", "ル"], "meaning": "towel"},
	"doa": {"kana": ["ド", "ア"], "meaning": "door"},
	"rajio": {"kana": ["ラ", "ジ", "オ"], "meaning": "radio"},
	"nooto": {"kana": ["ノ", "ー", "ト"], "meaning": "notebook"},
	"sofaa": {"kana": ["ソ", "フ", "ァ", "ー"], "meaning": "sofa"}
}

## Hiragana syllabary pool for decoys
const HIRAGANA_POOL: Array[String] = [
	"あ", "い", "う", "え", "お",
	"か", "き", "く", "け", "こ",
	"さ", "し", "す", "せ", "そ",
	"た", "ち", "つ", "て", "と",
	"な", "に", "ぬ", "ね", "の",
	"は", "ひ", "ふ", "へ", "ほ",
	"ま", "み", "む", "め", "も",
	"や", "ゆ", "よ",
	"ら", "り", "る", "れ", "ろ",
	"わ", "を", "ん",
	"が", "ぎ", "ぐ", "げ", "ご",
	"ざ", "じ", "ず", "ぜ", "ぞ",
	"だ", "で", "ど",
	"ば", "び", "ぶ", "べ", "ぼ",
	"ぱ", "ぴ", "ぷ", "ぺ", "ぽ"
]

## Katakana syllabary pool for decoys
const KATAKANA_POOL: Array[String] = [
	"ア", "イ", "ウ", "エ", "オ",
	"カ", "キ", "ク", "ケ", "コ",
	"サ", "シ", "ス", "セ", "ソ",
	"タ", "チ", "ツ", "テ", "ト",
	"ナ", "ニ", "ヌ", "ネ", "ノ",
	"ハ", "ヒ", "フ", "ヘ", "ホ",
	"マ", "ミ", "ム", "メ", "モ",
	"ヤ", "ユ", "ヨ",
	"ラ", "リ", "ル", "レ", "ロ",
	"ワ", "ヲ", "ン",
	"ガ", "ギ", "グ", "ゲ", "ゴ",
	"ザ", "ジ", "ズ", "ゼ", "ゾ",
	"ダ", "デ", "ド",
	"バ", "ビ", "ブ", "ベ", "ボ",
	"パ", "ピ", "プ", "ペ", "ポ"
]

## Game state tracking per mode
var current_word: String = ""
var current_character_index: int = 0

var hiragana_score: int = 0
var hiragana_cleared: int = 0

var katakana_score: int = 0
var katakana_cleared: int = 0

## Node references
@onready var targets_container: Node2D = $TargetsContainer
@onready var spawn_points_node: Node2D = $SpawnPoints
@onready var target_word_label: Label = $UI/TargetWordLabel
@onready var word_meaning_label: Label = $UI/WordMeaningLabel
@onready var spelling_progress_label: Label = $UI/SpellingProgressLabel
@onready var score_label: Label = $UI/ScoreLabel
@onready var words_count_label: Label = $UI/WordsCountLabel
@onready var hiragana_tab: Button = $UI/HiraganaTab
@onready var katakana_tab: Button = $UI/KatakanaTab
@onready var header_gold_border: ColorRect = $UI/HeaderGoldBorder

@onready var correct_player: AudioStreamPlayer = $Audio/CorrectPlayer
@onready var incorrect_player: AudioStreamPlayer = $Audio/IncorrectPlayer
@onready var shot_player: AudioStreamPlayer = $Audio/ShotPlayer
@onready var fanfare_player: AudioStreamPlayer = $Audio/FanfarePlayer
@onready var crosshair: Node2D = $Crosshair

@onready var pause_button: Button = $UI/PauseButton
@onready var pause_modal: Control = $UI/PauseModal
@onready var btn_resume: Button = $UI/PauseModal/ModalPanel/Margin/VBox/BtnResume
@onready var btn_restart: Button = $UI/PauseModal/ModalPanel/Margin/VBox/BtnRestart
@onready var btn_switch_kana: Button = $UI/PauseModal/ModalPanel/Margin/VBox/BtnSwitchKana
@onready var btn_return_title: Button = $UI/PauseModal/ModalPanel/Margin/VBox/BtnReturnTitle

var spawn_points: Array[Marker2D] = []

func _ready() -> void:
	randomize()
	process_mode = Node.PROCESS_MODE_ALWAYS
	
	# Always launch in exclusive fullscreen mode at the display's maximum native resolution
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_EXCLUSIVE_FULLSCREEN)
	
	# Connect gamepad shot trigger from Crosshair
	if crosshair and crosshair.has_signal("shot_requested"):
		crosshair.shot_requested.connect(_on_gamepad_shot)
	
	# Connect UI Mode tabs and Pause button
	if hiragana_tab:
		hiragana_tab.pressed.connect(func(): set_mode(KanaMode.HIRAGANA))
	if katakana_tab:
		katakana_tab.pressed.connect(func(): set_mode(KanaMode.KATAKANA))
	if pause_button:
		pause_button.pressed.connect(toggle_pause)
	if btn_resume:
		btn_resume.pressed.connect(toggle_pause)
	if btn_restart:
		btn_restart.pressed.connect(_on_restart_pressed)
	if btn_switch_kana:
		btn_switch_kana.pressed.connect(_on_switch_kana_pressed)
	if btn_return_title:
		btn_return_title.pressed.connect(_on_return_title_pressed)
	
	# Cache all pre-defined Marker2D spawn points
	for child in spawn_points_node.get_children():
		if child is Marker2D:
			spawn_points.append(child)
	
	_parse_cmd_line_arguments()
	update_tab_styles()
	start_new_word()

## Parses command-line arguments and environment variables to set initial mode
func _parse_cmd_line_arguments() -> void:
	var env_mode = OS.get_environment("NIHONGO_SNIPER_MODE").to_lower()
	if env_mode == "katakana":
		current_mode = KanaMode.KATAKANA
	elif env_mode == "hiragana":
		current_mode = KanaMode.HIRAGANA
	
	var args = OS.get_cmdline_user_args()
	if args.is_empty():
		args = OS.get_cmdline_args()
	for i in range(args.size()):
		if args[i] == "--mode" and i + 1 < args.size():
			var val = args[i + 1].to_lower()
			if val == "katakana":
				current_mode = KanaMode.KATAKANA
			elif val == "hiragana":
				current_mode = KanaMode.HIRAGANA


## Returns the active vocabulary dictionary based on current mode
func get_active_dictionary() -> Dictionary:
	return hiragana_dictionary if current_mode == KanaMode.HIRAGANA else katakana_dictionary

## Returns the Kana character sequence for the current active word
func get_current_word_chars() -> Array:
	var dict = get_active_dictionary()
	if not dict.has(current_word):
		return []
	var val = dict[current_word]
	if val is Dictionary:
		return val.get("kana", [])
	elif val is Array:
		return val
	return []

## Returns the English translation meaning for the current active word
func get_current_word_meaning() -> String:
	var dict = get_active_dictionary()
	if not dict.has(current_word):
		return ""
	var val = dict[current_word]
	if val is Dictionary:
		return val.get("meaning", "")
	return ""

## Returns the active syllabary pool for decoys
func get_active_pool() -> Array[String]:
	return HIRAGANA_POOL if current_mode == KanaMode.HIRAGANA else KATAKANA_POOL

## Returns current mode score
func get_current_score() -> int:
	return hiragana_score if current_mode == KanaMode.HIRAGANA else katakana_score

func add_current_score(amount: int) -> void:
	if current_mode == KanaMode.HIRAGANA:
		hiragana_score = maxi(0, hiragana_score + amount)
	else:
		katakana_score = maxi(0, katakana_score + amount)

## Returns current mode cleared count
func get_current_cleared() -> int:
	return hiragana_cleared if current_mode == KanaMode.HIRAGANA else katakana_cleared

func add_current_cleared() -> void:
	if current_mode == KanaMode.HIRAGANA:
		hiragana_cleared += 1
	else:
		katakana_cleared += 1

## Switches between Hiragana and Katakana versions
func set_mode(new_mode: KanaMode) -> void:
	if current_mode == new_mode:
		return
	current_mode = new_mode
	if shot_player:
		shot_player.play()
	update_tab_styles()
	start_new_word()

func toggle_mode() -> void:
	set_mode(KanaMode.KATAKANA if current_mode == KanaMode.HIRAGANA else KanaMode.HIRAGANA)

## Visual tab highlight updates
func update_tab_styles() -> void:
	if current_mode == KanaMode.HIRAGANA:
		if hiragana_tab:
			hiragana_tab.modulate = Color(1.0, 0.88, 0.25, 1.0)
		if katakana_tab:
			katakana_tab.modulate = Color(0.65, 0.7, 0.8, 0.6)
		if header_gold_border:
			header_gold_border.color = Color(0.95, 0.75, 0.2, 1.0)
	else:
		if hiragana_tab:
			hiragana_tab.modulate = Color(0.65, 0.7, 0.8, 0.6)
		if katakana_tab:
			katakana_tab.modulate = Color(0.2, 0.9, 1.0, 1.0)
		if header_gold_border:
			header_gold_border.color = Color(0.0, 0.85, 1.0, 1.0)
	
	if btn_switch_kana:
		var target_name = "KATAKANA" if current_mode == KanaMode.HIRAGANA else "HIRAGANA"
		btn_switch_kana.text = "⇄  SWITCH TO %s   [(Y) / TAB]" % target_name

## Toggles Pause modal and game state
func toggle_pause() -> void:
	var new_paused = not get_tree().paused
	get_tree().paused = new_paused
	if pause_modal:
		pause_modal.visible = new_paused
	
	if new_paused:
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		if crosshair:
			crosshair.visible = false
		if btn_resume:
			btn_resume.grab_focus()
		if shot_player:
			shot_player.play()
	else:
		Input.set_mouse_mode(Input.MOUSE_MODE_HIDDEN)
		if crosshair:
			crosshair.visible = true

func _on_restart_pressed() -> void:
	if get_tree().paused:
		toggle_pause()
	current_character_index = 0
	if current_mode == KanaMode.HIRAGANA:
		hiragana_score = 0
		hiragana_cleared = 0
	else:
		katakana_score = 0
		katakana_cleared = 0
	start_new_word()

func _on_switch_kana_pressed() -> void:
	toggle_mode()

func _on_return_title_pressed() -> void:
	if get_tree().paused:
		get_tree().paused = false
	get_tree().quit()

## Handles quick desktop / Steam Deck / Gamepad shortcuts
func _unhandled_input(event: InputEvent) -> void:
	# 1. When Paused:
	if get_tree().paused:
		if event is InputEventKey and event.pressed:
			match event.keycode:
				KEY_ESCAPE, KEY_P:
					toggle_pause()
					get_viewport().set_input_as_handled()
				KEY_R:
					_on_restart_pressed()
					get_viewport().set_input_as_handled()
				KEY_TAB:
					_on_switch_kana_pressed()
					get_viewport().set_input_as_handled()
				KEY_Q:
					_on_return_title_pressed()
					get_viewport().set_input_as_handled()
		elif event is InputEventJoypadButton and event.pressed:
			match event.button_index:
				JOY_BUTTON_START, JOY_BUTTON_BACK, JOY_BUTTON_B:
					toggle_pause()
					get_viewport().set_input_as_handled()
				JOY_BUTTON_X, 2, 3:
					_on_return_title_pressed()
					get_viewport().set_input_as_handled()
				JOY_BUTTON_Y:
					_on_switch_kana_pressed()
					get_viewport().set_input_as_handled()
		return

	# 2. When Playing:
	if event is InputEventKey and event.pressed:
		match event.keycode:
			KEY_ESCAPE, KEY_P:
				toggle_pause()
			KEY_F11:
				var mode = DisplayServer.window_get_mode()
				if mode == DisplayServer.WINDOW_MODE_EXCLUSIVE_FULLSCREEN or mode == DisplayServer.WINDOW_MODE_FULLSCREEN:
					DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
				else:
					DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_EXCLUSIVE_FULLSCREEN)
			KEY_TAB:
				toggle_mode()
			KEY_1:
				set_mode(KanaMode.HIRAGANA)
			KEY_2:
				set_mode(KanaMode.KATAKANA)
	
	elif event is InputEventJoypadButton and event.pressed:
		match event.button_index:
			JOY_BUTTON_START, JOY_BUTTON_BACK:
				toggle_pause()
			JOY_BUTTON_LEFT_SHOULDER:
				set_mode(KanaMode.HIRAGANA)
			JOY_BUTTON_RIGHT_SHOULDER:
				set_mode(KanaMode.KATAKANA)
			JOY_BUTTON_Y:
				toggle_mode()

## Handles gamepad shot trigger hitting a target at crosshair location
func _on_gamepad_shot(shot_pos: Vector2) -> void:
	if get_tree().paused:
		return
	var hit_target: Node = null
	var min_dist: float = 54.0 # Target radius is 48
	for child in targets_container.get_children():
		if child.has_method("set_character") and child.get("is_active"):
			var d = child.position.distance_to(shot_pos)
			if d < min_dist:
				min_dist = d
				hit_target = child
	
	if hit_target:
		_on_target_clicked(hit_target.character)
	else:
		if shot_player:
			shot_player.play()

## Picks a new random word from active mode dictionary, resets index, updates UI
func start_new_word() -> void:
	var dict = get_active_dictionary()
	var keys = dict.keys()
	if keys.is_empty():
		return
	
	var next_word = keys.pick_random()
	if keys.size() > 1 and next_word == current_word:
		while next_word == current_word:
			next_word = keys.pick_random()
	
	current_word = next_word
	current_character_index = 0
	
	update_ui()
	spawn_targets()

## Clears existing targets, generates decoys from mode syllabary pool, and spawns targets
func spawn_targets() -> void:
	for child in targets_container.get_children():
		child.queue_free()
	
	if current_word == "":
		return
	
	var word_chars: Array = get_current_word_chars()
	if current_character_index >= word_chars.size():
		return
	
	# 1. Correct next Kana character
	var correct_char: String = word_chars[current_character_index]
	
	# 2. Pick 3 to 4 random decoy characters strictly from active mode pool
	var pool = get_active_pool()
	var num_decoys: int = randi_range(3, 4)
	var available_decoys: Array[String] = pool.duplicate()
	available_decoys.erase(correct_char)
	available_decoys.shuffle()
	
	var chosen_chars: Array[String] = [correct_char]
	for i in range(mini(num_decoys, available_decoys.size())):
		chosen_chars.append(available_decoys[i])
	
	chosen_chars.shuffle()
	
	# 3. Place at random Marker2D spawn points
	var available_points: Array[Marker2D] = spawn_points.duplicate()
	available_points.shuffle()
	
	for i in range(chosen_chars.size()):
		if i >= available_points.size():
			break
		var marker: Marker2D = available_points[i]
		var target_instance = target_scene.instantiate()
		target_instance.position = marker.position
		targets_container.add_child(target_instance)
		target_instance.set_character(chosen_chars[i])
		target_instance.target_clicked.connect(_on_target_clicked)

## Evaluates clicked target character
func _on_target_clicked(clicked_character: String) -> void:
	if current_word == "":
		return
	
	var word_chars: Array = get_current_word_chars()
	if current_character_index >= word_chars.size():
		return
	
	var expected_char: String = word_chars[current_character_index]
	
	if clicked_character == expected_char:
		# Correct target shot!
		if shot_player:
			shot_player.play()
		if correct_player:
			correct_player.play()
		
		# Animate hit target
		for child in targets_container.get_children():
			if child.has_method("set_character") and child.character == clicked_character:
				if child.has_method("play_hit_effect"):
					child.play_hit_effect()
		
		current_character_index += 1
		update_ui()
		
		if current_character_index >= word_chars.size():
			# Full word completed!
			add_current_score(10)
			add_current_cleared()
			if fanfare_player:
				fanfare_player.play()
			update_ui()
			get_tree().create_timer(0.45).timeout.connect(start_new_word)
		else:
			get_tree().create_timer(0.2).timeout.connect(spawn_targets)
	else:
		# Incorrect target shot!
		add_current_score(-2)
		if incorrect_player:
			incorrect_player.play()
		
		# Shake clicked wrong target
		for child in targets_container.get_children():
			if child.has_method("set_character") and child.character == clicked_character:
				if child.has_method("play_wrong_effect"):
					child.play_wrong_effect()
		
		update_ui()

## Updates the UI labels to reflect current game state
func update_ui() -> void:
	if current_word == "":
		return
	
	var word_chars: Array = get_current_word_chars()
	
	# Target word header (romaji)
	target_word_label.text = current_word.to_upper()
	
	# Word translation meaning
	if word_meaning_label:
		var meaning = get_current_word_meaning()
		if meaning != "":
			word_meaning_label.text = "“ %s ”" % meaning
		else:
			word_meaning_label.text = ""
	
	# Progress text
	var progress_parts: Array[String] = []
	for i in range(word_chars.size()):
		if i < current_character_index:
			progress_parts.append(word_chars[i])
		else:
			progress_parts.append("＿")
	
	var progress_str = "  ".join(progress_parts)
	if current_character_index >= word_chars.size():
		progress_str += "  ★"
	
	spelling_progress_label.text = progress_str
	
	# Score and Cleared counters for active mode
	score_label.text = "SCORE: %d" % get_current_score()
	if words_count_label:
		words_count_label.text = "CLEARED: %d" % get_current_cleared()
