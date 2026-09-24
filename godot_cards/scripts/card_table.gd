extends Node3D
const WordsData = preload("res://scripts/words_data.gd")

enum State { TITLE, PLAYING, CORRECT, INCORRECT, SET_CLEAR, STAGE_CLEAR, PAUSED }

var current_state: State = State.PLAYING
var previous_state: State = State.PLAYING
const MAX_STAGES: int = 8
var current_stage_index: int = 1
var current_set_index: int = 1 # Backwards compatibility alias
var words_completed: int = 0
var total_words_solved: int = 0
var total_attempts: int = 0

var current_word: Dictionary = {}
var used_words: Array = []
var hand_cards: Array[Card3D] = []
var selected_cards: Array[Card3D] = []
var cursor_index: int = 0

# Timers
var state_timer: float = 0.0
var toast_timer: float = 0.0

# 3D Node References
@onready var camera: Camera3D = $Camera3D
@onready var cards_container: Node3D = $Cards
@onready var confetti_particles: CPUParticles3D = $ConfettiParticles

# UI References
@onready var top_set_label: Label = $HUD/TopBar/Margin/HBox/VBoxCenter/SetTitle
@onready var top_progress_label: Label = $HUD/TopBar/Margin/HBox/WordsCount
@onready var pips_container: HBoxContainer = $HUD/TopBar/Margin/HBox/VBoxCenter/Pips
@onready var romaji_label: Label = $HUD/Plaque/VBox/Romaji
@onready var meaning_label: Label = $HUD/Plaque/VBox/Meaning
@onready var toast_panel: PanelContainer = $HUD/Toast
@onready var toast_label: Label = $HUD/Toast/Margin/ToastLabel
@onready var banner_correct: PanelContainer = $HUD/BannerCorrect
@onready var banner_incorrect: PanelContainer = $HUD/BannerIncorrect
@onready var modal_set_clear: PanelContainer = $HUD/ModalSetClear
@onready var set_clear_title: Label = $HUD/ModalSetClear/Margin/VBox/Title
@onready var modal_stage_clear: PanelContainer = $HUD/ModalStageClear
@onready var stage_clear_title: Label = $HUD/ModalStageClear/Margin/VBox/Title
@onready var stage_clear_stats: Label = $HUD/ModalStageClear/Margin/VBox/Stats
@onready var stage_clear_prompt: Label = $HUD/ModalStageClear/Margin/VBox/Prompt
@onready var modal_paused: PanelContainer = $HUD/ModalPaused

# Audio Players
@onready var sfx_deal: AudioStreamPlayer = $Audio/SfxDeal
@onready var sfx_select: AudioStreamPlayer = $Audio/SfxSelect
@onready var sfx_deselect: AudioStreamPlayer = $Audio/SfxDeselect
@onready var sfx_reset: AudioStreamPlayer = $Audio/SfxReset
@onready var sfx_cursor: AudioStreamPlayer = $Audio/SfxCursor
@onready var sfx_correct: AudioStreamPlayer = $Audio/SfxCorrect
@onready var sfx_incorrect: AudioStreamPlayer = $Audio/SfxIncorrect
@onready var sfx_fanfare: AudioStreamPlayer = $Audio/SfxFanfare

const CardScene = preload("res://scenes/card_3d.tscn")

func _ready():
	DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)
	_init_card_instances()
	_parse_cmdline_stage()
	start_stage(current_stage_index)

func _parse_cmdline_stage():
	var env_st = OS.get_environment("NIHONGO_CARD_STAGE")
	if env_st != "" and env_st.is_valid_int():
		current_stage_index = clampi(env_st.to_int(), 1, MAX_STAGES)
		return

	var args = OS.get_cmdline_args()
	for i in range(args.size()):
		if args[i] == "--stage" and i + 1 < args.size():
			if args[i + 1].is_valid_int():
				current_stage_index = clampi(args[i + 1].to_int(), 1, MAX_STAGES)
				return

func _init_card_instances():
	for i in range(8):
		var card = CardScene.instantiate()
		card.card_id = i
		card.hand_index = i
		cards_container.add_child(card)
		hand_cards.append(card)

func start_game():
	start_stage(1)

func start_stage(stage_idx: int):
	current_stage_index = clampi(stage_idx, 1, MAX_STAGES)
	current_set_index = current_stage_index
	words_completed = 0
	used_words.clear()
	next_round()

