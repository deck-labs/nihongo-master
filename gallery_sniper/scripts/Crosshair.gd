extends Node2D
## Crosshair.gd
## Custom sniper scope reticle supporting Mouse, Steam Deck Trackpads, and Gamepad analog sticks.
## Automatically hides hardware cursor, provides smooth analog steering, and recoil punch.

signal shot_requested(at_position: Vector2)

var reticle_color: Color = Color(1.0, 0.25, 0.25, 0.95)
var reticle_radius: float = 24.0

## Gamepad analog stick steering
var gamepad_speed: float = 950.0 # Pixels per second
var is_gamepad_mode: bool = false
var last_mouse_pos: Vector2 = Vector2.ZERO
var target_pos: Vector2 = Vector2(640, 400)
var trigger_was_pressed: bool = false

func _ready() -> void:
	Input.set_mouse_mode(Input.MOUSE_MODE_HIDDEN)
	z_index = 100 # Keep reticle on top of all targets and background
	target_pos = get_viewport_rect().size / 2.0
	global_position = target_pos
	last_mouse_pos = get_global_mouse_position()

func _process(delta: float) -> void:
	if not visible or get_tree().paused:
		return
	
	# 1. Read Gamepad analog sticks and D-Pad
	var stick_vec: Vector2 = Vector2.ZERO
	
	# Left analog stick
	var lx = Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
	var ly = Input.get_joy_axis(0, JOY_AXIS_LEFT_Y)
	if Vector2(lx, ly).length() > 0.15:
		stick_vec += Vector2(lx, ly)
	
	# Right analog stick
	var rx = Input.get_joy_axis(0, JOY_AXIS_RIGHT_X)
	var ry = Input.get_joy_axis(0, JOY_AXIS_RIGHT_Y)
	if Vector2(rx, ry).length() > 0.15:
		stick_vec += Vector2(rx, ry)
	
	# Gamepad D-Pad
	if Input.is_joy_button_pressed(0, JOY_BUTTON_DPAD_LEFT):
		stick_vec.x -= 1.0
	if Input.is_joy_button_pressed(0, JOY_BUTTON_DPAD_RIGHT):
		stick_vec.x += 1.0
	if Input.is_joy_button_pressed(0, JOY_BUTTON_DPAD_UP):
		stick_vec.y -= 1.0
	if Input.is_joy_button_pressed(0, JOY_BUTTON_DPAD_DOWN):
		stick_vec.y += 1.0

	var mouse_pos = get_global_mouse_position()
	var mouse_delta = mouse_pos.distance_to(last_mouse_pos)

	if mouse_delta > 1.5:
		# Player is using Mouse or Steam Deck Touchscreen/Trackpad
		is_gamepad_mode = false
		target_pos = mouse_pos
		last_mouse_pos = mouse_pos
	elif stick_vec.length() > 0.1:
		# Player is using Gamepad analog stick
		is_gamepad_mode = true
		var stick_magnitude = minf(stick_vec.length(), 1.0)
		# Quadratic response curve for precision aiming
		var speed_factor = stick_magnitude * stick_magnitude
		target_pos += stick_vec.normalized() * (gamepad_speed * speed_factor) * delta
		
		# Clamp to screen boundaries
		var vp = get_viewport_rect().size
		target_pos.x = clampf(target_pos.x, 30.0, vp.x - 30.0)
		target_pos.y = clampf(target_pos.y, 30.0, vp.y - 30.0)
		
		get_viewport().warp_mouse(target_pos)
		last_mouse_pos = target_pos

	global_position = target_pos

func _input(event: InputEvent) -> void:
	if not visible or get_tree().paused:
		return
	
	# Mouse click recoil
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		play_shot_recoil()
	
	# Gamepad button triggers (A, X)
	elif event is InputEventJoypadButton and event.pressed:
		if event.button_index in [JOY_BUTTON_A, JOY_BUTTON_X]:
			play_shot_recoil()
			shot_requested.emit(global_position)

	
	# Gamepad analog trigger triggers (RT, LT)
	elif event is InputEventJoypadMotion:
		if (event.axis == JOY_AXIS_TRIGGER_RIGHT or event.axis == JOY_AXIS_TRIGGER_LEFT):
			if event.axis_value > 0.5 and not trigger_was_pressed:
				trigger_was_pressed = true
				play_shot_recoil()
				shot_requested.emit(global_position)
			elif event.axis_value < 0.2:
				trigger_was_pressed = false

func _draw() -> void:
	# 1. Subtle illuminated outer ring
	draw_arc(Vector2.ZERO, reticle_radius, 0, TAU, 32, reticle_color, 2.0, true)
	
	# 2. Outer bracket notches
	draw_arc(Vector2.ZERO, reticle_radius + 6.0, -PI/6, PI/6, 8, Color(reticle_color.r, reticle_color.g, reticle_color.b, 0.6), 1.5)
	draw_arc(Vector2.ZERO, reticle_radius + 6.0, PI - PI/6, PI + PI/6, 8, Color(reticle_color.r, reticle_color.g, reticle_color.b, 0.6), 1.5)
	
	# 3. Precision crosshair hair lines with central gap
	var gap = 7.0
	var length = 18.0
	# Top line
	draw_line(Vector2(0, -gap), Vector2(0, -gap - length), reticle_color, 2.0)
	# Bottom line
	draw_line(Vector2(0, gap), Vector2(0, gap + length), reticle_color, 2.0)
	# Left line
	draw_line(Vector2(-gap, 0), Vector2(-gap - length, 0), reticle_color, 2.0)
	# Right line
	draw_line(Vector2(gap, 0), Vector2(gap + length, 0), reticle_color, 2.0)
	
	# 4. Center pin-point red dot
	draw_circle(Vector2.ZERO, 2.5, Color(1.0, 0.95, 0.95, 1.0))

## Visual recoil feedback when clicking / shooting
func play_shot_recoil() -> void:
	scale = Vector2(1.3, 1.3)
	var tween = create_tween().set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tween.tween_property(self, "scale", Vector2.ONE, 0.15)
