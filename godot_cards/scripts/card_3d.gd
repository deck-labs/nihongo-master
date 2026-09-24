class_name Card3D
extends Node3D

@export var card_id: int = 0
@export var hand_index: int = 0
@export var kana: String = "あ"

var is_selected: bool = false
var select_order: int = 0
var is_hovered: bool = false

var base_pos: Vector3 = Vector3.ZERO
var base_rot: Vector3 = Vector3(24.0, 0, 0)
var current_tween: Tween = null

var mesh_inst: MeshInstance3D = null
@onready var viewport: SubViewport = $SubViewport
@onready var lbl_main: Label = $SubViewport/CardFace/MainKana
@onready var lbl_tl: Label = $SubViewport/CardFace/TopLeftKana
@onready var lbl_br: Label = $SubViewport/CardFace/BottomRightKana
@onready var badge_rect: ColorRect = $SubViewport/CardFace/Badge
@onready var badge_lbl: Label = $SubViewport/CardFace/Badge/BadgeNumber
@onready var border_rect: ReferenceRect = $SubViewport/CardFace/Border

var face_material: StandardMaterial3D = null

func _ready():
	mesh_inst = find_child("PlayingCard", true, false) as MeshInstance3D
	if not mesh_inst:
		for c in find_children("*", "MeshInstance3D", true, false):
			mesh_inst = c as MeshInstance3D
			break
	_setup_materials()
	set_kana(kana)

func _setup_materials():
	if mesh_inst and viewport:
		var vp_tex = viewport.get_texture()
		face_material = StandardMaterial3D.new()
		face_material.albedo_texture = vp_tex
		face_material.roughness = 0.35
		mesh_inst.set_surface_override_material(0, face_material)

func set_kana(new_kana: String):
	kana = new_kana
	if lbl_main: lbl_main.text = new_kana
	if lbl_tl: lbl_tl.text = new_kana
	if lbl_br: lbl_br.text = new_kana
	update_order_badge()

func set_order(order_num: int):
	select_order = order_num
	is_selected = (order_num > 0)
	update_order_badge()

func update_order_badge():
	if badge_rect and badge_lbl:
		badge_rect.visible = is_selected
		badge_lbl.text = str(select_order)

func set_hovered(hover: bool):
	is_hovered = hover
	if border_rect:
		border_rect.border_color = Color(1.0, 0.80, 0.22, 1.0) if hover else Color(0.85, 0.8, 0.72, 1.0)
		border_rect.border_width = 7.0 if hover else 3.0
		
	var target_y = base_pos.y + (0.26 if hover else 0.0)
	var target_rx = base_rot.x + (-12.0 if hover else 0.0)

	if current_tween and current_tween.is_valid():
		current_tween.kill()
	current_tween = create_tween().set_parallel(true).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	current_tween.tween_property(self, "position:y", target_y, 0.16)
	current_tween.tween_property(self, "rotation_degrees:x", target_rx, 0.16)

func glide_to(target_p: Vector3, target_r: Vector3 = Vector3.ZERO, duration: float = 0.28):
	base_pos = target_p
	base_rot = target_r
	
	var final_y = target_p.y + (0.24 if is_hovered else 0.0)
	var final_rx = target_r.x + (-14.0 if is_hovered else 0.0)

	if current_tween and current_tween.is_valid():
		current_tween.kill()
	current_tween = create_tween().set_parallel(true).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	current_tween.tween_property(self, "position:x", target_p.x, duration)
	current_tween.tween_property(self, "position:y", final_y, duration)
	current_tween.tween_property(self, "position:z", target_p.z, duration)
	current_tween.tween_property(self, "rotation_degrees", Vector3(final_rx, target_r.y, target_r.z), duration)

func shake():
	if current_tween and current_tween.is_valid():
		current_tween.kill()
	current_tween = create_tween().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
	current_tween.tween_property(self, "rotation_degrees:z", 10.0, 0.06)
	current_tween.tween_property(self, "rotation_degrees:z", -10.0, 0.06)
	current_tween.tween_property(self, "rotation_degrees:z", 8.0, 0.06)
	current_tween.tween_property(self, "rotation_degrees:z", -8.0, 0.06)
	current_tween.tween_property(self, "rotation_degrees:z", 0.0, 0.06)
