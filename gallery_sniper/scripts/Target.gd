extends Area2D
## Target.gd
## Represents an individual shooting gallery target displaying a Kana character.
## Emits target_clicked(character) when shot by the player.

signal target_clicked(character: String)

var character: String = ""
var is_active: bool = true

@onready var label: Label = $Label
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	# Ensure the target can receive mouse input
	input_pickable = true
	# Initial pop-in animation
	scale = Vector2(0.1, 0.1)
	var tween = create_tween().set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tween.tween_property(self, "scale", Vector2.ONE, 0.25)

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

## Target hits are evaluated centrally by Crosshair and Main.gd
func _input_event(_viewport: Node, _event: InputEvent, _shape_idx: int) -> void:
	pass

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