# Backwards compatibility alias
func start_set(set_idx: int):
	start_stage(set_idx)

func next_round():
	var cfg = WordsData.STAGE_DATA.get(current_stage_index, WordsData.STAGE_DATA[1])
	var pool = []
	for w in cfg["words"]:
		if not used_words.has(w["romaji"]):
			pool.append(w)
	if pool.is_empty():
		used_words.clear()
		pool = cfg["words"].duplicate()

	current_word = pool[randi() % pool.size()]
	used_words.append(current_word["romaji"])

	_deal_8_card_hand()
	cursor_index = 0
	_update_cursor_hover()
	_update_hud()
	
	current_state = State.PLAYING
	state_timer = 0.0
	_hide_overlays()

func _deal_8_card_hand():
	selected_cards.clear()
	var target_chars: Array = current_word["kana"].duplicate()
	var needed = target_chars.size()
	var decoy_count = 8 - needed

	var cfg = WordsData.STAGE_DATA.get(current_stage_index, WordsData.STAGE_DATA[1])
	var decoy_mode = cfg.get("decoy_mode", "random")

	var decoys: Array = []

	# 1. Intelligent decoy selection based on stage difficulty
	if decoy_mode in ["similar", "lookalike", "dakuten", "handakuten", "sokuon", "advanced", "master"]:
		for c in target_chars:
			if WordsData.CONFUSABLE_MAP.has(c):
				var conf = WordsData.CONFUSABLE_MAP[c]
				if not target_chars.has(conf) and not decoys.has(conf):
					decoys.append(conf)
					if decoys.size() >= decoy_count:
						break

	# 2. Complete remaining decoy quota from stage-appropriate pool
	var pool: Array = []
	if current_stage_index >= 6:
		pool = WordsData.SOKUON_POOL + WordsData.HANDAKUTEN_POOL + WordsData.DAKUTEN_POOL + WordsData.GOJUON_POOL
	elif current_stage_index == 5:
		pool = WordsData.HANDAKUTEN_POOL + WordsData.DAKUTEN_POOL + WordsData.GOJUON_POOL
	elif current_stage_index == 4:
		pool = WordsData.DAKUTEN_POOL + WordsData.GOJUON_POOL
	else:
		pool = WordsData.GOJUON_POOL.duplicate()

	pool.shuffle()
	for c in pool:
		if decoys.size() >= decoy_count:
			break
		if not target_chars.has(c) and not decoys.has(c):
			decoys.append(c)

	var all_chars = target_chars + decoys
	all_chars.shuffle()

	if sfx_deal: sfx_deal.play()

	for i in range(8):
		var card = hand_cards[i]
		card.set_kana(all_chars[i])
		card.set_order(0)
		var hand_pos = _get_hand_position(i)
		# Start slightly offscreen, glide to position
		card.position = hand_pos + Vector3(0, 0.4, 0.8)
		card.rotation_degrees = Vector3(24.0, 0, 0)
		card.glide_to(hand_pos, Vector3(24.0, 0, 0), 0.32 + i * 0.03)

func _get_hand_position(idx: int) -> Vector3:
	var col = idx % 4
	var row = idx / 4
	var x = -2.25 + col * 1.5
	var z = 0.15 if row == 0 else 1.35
	return Vector3(x, 0.32, z)

func _get_tray_position(order_idx: int, total_selected: int) -> Vector3:
	var spacing = 1.3
	var start_x = -((total_selected - 1) * spacing) / 2.0
	var x = start_x + (order_idx - 1) * spacing
	return Vector3(x, 0.34, -0.95)

func _update_cursor_hover():
	for i in range(8):
		hand_cards[i].set_hovered(i == cursor_index)

func _update_card_tray_positions():
	var total = selected_cards.size()
	for i in range(total):
		var c = selected_cards[i]
		c.set_order(i + 1)
		var t_pos = _get_tray_position(i + 1, total)
		c.glide_to(t_pos, Vector3(24.0, 0, 0), 0.22)

