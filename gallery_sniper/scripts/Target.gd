extends Area2D
## Target.gd
## Represents an individual shooting gallery target displaying a Kana character.
## Emits target_clicked(character) when shot by the player.

signal target_clicked(character: String)

enum MotionType { NONE, BOB, SWAY, PATROL, WAVE }

var character: String = ""
var is_active: bool = true

var motion_type: MotionType = MotionType.NONE
var move_speed: float = 0.0
var move_dir: float = 1.0
var base_position: Vector2 = Vector2.ZERO
var time_offset: float = 0.0
var min_x: float = 160.0
var max_x: float = 1120.0

@onready var label: Label = $Label
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	# Ensure the target can receive mouse input
	input_pickable = true
	base_position = position
	# Initial pop-in animation
	scale = Vector2(0.1, 0.1)
	var tween = create_tween().set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tween.tween_property(self, "scale", Vector2.ONE, 0.25)

func setup_motion(p_motion: MotionType, p_speed: float = 0.0) -> void:
	motion_type = p_motion
	move_speed = p_speed
	base_position = position
	time_offset = randf_range(0.0, 10.0)
	move_dir = 1.0 if randf() > 0.5 else -1.0

func _process(delta: float) -> void:
	if not is_active:
		return
	
	match motion_type:
		MotionType.NONE:
			pass
		MotionType.BOB:
			var t = (Time.get_ticks_msec() / 1000.0) + time_offset
			position.y = base_position.y + sin(t * 3.0) * 12.0
		MotionType.SWAY:
			var t = (Time.get_ticks_msec() / 1000.0) + time_offset
			position.x = base_position.x + sin(t * 2.5) * 35.0
		MotionType.PATROL:
			position.x += move_dir * move_speed * delta
			if position.x > max_x:
				position.x = max_x
				move_dir = -1.0
			elif position.x < min_x:
				position.x = min_x
				move_dir = 1.0
		MotionType.WAVE:
			position.x += move_dir * move_speed * delta
			var t = (Time.get_ticks_msec() / 1000.0) + time_offset
			position.y = base_position.y + sin(t * 4.0) * 14.0
			if position.x > max_x:
				position.x = max_x
				move_dir = -1.0
			elif position.x < min_x:
				position.x = min_x
				move_dir = 1.0

## Renders arcade carnival target with crisp concentric circles
func _draw() -> void:
	# Outer brass/gold border ring
	draw_circle(Vector2.ZERO, 48.0, Color(0.92, 0.76, 0.22, 1.0))
	# Outer red band
	draw_circle(Vector2.ZERO, 45.0, Color(0.85, 0.18, 0.22, 1.0))
	# Middle cream/white ring
	draw_circle(Vector2.ZERO, 35.0, Color(0.96, 0.94, 0.88, 1.0))
	# Inner red ring
	draw_circle(Vector2.ZERO, 25.0, Color(0.85, 0.18, 0.22, 1.0))
	# Bullseye dark center core for maximum Japanese Kana contrast
	draw_circle(Vector2.ZERO, 17.0, Color(0.12, 0.14, 0.22, 0.85))

## Sets the Kana character displayed on this target
func set_character(new_char: String) -> void:
	character = new_char
	if label:
		label.text = character

## Handles player clicks on this target's Area2D collision zone
func _input_event(_viewport: Node, event: InputEvent, _shape_idx: int) -> void:
	if not is_active:
		return
	
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		target_clicked.emit(character)

## Play successful hit animation (pop & shrink) then free
func play_hit_effect() -> void:
	is_active = false
	var tween = create_tween().set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
	tween.tween_property(self, "scale", Vector2(1.35, 1.35), 0.1)
	tween.tween_property(self, "scale", Vector2(0.0, 0.0), 0.15)
	tween.tween_callback(queue_free)

## Play wrong target penalty animation (shake & flash)
func play_wrong_effect() -> void:
	if label:
		var tween = create_tween().set_trans(Tween.TRANS_SINE)
		tween.tween_property(label, "position:x", -46.0 - 12.0, 0.04)
		tween.tween_property(label, "position:x", -46.0 + 12.0, 0.04)
		tween.tween_property(label, "position:x", -46.0 - 8.0, 0.04)
		tween.tween_property(label, "position:x", -46.0 + 8.0, 0.04)
		tween.tween_property(label, "position:x", -46.0, 0.04)