func _input(event: InputEvent):
	if current_state == State.PAUSED:
		if event.is_action_pressed("ui_cancel") or (event is InputEventKey and event.pressed and event.keycode in [KEY_ESCAPE, KEY_P]):
			toggle_pause()
		elif event is InputEventJoypadButton and event.pressed:
			if event.button_index in [JOY_BUTTON_START, JOY_BUTTON_BACK, JOY_BUTTON_A]:
				toggle_pause()
			elif event.button_index == JOY_BUTTON_B:
				toggle_pause()
				start_set(current_set_index)
			elif event.button_index in [JOY_BUTTON_X, 2, 3]:
				get_tree().quit()
		return

	if current_state == State.STAGE_CLEAR:
		if (event is InputEventJoypadButton and event.pressed and event.button_index == JOY_BUTTON_A) or (event is InputEventKey and event.pressed and event.keycode == KEY_ENTER):
			if current_stage_index >= MAX_STAGES:
				start_stage(1)
			else:
				start_stage(current_stage_index + 1)
		elif (event is InputEventJoypadButton and event.pressed and event.button_index in [JOY_BUTTON_B, JOY_BUTTON_START, JOY_BUTTON_BACK]) or (event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE):
			get_tree().quit()
		return

	if current_state != State.PLAYING:
		return

	# 1. Navigation (D-Pad & Analog Stick & Arrow Keys)
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_LEFT, KEY_A: _move_cursor(-1, 0)
			KEY_RIGHT, KEY_D: _move_cursor(1, 0)
			KEY_UP, KEY_W: _move_cursor(0, -1)
			KEY_DOWN, KEY_S: _move_cursor(0, 1)
			KEY_SPACE, KEY_ENTER, KEY_Z: toggle_selected_card()
			KEY_BACKSPACE, KEY_K: reset_selection()
			KEY_TAB, KEY_X, KEY_C: submit_word()
			KEY_ESCAPE, KEY_P: toggle_pause()

	elif event is InputEventJoypadButton and event.pressed:
		var btn = event.button_index
		if btn == JOY_BUTTON_DPAD_LEFT: _move_cursor(-1, 0)
		elif btn == JOY_BUTTON_DPAD_RIGHT: _move_cursor(1, 0)
		elif btn == JOY_BUTTON_DPAD_UP: _move_cursor(0, -1)
		elif btn == JOY_BUTTON_DPAD_DOWN: _move_cursor(0, 1)
		elif btn == JOY_BUTTON_A: toggle_selected_card()
		elif btn == JOY_BUTTON_B: reset_selection()
		elif btn in [JOY_BUTTON_X, 2, 3, JOY_BUTTON_RIGHT_SHOULDER]:
			# Supports Xbox X (2), 8BitDo/Nintendo X (3), and RB!
			submit_word()
		elif btn in [JOY_BUTTON_START, JOY_BUTTON_BACK]: toggle_pause()

func _move_cursor(dx: int, dy: int):
	var old = cursor_index
	if dx != 0:
		var col = cursor_index % 4
		var row = cursor_index / 4
		col = (col + dx + 4) % 4
		cursor_index = row * 4 + col
	if dy != 0:
		var col = cursor_index % 4
		var row = cursor_index / 4
		row = (row + dy + 2) % 2
		cursor_index = row * 4 + col

	if cursor_index != old:
		_update_cursor_hover()
		if sfx_cursor: sfx_cursor.play()

func toggle_selected_card():
	var card = hand_cards[cursor_index]
	if not card.is_selected:
		selected_cards.append(card)
		_update_card_tray_positions()
		if sfx_select: sfx_select.play()

		# Card selection goes back to the hand so player won't have to press down
		var next_idx = -1
		for offset in range(1, 8):
			var check_idx = (cursor_index + offset) % 8
			if not hand_cards[check_idx].is_selected:
				next_idx = check_idx
				break
		if next_idx != -1:
			cursor_index = next_idx
		_update_cursor_hover()
	else:
		selected_cards.erase(card)
		card.set_order(0)
		var hand_pos = _get_hand_position(card.hand_index)
		card.glide_to(hand_pos, Vector3(24.0, 0, 0), 0.22)
		_update_card_tray_positions()
		if sfx_deselect: sfx_deselect.play()
		_update_cursor_hover()

func reset_selection():
	if selected_cards.is_empty():
		return
	for c in selected_cards:
		c.set_order(0)
		var hand_pos = _get_hand_position(c.hand_index)
		c.glide_to(hand_pos, Vector3(24.0, 0, 0), 0.24)
	selected_cards.clear()
	if sfx_reset: sfx_reset.play()
	_update_cursor_hover()

func submit_word():
	if selected_cards.is_empty():
		_show_toast("PLEASE SELECT CARDS FIRST!")
		if sfx_deselect: sfx_deselect.play()
		return

	var chosen_chars = []
	for c in selected_cards:
		chosen_chars.append(c.kana)

	total_attempts += 1
	var target_chars = current_word["kana"]

	if chosen_chars == target_chars:
		# CORRECT ANSWER
		words_completed += 1
		total_words_solved += 1
		current_state = State.CORRECT
		state_timer = 0.0
		if banner_correct: banner_correct.visible = true
		if sfx_correct: sfx_correct.play()
		if confetti_particles: confetti_particles.restart()
		_update_hud()
	else:
		# INCORRECT SEQUENCE
		current_state = State.INCORRECT
		state_timer = 0.0
		if banner_incorrect: banner_incorrect.visible = true
		if sfx_incorrect: sfx_incorrect.play()
		for c in selected_cards:
			c.shake()

func toggle_pause():
	if current_state == State.PAUSED:
		current_state = previous_state
		if modal_paused: modal_paused.visible = false
	else:
		previous_state = current_state
		current_state = State.PAUSED
		if modal_paused: modal_paused.visible = true

func _show_toast(msg: String):
	toast_label.text = msg
	toast_panel.visible = true
	toast_timer = 1.6

func _hide_overlays():
	if banner_correct: banner_correct.visible = false
	if banner_incorrect: banner_incorrect.visible = false
	if modal_set_clear: modal_set_clear.visible = false
	if modal_stage_clear: modal_stage_clear.visible = false
	if modal_paused: modal_paused.visible = false
	if toast_panel: toast_panel.visible = false

func _process(delta: float):
	state_timer += delta
	if toast_timer > 0.0:
		toast_timer = max(0.0, toast_timer - delta)
		if toast_timer <= 0.0 and toast_panel:
			toast_panel.visible = false

	if current_state == State.CORRECT:
		if state_timer >= 1.2:
			var cfg = WordsData.STAGE_DATA.get(current_stage_index, WordsData.STAGE_DATA[1])
			if words_completed >= cfg["goal"]:
				current_state = State.STAGE_CLEAR
				state_timer = 0.0
				_hide_overlays()
				var acc = (float(total_words_solved) / max(1, total_attempts)) * 100.0
				stage_clear_stats.text = "Words Solved: %d  |  Total Attempts: %d  |  Accuracy: %.1f%%" % [total_words_solved, total_attempts, acc]
				if current_stage_index >= MAX_STAGES:
					stage_clear_title.text = "GRAND MASTER CHAMPION!"
					stage_clear_prompt.text = "All 8 Stages Cleared! Press (A) / Enter to Play Again • (B) to Exit"
				else:
					stage_clear_title.text = "STAGE %02d CLEAR!" % current_stage_index
					stage_clear_prompt.text = "Press (A) / Enter for Stage %02d • (B) to Exit" % (current_stage_index + 1)
				modal_stage_clear.visible = true
				if sfx_fanfare: sfx_fanfare.play()
			else:
				next_round()

	elif current_state == State.INCORRECT:
		if state_timer >= 1.2:
			reset_selection()
			current_state = State.PLAYING
			if banner_incorrect: banner_incorrect.visible = false

	elif current_state == State.SET_CLEAR:
		if state_timer >= 2.8:
			start_stage(current_stage_index + 1)

func _update_hud():
	if current_word.is_empty():
		return
	var cfg = WordsData.STAGE_DATA.get(current_stage_index, WordsData.STAGE_DATA[1])
	top_set_label.text = "STAGE %02d/%02d — %s" % [current_stage_index, MAX_STAGES, cfg["name"].to_upper()]
	top_progress_label.text = "WORDS: %d/%d" % [words_completed, cfg["goal"]]
	
	romaji_label.text = "  ".join(current_word["romaji"].split())
	meaning_label.text = "“ %s ”" % current_word["meaning"]

	# Update pips
	for child in pips_container.get_children():
		child.queue_free()
	for i in range(cfg["goal"]):
		var pip = ColorRect.new()
		pip.custom_minimum_size = Vector2(14, 14)
		pip.color = Color(0.18, 0.84, 0.45, 1) if i < words_completed else Color(0.25, 0.35, 0.3, 0.8)
		pips_container.add_child(pip)

