"""
hud_renderer.py
Renders the Left GPS Radar, Right Command Deck, NES Title Screen, Volume Menu, and Game Overlays.
"""

import math
import time
import pygame
from game_config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TOTAL_STAGES, STAGE_NAMES, STAGE_ENV_NOTES,
    COLOR_PANEL_BG, COLOR_PANEL_BORDER, COLOR_GOLD, COLOR_CYAN, COLOR_WHITE,
    GAME_VERSION, TOTAL_GAUNTLET_KANA, get_asset_path
)

class HudRenderer:
    def __init__(self, font_latin: pygame.font.Font, font_cjk: pygame.font.Font):
        self.font_latin = font_latin
        self.font_cjk = font_cjk
        
        # Load carbon texture
        self.tex_carbon = None
        c_path = get_asset_path("textures/carbon.png")
        try:
            raw = pygame.image.load(c_path).convert_alpha()
            self.tex_carbon = raw
        except Exception as e:
            print(f"Warning: Failed to load carbon texture: {e}")

        # Load 8-bit retro arcade title logo
        self.spr_title_logo = None
        logo_path = get_asset_path("sprites/title_logo_8bit.png")
        try:
            raw_logo = pygame.image.load(logo_path).convert_alpha()
            orig_w, orig_h = raw_logo.get_size()
            target_w = 860
            target_h = int(target_w * (orig_h / orig_w))
            self.spr_title_logo = pygame.transform.smoothscale(raw_logo, (target_w, target_h))
        except Exception as e:
            print(f"Warning: Failed to load title logo: {e}")

        # Scaled fonts optimized for high-DPI and handheld (Steam Deck OLED) readability
        self.font_title = pygame.font.Font(get_asset_path("fonts/DejaVuSans-Bold.ttf"), 60)
        self.font_kana_title = pygame.font.Font(get_asset_path("fonts/NotoSansCJK-Bold.ttc"), 36)
        self.font_menu = pygame.font.Font(get_asset_path("fonts/DejaVuSans-Bold.ttf"), 32)
        self.font_large_kana = pygame.font.Font(get_asset_path("fonts/NotoSansCJK-Bold.ttc"), 92)
        self.font_speed = pygame.font.Font(get_asset_path("fonts/DejaVuSans-Bold.ttf"), 54)
        self.font_version = pygame.font.Font(get_asset_path("fonts/DejaVuSans-Bold.ttf"), 22)
        self.font_sub = pygame.font.Font(get_asset_path("fonts/DejaVuSans-Bold.ttf"), 22)
        self.font_stage_name = pygame.font.Font(get_asset_path("fonts/DejaVuSans-Bold.ttf"), 20)
        self.font_caption = pygame.font.Font(get_asset_path("fonts/DejaVuSans-Bold.ttf"), 18)
        self.font_desc = pygame.font.Font(get_asset_path("fonts/DejaVuSans-Bold.ttf"), 15)
        self.font_tiny = self.font_caption  # High-contrast 18pt font alias for handheld readability

    def draw_tiled_carbon(self, surface: pygame.Surface, rect: tuple[int, int, int, int]):
        rx, ry, rw, rh = rect
        if self.tex_carbon:
            tw, th = self.tex_carbon.get_size()
            surface.set_clip(pygame.Rect(rx, ry, rw, rh))
            for x in range(rx, rx + rw, tw):
                for y in range(ry, ry + rh, th):
                    surface.blit(self.tex_carbon, (x, y))
            surface.set_clip(None)
        else:
            pygame.draw.rect(surface, COLOR_PANEL_BG, (rx, ry, rw, rh))

    def render_left_panel(self, surface: pygame.Surface, stage: int, track_dist: float, max_dist: float):
        scr_h = surface.get_height()
        # 0 to 280 px
        self.draw_tiled_carbon(surface, (0, 0, 280, scr_h))
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (280, 0), (280, scr_h), 2)
        
        # Stage Header Box (Balanced spacing, zero collisions, clean centering)
        st_rect = pygame.Rect(14, 14, 252, 130)
        pygame.draw.rect(surface, (10, 20, 36), st_rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_GOLD, st_rect, 2, border_radius=6)
        
        if stage == 11:
            txt_st = self.font_menu.render("BONUS STAGE", True, COLOR_GOLD)
        else:
            txt_st = self.font_menu.render(f"STAGE {stage:02d}", True, COLOR_GOLD)
        surface.blit(txt_st, txt_st.get_rect(center=(140, 38)))
        
        st_name = STAGE_NAMES.get(stage, "HIGHWAY")
        txt_name = self.font_stage_name.render(st_name, True, COLOR_CYAN)
        surface.blit(txt_name, txt_name.get_rect(center=(140, 76)))
        
        txt_tele = self.font_caption.render("ALL-KANA GAUNTLET" if stage == 11 else "GPS TRACK TELEMETRY", True, (180, 220, 250))
        surface.blit(txt_tele, txt_tele.get_rect(center=(140, 112)))
        
        # Dedicated Bottom Distance Telemetry Card
        card_x = 16
        card_w = 248
        card_h = 185
        card_y = scr_h - card_h - 20
        card_rect = pygame.Rect(card_x, card_y, card_w, card_h)
        pygame.draw.rect(surface, (8, 16, 28), card_rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, card_rect, 2, border_radius=8)

        # Vertical Mini-Map Track
        track_x = 155
        track_top = 182
        track_bot = card_y - 48
        track_len = track_bot - track_top
        
        # Goal Badge
        goal_rect = pygame.Rect(95, track_top - 30, 120, 26)
        pygame.draw.rect(surface, (10, 20, 36), goal_rect, border_radius=4)
        pygame.draw.rect(surface, COLOR_GOLD, goal_rect, 1, border_radius=4)
        txt_goal = self.font_caption.render("★ GOAL ★", True, COLOR_GOLD)
        surface.blit(txt_goal, txt_goal.get_rect(center=goal_rect.center))
        
        # Center line
        pygame.draw.line(surface, (75, 100, 130), (track_x, track_top), (track_x, track_bot), 3)
        
        # Milestone markers (25%, 50%, 75%)
        for q in [0.25, 0.5, 0.75]:
            qy = int(track_bot - (track_len * q))
            pygame.draw.line(surface, COLOR_CYAN, (track_x - 16, qy), (track_x + 16, qy), 2)
            txt_q = self.font_caption.render(f"{int(q * 100)}%", True, COLOR_WHITE)
            surface.blit(txt_q, (24, qy - 18))
            q_dist = int((max_dist * (1.0 - q)) * 0.1)
            txt_qd = self.font_caption.render(f"{q_dist}m", True, (160, 210, 250))
            surface.blit(txt_qd, (24, qy + 2))
            
        # Start Badge
        start_rect = pygame.Rect(105, track_bot + 8, 100, 28)
        pygame.draw.rect(surface, (10, 20, 36), start_rect, border_radius=4)
        pygame.draw.rect(surface, COLOR_CYAN, start_rect, 1, border_radius=4)
        txt_start = self.font_caption.render("START", True, COLOR_CYAN)
        surface.blit(txt_start, txt_start.get_rect(center=start_rect.center))
        
        # Player Cursor (Sports car beacon)
        progress = max(0.0, min(1.0, track_dist / max_dist))
        cur_y = int(track_bot - (track_len * progress))
        # Beacon pulse ring
        pygame.draw.rect(surface, (0, 200, 255), (track_x - 12, cur_y - 12, 24, 24), 1, border_radius=3)
        # Car icon
        pygame.draw.rect(surface, (220, 35, 35), (track_x - 7, cur_y - 9, 14, 18), border_radius=3)
        pygame.draw.rect(surface, (255, 255, 255), (track_x - 4, cur_y - 6, 8, 8), border_radius=2)
        # 'YOU' label
        you_rect = pygame.Rect(track_x + 18, cur_y - 12, 54, 24)
        pygame.draw.rect(surface, COLOR_GOLD, you_rect, border_radius=3)
        txt_you = self.font_caption.render("YOU", True, (0, 0, 0))
        surface.blit(txt_you, txt_you.get_rect(center=you_rect.center))

        txt_dh = self.font_caption.render("REMAINING DISTANCE", True, (210, 235, 255))
        surface.blit(txt_dh, txt_dh.get_rect(center=(card_x + card_w // 2, card_y + 22)))

        remaining_m = int(max(0.0, (max_dist - track_dist) * 0.1))
        txt_m = self.font_speed.render(f"{remaining_m:,} M", True, COLOR_GOLD)
        surface.blit(txt_m, txt_m.get_rect(center=(card_x + card_w // 2, card_y + 64)))

        pct_val = int(round(progress * 100))
        txt_pct = self.font_sub.render(f"{pct_val}% COMPLETED", True, COLOR_CYAN)
        surface.blit(txt_pct, txt_pct.get_rect(center=(card_x + card_w // 2, card_y + 112)))

        # Progress bar
        bar_bx = card_x + 18
        bar_by = card_y + 144
        bar_bw = card_w - 36
        bar_bh = 22
        pygame.draw.rect(surface, (16, 26, 42), (bar_bx, bar_by, bar_bw, bar_bh), border_radius=4)
        p_fill = int(bar_bw * progress)
        if p_fill > 0:
            pygame.draw.rect(surface, (0, 217, 255), (bar_bx, bar_by, p_fill, bar_bh), border_radius=4)
        pygame.draw.rect(surface, (60, 90, 130), (bar_bx, bar_by, bar_bw, bar_bh), 1, border_radius=4)

    def render_right_panel(self, surface: pygame.Surface, stage: int, target_kana: str, target_romaji: str,
                           speed_kmh: float, is_turbo: bool, is_braking: bool, fuel: float, score: float, match_timer: float,
                           flawless_active: bool = False, damage_taken: bool = False, gauntlet_count: int = 0,
                           game_mode: str = "hiragana"):
        # 1240 to 1920 px (width 680)
        scr_h = surface.get_height()
        self.draw_tiled_carbon(surface, (1240, 0, 680, scr_h))
        pygame.draw.line(surface, COLOR_PANEL_BORDER, (1240, 0), (1240, scr_h), 2)
        
        rx = 1260
        rw = 640
        
        # 1. Target Kana Holographic Chamber
        box_y = 20
        box_h = 245
        chamber_rect = pygame.Rect(rx, box_y, rw, box_h)
        pygame.draw.rect(surface, (8, 16, 28), chamber_rect)
        border_col = COLOR_GOLD if match_timer > 0.0 else COLOR_CYAN
        pygame.draw.rect(surface, border_col, chamber_rect, 2)
        
        # Header text
        if stage == 11:
            txt_tgt_h = self.font_sub.render("★ ALL-KANA & DAKUTEN GAUNTLET TARGET ★", True, COLOR_GOLD)
        else:
            txt_tgt_h = self.font_sub.render("TARGET KANA INTERCEPT TARGET", True, COLOR_CYAN)
        surface.blit(txt_tgt_h, (rx + 20, box_y + 12))
        
        # Huge Kana character
        if self.font_large_kana and target_kana:
            k_surf = self.font_large_kana.render(target_kana, True, COLOR_GOLD if match_timer > 0.0 else COLOR_WHITE)
            kr = k_surf.get_rect(center=(rx + rw // 2, box_y + 105))
            surface.blit(k_surf, kr)
            
        # Romaji pronunciation guide (high-contrast pill plate)
        ro_box = pygame.Rect(rx + rw // 2 - 110, box_y + 162, 220, 42)
        pygame.draw.rect(surface, (12, 22, 38), ro_box, border_radius=6)
        pygame.draw.rect(surface, COLOR_CYAN, ro_box, 2, border_radius=6)
        txt_ro = self.font_menu.render(f"[ {target_romaji.upper()} ]", True, COLOR_GOLD)
        surface.blit(txt_ro, txt_ro.get_rect(center=ro_box.center))
        
        # Subtitle instruction
        if stage == 11:
            txt_sub = self.font_caption.render(f"MATCH TRAFFIC FOR ALL {TOTAL_GAUNTLET_KANA} KANA! (+100 PTS / +35% FUEL)", True, (255, 240, 180))
        else:
            txt_sub = self.font_caption.render("MATCH TRAFFIC ROOF ROMAJI TO REFUEL +30%", True, (230, 242, 255))
        sub_r = txt_sub.get_rect(center=(rx + rw // 2, box_y + 220))
        surface.blit(txt_sub, sub_r)
        
        # 2. Speedometer
        spd_y = 285
        spd_rect = pygame.Rect(rx, spd_y, rw, 150)
        pygame.draw.rect(surface, (8, 16, 28), spd_rect)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, spd_rect, 1)
        
        txt_spd_h = self.font_sub.render("VELOCITY TELEMETRY", True, (200, 225, 250))
        surface.blit(txt_spd_h, (rx + 20, spd_y + 12))
        
        # Speed readout
        s_val = int(speed_kmh)
        txt_s_val = self.font_speed.render(f"{s_val:03d}", True, COLOR_GOLD if is_turbo else COLOR_WHITE)
        surface.blit(txt_s_val, (rx + 24, spd_y + 40))
        txt_unit = self.font_sub.render("KM/H", True, COLOR_CYAN)
        surface.blit(txt_unit, (rx + 155, spd_y + 56))
        
        # State Badge
        if is_braking:
            badge_text = "BRAKING"
            badge_col = (255, 70, 70)
        elif is_turbo:
            badge_text = "TURBO BOOST"
            badge_col = COLOR_GOLD
        else:
            badge_text = "CRUISE DRIVE"
            badge_col = COLOR_CYAN
            
        txt_badge = self.font_sub.render(badge_text, True, badge_col)
        surface.blit(txt_badge, (rx + rw - 220, spd_y + 56))
        
        # Speed Segment Bar (160 cruise / 240 max turbo)
        bar_x = rx + 24
        bar_y = spd_y + 105
        bar_w = rw - 48
        bar_h = 24
        pygame.draw.rect(surface, (16, 26, 42), (bar_x, bar_y, bar_w, bar_h))
        
        fill_ratio = min(1.0, speed_kmh / 264.0)
        fill_w = int(bar_w * fill_ratio)
        if fill_w > 0:
            b_col = COLOR_GOLD if is_turbo else (0, 210, 255)
            pygame.draw.rect(surface, b_col, (bar_x, bar_y, fill_w, bar_h))
        pygame.draw.rect(surface, (80, 120, 160), (bar_x, bar_y, bar_w, bar_h), 1)
        
        # 3. Battery / Fuel Level
        fuel_y = 455
        fuel_rect = pygame.Rect(rx, fuel_y, rw, 150)
        pygame.draw.rect(surface, (8, 16, 28), fuel_rect)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, fuel_rect, 1)
        
        txt_f_h = self.font_sub.render("FUEL ENERGY CELL (WRONG CAR: -15%)", True, (200, 225, 250))
        surface.blit(txt_f_h, (rx + 20, fuel_y + 12))
        
        # Fuel %
        f_int = int(fuel)
        if fuel > 50.0:
            f_col = (46, 224, 125)
        elif fuel > 25.0:
            f_col = COLOR_GOLD
        else:
            f_col = (255, 65, 65)
            
        txt_f_val = self.font_speed.render(f"{f_int}%", True, f_col)
        surface.blit(txt_f_val, (rx + 24, fuel_y + 40))
        
        # 10 Fuel Battery Blocks
        bx_start = rx + 24
        by = fuel_y + 105
        total_cells = 10
        gap = 6
        cell_w = int((rw - 48 - (gap * (total_cells - 1))) / total_cells)
        active_cells = int(round((fuel / 100.0) * total_cells))
        
        for c in range(total_cells):
            cx = bx_start + c * (cell_w + gap)
            is_active = (c < active_cells)
            cell_col = f_col if is_active else (25, 35, 50)
            pygame.draw.rect(surface, cell_col, (cx, by, cell_w, 26), border_radius=3)
            pygame.draw.rect(surface, (70, 100, 135), (cx, by, cell_w, 26), 1, border_radius=3)
            
        # 4. Mission Telemetry / Score
        score_y = 625
        sc_rect = pygame.Rect(rx, score_y, rw, 140)
        pygame.draw.rect(surface, (8, 16, 28), sc_rect)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, sc_rect, 1)
        
        txt_sc_h = self.font_sub.render("TACTICAL SCORE TELEMETRY", True, (200, 225, 250))
        surface.blit(txt_sc_h, (rx + 20, score_y + 12))
        
        txt_sc_val = self.font_speed.render(f"{int(score):06d}", True, COLOR_GOLD)
        surface.blit(txt_sc_val, (rx + 24, score_y + 45))

        # Stage 11 Gauntlet Progress Badge
        if stage == 11:
            badge_rect = pygame.Rect(rx + rw - 310, score_y + 36, 290, 48)
            pygame.draw.rect(surface, (24, 16, 48), badge_rect, border_radius=6)
            pygame.draw.rect(surface, (255, 215, 0), badge_rect, 2, border_radius=6)
            txt_b1 = self.font_sub.render(f"GAUNTLET: {gauntlet_count} / {TOTAL_GAUNTLET_KANA}", True, (255, 220, 50))
            surface.blit(txt_b1, txt_b1.get_rect(center=badge_rect.center))
        
        env_note = STAGE_ENV_NOTES.get(stage, "")
        txt_env = self.font_caption.render(env_note, True, (190, 220, 250))
        surface.blit(txt_env, (rx + 24, score_y + 110))
        
        # 5. Controls Guide Deck (Dynamically scaled to 16:10 canvas)
        ctrl_y = 800
        ctrl_h = max(285, scr_h - ctrl_y - 20)
        c_rect = pygame.Rect(rx, ctrl_y, rw, ctrl_h)
        pygame.draw.rect(surface, (8, 16, 28), c_rect)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, c_rect, 1)
        
        txt_c_h = self.font_sub.render("FLIGHT CONTROLS & COMMANDS", True, COLOR_CYAN)
        surface.blit(txt_c_h, (rx + 20, ctrl_y + 16))
        pygame.draw.line(surface, (0, 140, 210), (rx + 20, ctrl_y + 44), (rx + rw - 20, ctrl_y + 44), 1)
        
        mode_str = "HIRAGANA" if game_mode == "hiragana" else "KATAKANA"
        goal_msg = f"BONUS GOAL: CONQUER ALL {TOTAL_GAUNTLET_KANA} {mode_str} & DAKUTEN!" if stage == 11 else f"TARGET GOAL: 36,000 M // {TOTAL_STAGES} TOTAL STAGES"
        lines = [
            "STEER: [A / D] / [LEFT / RIGHT] / D-PAD / ANALOG STICK",
            "TURBO BOOST: [W] / [UP] / [SPACE] / GAMEPAD [A] / [RT]",
            "BRAKE / SLOW: [S] / [DOWN] / GAMEPAD [X] / [LT]",
            "OPTIONS / AUDIO: [ESC] / [ENTER] / GAMEPAD [START]",
            "QUICK PAUSE: [P] / GAMEPAD [SELECT]",
            "QUIT TO DESKTOP: GAMEPAD [SELECT + START]",
            goal_msg
        ]
        line_spacing = 40 if ctrl_h >= 350 else 33
        line_start = ctrl_y + 58 if ctrl_h >= 350 else ctrl_y + 48
        for idx, line in enumerate(lines):
            txt_l = self.font_caption.render(line, True, (235, 245, 255))
            surface.blit(txt_l, (rx + 20, line_start + idx * line_spacing))

    def render_title_screen(self, surface: pygame.Surface, menu_index: int, selected_stage: int,
                            game_mode: str = "hiragana", display_info: str = ""):
        # Solid dark arcade canvas
        surface.fill((8, 12, 22))
        surface_w = surface.get_width()
        surface_h = surface.get_height()
        cx = surface_w // 2
        
        # Current Version Running Indicator (Upper-Left)
        ver_text = f"VERSION {GAME_VERSION}"
        txt_ver = self.font_version.render(ver_text, True, (180, 230, 255))
        badge_w = txt_ver.get_width() + 28
        badge_h = txt_ver.get_height() + 14
        badge_rect = pygame.Rect(40, 32, badge_w, badge_h)
        pygame.draw.rect(surface, (12, 22, 38), badge_rect, border_radius=6)
        pygame.draw.rect(surface, (0, 160, 240), badge_rect, 2, border_radius=6)
        surface.blit(txt_ver, txt_ver.get_rect(center=badge_rect.center))
        
        # 1. 8-Bit Title Logo or Retro Chromatic Fallback
        if self.spr_title_logo:
            logo_rect = self.spr_title_logo.get_rect(center=(cx, 260))
            surface.blit(self.spr_title_logo, logo_rect)
            sub_y = logo_rect.bottom + 26
            pill_y = sub_y
            div_y = sub_y + 50
            menu_y_start = sub_y + 104
            spacing = 64
        else:
            title_text = "NIHONGO MASTER"
            title_y = int(surface_h * 0.22)
            t_b = self.font_title.render(title_text, True, (0, 0, 0))
            surface.blit(t_b, t_b.get_rect(center=(cx, title_y + 4)))
            t_r = self.font_title.render(title_text, True, (215, 38, 38))
            surface.blit(t_r, t_r.get_rect(center=(cx, title_y + 2)))
            t_g = self.font_title.render(title_text, True, COLOR_GOLD)
            surface.blit(t_g, t_g.get_rect(center=(cx, title_y)))
            sub_text = "日本語  マスター"
            sub_y = title_y + 68
            t_k = self.font_kana_title.render(sub_text, True, COLOR_CYAN)
            surface.blit(t_k, t_k.get_rect(center=(cx, sub_y)))
            pill_y = sub_y + 44
            div_y = sub_y + 94
            menu_y_start = sub_y + 148
            spacing = 68

        # Active Mode Banner Pill
        is_hiragana = (game_mode == "hiragana")
        mode_tag = "★ HIRAGANA MASTER MODE ★" if is_hiragana else "★ KATAKANA MASTER MODE ★"
        mode_col = (0, 225, 255) if is_hiragana else (255, 175, 45)
        txt_m_tag = self.font_sub.render(mode_tag, True, mode_col)
        pill_w = txt_m_tag.get_width() + 40
        pill_h = 36
        pill_rect = pygame.Rect(cx - pill_w // 2, pill_y, pill_w, pill_h)
        pygame.draw.rect(surface, (14, 22, 38), pill_rect, border_radius=18)
        pygame.draw.rect(surface, mode_col, pill_rect, 2, border_radius=18)
        surface.blit(txt_m_tag, txt_m_tag.get_rect(center=pill_rect.center))
        
        # Divider line
        pygame.draw.line(surface, (0, 140, 220), (cx - 380, div_y), (cx + 380, div_y), 2)
        
        # 3. Menu Items with 200ms NES Blinking (16:10 spacious vertical layout)
        is_blink = (int(time.time() * 1000) // 200) % 2 == 0
        
        # Item 0: GAME MODE
        is_sel_0 = (menu_index == 0)
        col0 = COLOR_WHITE if (is_sel_0 and is_blink) else (COLOR_GOLD if is_sel_0 else (210, 230, 250))
        cur_mode_str = "HIRAGANA MASTER" if is_hiragana else "KATAKANA MASTER"
        txt_0 = self.font_menu.render(f"GAME MODE   ◄  {cur_mode_str}  ►", True, col0)
        r0 = txt_0.get_rect(center=(cx, menu_y_start))
        if is_sel_0 and is_blink:
            arrow = self.font_menu.render("►", True, COLOR_GOLD)
            surface.blit(arrow, (r0.left - 45, r0.top))
        surface.blit(txt_0, r0)

        # Item 1: START
        is_sel_1 = (menu_index == 1)
        col1 = COLOR_WHITE if (is_sel_1 and is_blink) else (COLOR_GOLD if is_sel_1 else (210, 230, 250))
        start_lbl = "START HIRAGANA" if is_hiragana else "START KATAKANA"
        txt_1 = self.font_menu.render(start_lbl, True, col1)
        r1 = txt_1.get_rect(center=(cx, menu_y_start + spacing))
        if is_sel_1 and is_blink:
            arrow = self.font_menu.render("►", True, COLOR_GOLD)
            surface.blit(arrow, (r1.left - 45, r1.top))
        surface.blit(txt_1, r1)
        
        # Item 2: STAGE SELECT
        is_sel_2 = (menu_index == 2)
        col2 = COLOR_WHITE if (is_sel_2 and is_blink) else (COLOR_GOLD if is_sel_2 else (210, 230, 250))
        if selected_stage == 11:
            st_name = "★ RAINBOW SKYWAY ★"
            st_str = f"STAGE SELECT   ◄  BONUS TRIAL : {st_name}  ►" if is_sel_2 else "STAGE SELECT   < BONUS TRIAL : ★ SECRET ★ >"
        else:
            st_name = STAGE_NAMES.get(selected_stage, "STAGE 01")
            st_str = f"STAGE SELECT   ◄  STAGE {selected_stage:02d} : {st_name}  ►" if is_sel_2 else f"STAGE SELECT   < STAGE {selected_stage:02d} >"
        txt_2 = self.font_menu.render(st_str, True, col2)
        r2 = txt_2.get_rect(center=(cx, menu_y_start + spacing * 2))
        if is_sel_2 and is_blink:
            arrow = self.font_menu.render("►", True, COLOR_GOLD)
            surface.blit(arrow, (r2.left - 45, r2.top))
        surface.blit(txt_2, r2)
        
        # Item 3: OPTIONS
        is_sel_3 = (menu_index == 3)
        col3 = COLOR_WHITE if (is_sel_3 and is_blink) else (COLOR_GOLD if is_sel_3 else (210, 230, 250))
        txt_3 = self.font_menu.render("OPTIONS", True, col3)
        r3 = txt_3.get_rect(center=(cx, menu_y_start + spacing * 3))
        if is_sel_3 and is_blink:
            arrow = self.font_menu.render("►", True, COLOR_GOLD)
            surface.blit(arrow, (r3.left - 45, r3.top))
        surface.blit(txt_3, r3)

        # Item 4: CHECK FOR UPDATES
        is_sel_4 = (menu_index == 4)
        col4 = COLOR_WHITE if (is_sel_4 and is_blink) else (COLOR_GOLD if is_sel_4 else (210, 230, 250))
        txt_4 = self.font_menu.render("CHECK FOR UPDATES", True, col4)
        r4 = txt_4.get_rect(center=(cx, menu_y_start + spacing * 4))
        if is_sel_4 and is_blink:
            arrow = self.font_menu.render("►", True, COLOR_GOLD)
            surface.blit(arrow, (r4.left - 45, r4.top))
        surface.blit(txt_4, r4)

        # Item 5: QUIT
        is_sel_5 = (menu_index == 5)
        col5 = COLOR_WHITE if (is_sel_5 and is_blink) else (COLOR_GOLD if is_sel_5 else (210, 230, 250))
        txt_5 = self.font_menu.render("QUIT", True, col5)
        r5 = txt_5.get_rect(center=(cx, menu_y_start + spacing * 5))
        if is_sel_5 and is_blink:
            arrow = self.font_menu.render("►", True, COLOR_GOLD)
            surface.blit(arrow, (r5.left - 45, r5.top))
        surface.blit(txt_5, r5)

        # Display Mode Badge (Bottom-Left)
        if display_info:
            txt_disp = self.font_caption.render(f"DISPLAY: {display_info}", True, (160, 210, 255))
            surface.blit(txt_disp, (40, surface_h - 48))

        # Footer
        txt_foot = self.font_caption.render("▲/▼ NAVIGATE   ◀/▶ ADJUST   [ENTER] / [A] / [START]: SELECT   [SELECT + START]: QUIT", True, (210, 235, 255))
        surface.blit(txt_foot, txt_foot.get_rect(center=(cx, surface_h - 60)))

    def render_volume_menu(self, surface: pygame.Surface, is_title_screen: bool, selected_idx: int,
                           master_vol: float, engine_vol: float, sfx_vol: float,
                           aspect_ratio_label: str = "16:10 (STANDARD)"):
        surface_w = surface.get_width()
        surface_h = surface.get_height()
        
        # 1. Full-screen dimmed backdrop for clarity & focus
        dim_surf = pygame.Surface((surface_w, surface_h), pygame.SRCALPHA)
        dim_surf.fill((5, 10, 18, 200))
        surface.blit(dim_surf, (0, 0))
        
        # 2. Centered cyber options dialog
        w = 780
        h = 600
        cx = surface_w // 2 if is_title_screen else 760
        cy = surface_h // 2
        x = cx - (w // 2)
        y = cy - (h // 2)
        
        # High-contrast dark backing
        modal_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        modal_surf.fill((10, 18, 32, 255))
        surface.blit(modal_surf, (x, y))
        
        # Cyber gold/cyan border
        pygame.draw.rect(surface, (0, 180, 240), (x, y, w, h), 3, border_radius=12)
        pygame.draw.rect(surface, (15, 30, 50), (x + 3, y + 3, w - 6, h - 6), 1, border_radius=10)
        
        # Header title
        title_str = "GAME OPTIONS & CONFIGURATION"
        txt_title = self.font_menu.render(title_str, True, COLOR_GOLD)
        surface.blit(txt_title, txt_title.get_rect(center=(cx, y + 40)))
        pygame.draw.line(surface, (0, 140, 210), (x + 30, y + 72), (x + w - 30, y + 72), 2)
        
        # Sliders: 0: Master, 1: Engine, 2: SFX
        items = [
            ("MASTER VOLUME", master_vol, 0),
            ("ENGINE VOLUME", engine_vol, 1),
            ("SFX VOLUME", sfx_vol, 2)
        ]
        
        start_sy = y + 92
        spacing_s = 72
        
        for name, vol, idx in items:
            sy = start_sy + idx * spacing_s
            is_sel = (selected_idx == idx)
            
            # Label
            lbl_col = COLOR_GOLD if is_sel else (220, 235, 255)
            prefix = "► " if is_sel else "  "
            txt_lbl = self.font_sub.render(prefix + name, True, lbl_col)
            surface.blit(txt_lbl, (x + 45, sy))
            
            # Value %
            pct = int(round(vol * 100))
            txt_pct = self.font_sub.render(f"{pct}%", True, COLOR_CYAN if is_sel else (180, 215, 245))
            surface.blit(txt_pct, (x + w - 115, sy))
            
            # Slider Track
            bx = x + 45
            by = sy + 30
            bw = w - 90
            bh = 18
            pygame.draw.rect(surface, (15, 25, 42), (bx, by, bw, bh), border_radius=4)
            fill_w = int(bw * max(0.0, min(1.0, vol)))
            if fill_w > 0:
                bar_col = (0, 220, 255) if is_sel else (0, 150, 200)
                pygame.draw.rect(surface, bar_col, (bx, by, fill_w, bh), border_radius=4)
            pygame.draw.rect(surface, (60, 100, 140), (bx, by, bw, bh), 1, border_radius=4)
            
            # Slider thumb knob
            kx = bx + fill_w
            pygame.draw.circle(surface, COLOR_GOLD if is_sel else COLOR_WHITE, (kx, by + bh // 2), 10)
            pygame.draw.circle(surface, (20, 30, 45), (kx, by + bh // 2), 10, 2)
            
        # Item 3: Aspect Ratio Selector
        ar_y = start_sy + 3 * spacing_s
        is_sel_ar = (selected_idx == 3)
        ar_col = COLOR_GOLD if is_sel_ar else (220, 235, 255)
        prefix_ar = "► " if is_sel_ar else "  "
        txt_ar_lbl = self.font_sub.render(prefix_ar + "ASPECT RATIO", True, ar_col)
        surface.blit(txt_ar_lbl, (x + 45, ar_y))

        ar_box = pygame.Rect(x + 45, ar_y + 28, w - 90, 36)
        pygame.draw.rect(surface, (15, 25, 42), ar_box, border_radius=6)
        pygame.draw.rect(surface, COLOR_GOLD if is_sel_ar else (60, 100, 140), ar_box, 1, border_radius=6)

        mode_str = f"◄  {aspect_ratio_label}  ►" if is_sel_ar else aspect_ratio_label
        txt_mode = self.font_sub.render(mode_str, True, COLOR_CYAN if is_sel_ar else COLOR_WHITE)
        surface.blit(txt_mode, txt_mode.get_rect(center=ar_box.center))

        if not is_title_screen:
            # Item 4: Resume Game Button
            btn1_y = y + 404
            btn1_sel = (selected_idx == 4)
            btn1_bg = (0, 110, 180) if btn1_sel else (18, 32, 50)
            btn1_rect = pygame.Rect(cx - 210, btn1_y, 420, 46)
            pygame.draw.rect(surface, btn1_bg, btn1_rect, border_radius=6)
            pygame.draw.rect(surface, COLOR_GOLD if btn1_sel else (40, 80, 120), btn1_rect, 2, border_radius=6)
            txt_b1 = self.font_sub.render("◄ RESUME GAME ►", True, COLOR_WHITE if btn1_sel else (200, 225, 245))
            surface.blit(txt_b1, txt_b1.get_rect(center=btn1_rect.center))

            # Item 5: Return to Title Button
            btn2_y = y + 462
            btn2_sel = (selected_idx == 5)
            btn2_bg = (160, 30, 30) if btn2_sel else (28, 20, 30)
            btn2_rect = pygame.Rect(cx - 210, btn2_y, 420, 46)
            pygame.draw.rect(surface, btn2_bg, btn2_rect, border_radius=6)
            pygame.draw.rect(surface, COLOR_GOLD if btn2_sel else (90, 50, 60), btn2_rect, 2, border_radius=6)
            txt_b2 = self.font_sub.render("◄ RETURN TO TITLE ►", True, COLOR_GOLD if btn2_sel else (230, 200, 210))
            surface.blit(txt_b2, txt_b2.get_rect(center=btn2_rect.center))
        else:
            # Item 4: Return to Title (Close)
            btn_y = y + 430
            btn_is_sel = (selected_idx == 4)
            btn_bg = (0, 110, 180) if btn_is_sel else (18, 32, 50)
            btn_rect = pygame.Rect(cx - 210, btn_y, 420, 50)
            pygame.draw.rect(surface, btn_bg, btn_rect, border_radius=6)
            pygame.draw.rect(surface, COLOR_GOLD if btn_is_sel else (40, 80, 120), btn_rect, 2, border_radius=6)
            txt_b = self.font_sub.render("◄ RETURN TO TITLE ►", True, COLOR_WHITE if btn_is_sel else (200, 225, 245))
            surface.blit(txt_b, txt_b.get_rect(center=btn_rect.center))
        
        # Navigation footer
        pygame.draw.line(surface, (0, 90, 150), (x + 30, y + 535), (x + w - 30, y + 535), 1)
        foot_str = "▲/▼ SELECT    ◀/▶ ADJUST    [ENTER] / [A]: SELECT    [B] / [ESC]: BACK"
        txt_foot = self.font_caption.render(foot_str, True, (180, 215, 245))
        surface.blit(txt_foot, txt_foot.get_rect(center=(cx, y + 565)))

    def render_pause_overlay(self, surface: pygame.Surface):
        is_blink = (int(time.time() * 1000) // 350) % 2 == 0
        surface_w = surface.get_width()
        surface_h = surface.get_height()
        cx = 760
        cy = surface_h // 2
        
        # Semi-transparent dark curtain across the road viewport
        dim_surf = pygame.Surface((960, surface_h), pygame.SRCALPHA)
        dim_surf.fill((0, 0, 0, 120))
        surface.blit(dim_surf, (280, 0))
        
        # Pause badge box (Generous margins for Steam Deck handheld readability)
        box_w = 640
        box_h = 150
        bg_rect = pygame.Rect(cx - box_w // 2, cy - box_h // 2, box_w, box_h)
        pygame.draw.rect(surface, (10, 15, 26), bg_rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_GOLD, bg_rect, 3, border_radius=10)
        
        col_p = COLOR_GOLD if is_blink else (170, 150, 25)
        txt_p = self.font_title.render("PAUSE", True, col_p)
        surface.blit(txt_p, txt_p.get_rect(center=(cx, cy - 24)))
        
        txt_sub = self.font_caption.render("SELECT / START: RESUME   |   SELECT + START: QUIT", True, COLOR_WHITE)
        surface.blit(txt_sub, txt_sub.get_rect(center=(cx, cy + 34)))

    def render_stage_clear_overlay(self, surface: pygame.Surface, stage: int, is_flawless_unlock: bool = False, game_mode: str = "hiragana"):
        surface_h = surface.get_height()
        cx = 760
        cy = surface_h // 2
        
        if stage == 11:
            # Stage 11 Cleared: Grand Master Victory Overlay
            box_w = 880
            box_h = 280
            r_box = pygame.Rect(cx - box_w // 2, cy - box_h // 2, box_w, box_h)
            pygame.draw.rect(surface, (14, 10, 32), r_box, border_radius=14)
            pygame.draw.rect(surface, (255, 215, 0), r_box, 3, border_radius=14)
            pygame.draw.rect(surface, (0, 220, 255), r_box.inflate(-8, -8), 1, border_radius=10)

            mode_str = "HIRAGANA" if game_mode == "hiragana" else "KATAKANA"
            txt_h = self.font_menu.render(f"★ ULTIMATE {mode_str} MASTER! ★", True, COLOR_GOLD)
            surface.blit(txt_h, txt_h.get_rect(center=(cx, cy - 65)))
            
            txt_m = self.font_sub.render(f"ALL {TOTAL_GAUNTLET_KANA} {mode_str} & DAKUTEN MASTERED!", True, (0, 240, 255))
            surface.blit(txt_m, txt_m.get_rect(center=(cx, cy - 15)))

            txt_s = self.font_caption.render("STAGE 11 SECRET TRIAL CONQUERED // PERFECT VICTORY", True, (255, 235, 130))
            surface.blit(txt_s, txt_s.get_rect(center=(cx, cy + 30)))
            
            txt_f = self.font_caption.render("PRESS [SPACE] / [ENTER] / GAMEPAD [A] FOR TITLE SCREEN", True, COLOR_WHITE)
            surface.blit(txt_f, txt_f.get_rect(center=(cx, cy + 85)))

        elif stage == TOTAL_STAGES and is_flawless_unlock:
            # Stage 10 Cleared on Flawless Run: Secret Stage Unlocked!
            box_w = 880
            box_h = 280
            r_box = pygame.Rect(cx - box_w // 2, cy - box_h // 2, box_w, box_h)
            pygame.draw.rect(surface, (10, 22, 38), r_box, border_radius=14)
            pygame.draw.rect(surface, (255, 215, 0), r_box, 3, border_radius=14)
            pygame.draw.rect(surface, (46, 224, 125), r_box.inflate(-8, -8), 1, border_radius=10)

            txt_h = self.font_menu.render("★ FLAWLESS RUN ACCOMPLISHED! ★", True, (46, 224, 125))
            surface.blit(txt_h, txt_h.get_rect(center=(cx, cy - 65)))
            
            txt_m = self.font_sub.render("ZERO DAMAGE TAKEN ACROSS ALL 10 STAGES!", True, COLOR_GOLD)
            surface.blit(txt_m, txt_m.get_rect(center=(cx, cy - 15)))

            txt_s = self.font_caption.render(f"SECRET FINAL STAGE UNLOCKED: ALL {TOTAL_GAUNTLET_KANA}-KANA MASTERY GAUNTLET", True, (0, 240, 255))
            surface.blit(txt_s, txt_s.get_rect(center=(cx, cy + 30)))
            
            txt_f = self.font_caption.render("PRESS [SPACE] / [ENTER] / GAMEPAD [A] TO ENTER SECRET TRIAL", True, COLOR_WHITE)
            surface.blit(txt_f, txt_f.get_rect(center=(cx, cy + 85)))

        elif stage == TOTAL_STAGES:
            # All stages cleared! Generous 880px box width guarantees 60px padding
            box_w = 880
            box_h = 260
            r_box = pygame.Rect(cx - box_w // 2, cy - box_h // 2, box_w, box_h)
            pygame.draw.rect(surface, (10, 20, 36), r_box, border_radius=12)
            pygame.draw.rect(surface, COLOR_GOLD, r_box, 3, border_radius=12)
            
            txt_h = self.font_title.render("ALL STAGES CLEARED!", True, COLOR_GOLD)
            surface.blit(txt_h, txt_h.get_rect(center=(cx, cy - 56)))
            
            txt_m = self.font_menu.render(f"YOU MASTERED ALL {TOTAL_STAGES} STAGES!", True, COLOR_CYAN)
            surface.blit(txt_m, txt_m.get_rect(center=(cx, cy + 10)))
            
            txt_f = self.font_sub.render("RETURNING TO TITLE SCREEN...", True, COLOR_WHITE)
            surface.blit(txt_f, txt_f.get_rect(center=(cx, cy + 68)))
        else:
            # Per-stage clear box: 860px width comfortably contains 725px button prompt
            box_w = 860
            box_h = 220
            r_box = pygame.Rect(cx - box_w // 2, cy - box_h // 2, box_w, box_h)
            pygame.draw.rect(surface, (10, 20, 36), r_box, border_radius=12)
            pygame.draw.rect(surface, COLOR_GOLD, r_box, 3, border_radius=12)
            
            txt_h = self.font_title.render(f"STAGE {stage:02d} CLEARED!", True, COLOR_GOLD)
            surface.blit(txt_h, txt_h.get_rect(center=(cx, cy - 36)))
            
            txt_f = self.font_sub.render("PRESS [SPACE] / [ENTER] / GAMEPAD [A] FOR NEXT STAGE", True, COLOR_CYAN)
            surface.blit(txt_f, txt_f.get_rect(center=(cx, cy + 36)))

    def render_game_over_overlay(self, surface: pygame.Surface):
        surface_h = surface.get_height()
        cx = 760
        cy = surface_h // 2
        box_w = 780
        box_h = 210
        r_box = pygame.Rect(cx - box_w // 2, cy - box_h // 2, box_w, box_h)
        pygame.draw.rect(surface, (25, 10, 10), r_box, border_radius=10)
        pygame.draw.rect(surface, (240, 40, 40), r_box, 3, border_radius=10)
        
        txt_h = self.font_title.render("OUT OF FUEL", True, (255, 65, 65))
        surface.blit(txt_h, txt_h.get_rect(center=(cx, cy - 35)))
        
        txt_f = self.font_sub.render("PRESS [SPACE] / [ENTER] TO RETRY  |  [ESC]: TITLE", True, COLOR_WHITE)
        surface.blit(txt_f, txt_f.get_rect(center=(cx, cy + 35)))

    def render_update_modal(self, surface: pygame.Surface, update_mgr):
        """Renders the online system update dialog modal with real-time status and download progress."""
        import os
        surface_w = surface.get_width()
        surface_h = surface.get_height()
        
        # 1. Full-screen dimmed backdrop
        dim_surf = pygame.Surface((surface_w, surface_h), pygame.SRCALPHA)
        dim_surf.fill((5, 10, 18, 225))
        surface.blit(dim_surf, (0, 0))
        
        # 2. Centered Cyber Modal Dialog (Expanded width for generous text padding)
        w = 980
        h = 560
        cx = surface_w // 2
        cy = surface_h // 2
        x = cx - (w // 2)
        y = cy - (h // 2)
        
        modal_bg = pygame.Surface((w, h), pygame.SRCALPHA)
        modal_bg.fill((10, 18, 30, 252))
        surface.blit(modal_bg, (x, y))
        
        # Double border
        pygame.draw.rect(surface, (0, 180, 240), (x, y, w, h), 3, border_radius=12)
        pygame.draw.rect(surface, (15, 35, 55), (x + 3, y + 3, w - 6, h - 6), 1, border_radius=10)
        
        # Header
        t_header = self.font_menu.render("ONLINE SYSTEM UPDATER", True, COLOR_GOLD)
        surface.blit(t_header, t_header.get_rect(center=(cx, y + 42)))
        pygame.draw.line(surface, (0, 140, 210), (x + 30, y + 74), (x + w - 30, y + 74), 2)
        
        # Target info badge
        tgt_base = os.path.basename(update_mgr.target_path) if update_mgr.target_path else "Nihongo_Master-x86_64.AppImage"
        if len(tgt_base) > 36:
            tgt_base = tgt_base[:33] + "..."
        t_cur_ver = self.font_caption.render(f"INSTALLED: v{update_mgr.current_version}   |   TARGET: {tgt_base}", True, (180, 215, 245))
        surface.blit(t_cur_ver, t_cur_ver.get_rect(center=(cx, y + 98)))
        
        def wrap_text(fnt: pygame.font.Font, txt: str, max_px: int) -> list[str]:
            words = txt.split()
            out_lines = []
            cur_words = []
            for word in words:
                test_str = " ".join(cur_words + [word])
                if fnt.size(test_str)[0] <= max_px:
                    cur_words.append(word)
                else:
                    if cur_words:
                        out_lines.append(" ".join(cur_words))
                    cur_words = [word]
            if cur_words:
                out_lines.append(" ".join(cur_words))
            return out_lines

        state = update_mgr.state
        
        if state == update_mgr.STATE_CHECKING:
            dots = "." * (int(time.time() * 3) % 4)
            t_spin = self.font_menu.render(f"CONNECTING TO GITHUB{dots}", True, COLOR_CYAN)
            surface.blit(t_spin, t_spin.get_rect(center=(cx, cy - 25)))
            
            t_sub = self.font_sub.render("Checking repository for new updates...", True, (200, 225, 250))
            surface.blit(t_sub, t_sub.get_rect(center=(cx, cy + 25)))
            
            pulse_x = int((math.sin(time.time() * 5.0) * 0.5 + 0.5) * (w - 240))
            pygame.draw.rect(surface, (15, 30, 50), (x + 120, cy + 70, w - 240, 10), border_radius=5)
            pygame.draw.rect(surface, (0, 220, 255), (x + 120 + pulse_x, cy + 70, 60, 10), border_radius=5)
            
        elif state == update_mgr.STATE_UP_TO_DATE:
            t_icon = self.font_speed.render("✓", True, (60, 220, 120))
            surface.blit(t_icon, t_icon.get_rect(center=(cx, cy - 65)))
            
            t_title = self.font_menu.render("YOUR GAME IS UP TO DATE!", True, (60, 220, 120))
            surface.blit(t_title, t_title.get_rect(center=(cx, cy - 10)))
            
            t_msg = self.font_sub.render(f"You are currently running the latest version (v{update_mgr.current_version}).", True, COLOR_WHITE)
            surface.blit(t_msg, t_msg.get_rect(center=(cx, cy + 35)))
            
            t_sub = self.font_caption.render("No new updates found in the GitHub repository.", True, (180, 210, 240))
            surface.blit(t_sub, t_sub.get_rect(center=(cx, cy + 68)))
            
            btn_ok = pygame.Rect(cx - 240, y + h - 70, 480, 50)
            pygame.draw.rect(surface, (18, 32, 52), btn_ok, border_radius=8)
            pygame.draw.rect(surface, (0, 180, 240), btn_ok, 2, border_radius=8)
            t_btn = self.font_sub.render("OK  [ENTER] / [A] / [B]", True, COLOR_GOLD)
            surface.blit(t_btn, t_btn.get_rect(center=btn_ok.center))
            
        elif state == update_mgr.STATE_UPDATE_AVAILABLE:
            t_star = self.font_menu.render("★ NEW UPDATE AVAILABLE! ★", True, COLOR_GOLD)
            surface.blit(t_star, t_star.get_rect(center=(cx, cy - 95)))
            
            clean_ver = update_mgr.remote_version.lstrip("v") if update_mgr.remote_version else ""
            t_ver = self.font_menu.render(f"LATEST VERSION: v{clean_ver}", True, COLOR_CYAN)
            surface.blit(t_ver, t_ver.get_rect(center=(cx, cy - 52)))
            
            # Changelog box (fits neatly within modal)
            c_box = pygame.Rect(x + 40, cy - 22, w - 80, 130)
            pygame.draw.rect(surface, (15, 26, 44), c_box, border_radius=8)
            pygame.draw.rect(surface, (0, 140, 215), c_box, 1, border_radius=8)
            
            t_ch_h = self.font_caption.render("WHAT'S NEW IN THIS UPDATE:", True, (180, 215, 245))
            surface.blit(t_ch_h, (c_box.left + 16, c_box.top + 10))
            
            ch_text = update_mgr.changelog or "Bug fixes, performance enhancements, and new content."
            clean_lines = []
            for raw_l in ch_text.splitlines():
                cl = raw_l.strip().lstrip("#*- ").strip()
                if cl and not cl.startswith("Download"):
                    clean_lines.append(cl)
            ch_summary = "   •   ".join(clean_lines[:3]) if clean_lines else ch_text
            wrapped_lines = wrap_text(self.font_caption, ch_summary, c_box.width - 32)
            for idx, line in enumerate(wrapped_lines[:2]):
                t_line = self.font_caption.render(line, True, COLOR_WHITE)
                surface.blit(t_line, (c_box.left + 16, c_box.top + 36 + idx * 22))
            
            t_safe = self.font_caption.render("✓ Safe In-Place Update: Preserves AppImage filename & Steam shortcuts.", True, (80, 230, 150))
            surface.blit(t_safe, (c_box.left + 16, c_box.top + c_box.height - 28))
            
            # Dual interactive buttons: Install vs Cancel
            btn_inst = pygame.Rect(cx - 390, y + h - 70, 360, 50)
            pygame.draw.rect(surface, (15, 55, 35), btn_inst, border_radius=8)
            pygame.draw.rect(surface, (60, 220, 120), btn_inst, 2, border_radius=8)
            t_inst = self.font_sub.render("INSTALL NOW  [A] / [ENTER]", True, (90, 255, 160))
            surface.blit(t_inst, t_inst.get_rect(center=btn_inst.center))

            btn_canc = pygame.Rect(cx + 30, y + h - 70, 360, 50)
            pygame.draw.rect(surface, (45, 22, 22), btn_canc, border_radius=8)
            pygame.draw.rect(surface, (220, 75, 75), btn_canc, 2, border_radius=8)
            t_canc = self.font_sub.render("CANCEL  [B] / [ESC]", True, (255, 170, 170))
            surface.blit(t_canc, t_canc.get_rect(center=btn_canc.center))
            
        elif state == update_mgr.STATE_DOWNLOADING:
            pct = update_mgr.progress_percent
            t_down = self.font_menu.render(f"DOWNLOADING UPDATE... {pct:.1f}%", True, COLOR_CYAN)
            surface.blit(t_down, t_down.get_rect(center=(cx, cy - 50)))
            
            bar_w = w - 120
            bar_h = 26
            bar_x = x + 60
            bar_y = cy - 12
            pygame.draw.rect(surface, (15, 25, 42), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
            fill_w = int(bar_w * (pct / 100.0))
            if fill_w > 0:
                pygame.draw.rect(surface, (0, 220, 255), (bar_x, bar_y, fill_w, bar_h), border_radius=6)
            pygame.draw.rect(surface, (0, 180, 240), (bar_x, bar_y, bar_w, bar_h), 2, border_radius=6)
            
            mb_down = update_mgr.bytes_downloaded / (1024 * 1024)
            mb_tot = update_mgr.bytes_total / (1024 * 1024)
            t_bytes = self.font_sub.render(f"{mb_down:.1f} MB / {mb_tot:.1f} MB", True, (200, 225, 250))
            surface.blit(t_bytes, t_bytes.get_rect(center=(cx, cy + 38)))
            
            t_warn = self.font_caption.render("Downloading and applying atomic in-place replacement. Please wait...", True, (180, 210, 240))
            surface.blit(t_warn, t_warn.get_rect(center=(cx, cy + 72)))
            
        elif state == update_mgr.STATE_SUCCESS:
            t_icon = self.font_speed.render("★", True, COLOR_GOLD)
            surface.blit(t_icon, t_icon.get_rect(center=(cx, cy - 75)))
            
            t_title = self.font_menu.render("UPDATE COMPLETED SUCCESSFULLY!", True, (60, 220, 120))
            surface.blit(t_title, t_title.get_rect(center=(cx, cy - 25)))
            
            t_msg = self.font_sub.render(f"Updated in-place to v{update_mgr.current_version}!", True, COLOR_WHITE)
            surface.blit(t_msg, t_msg.get_rect(center=(cx, cy + 18)))
            
            t_sub = self.font_caption.render("The AppImage binary was updated without altering filenames or paths.", True, (180, 210, 240))
            surface.blit(t_sub, t_sub.get_rect(center=(cx, cy + 50)))
            
            t_steam = self.font_caption.render("All Steam shortcuts, desktop launchers, and scripts will run this version.", True, (80, 230, 150))
            surface.blit(t_steam, t_steam.get_rect(center=(cx, cy + 76)))
            
            btn_rst = pygame.Rect(cx - 390, y + h - 70, 360, 50)
            pygame.draw.rect(surface, (18, 48, 75), btn_rst, border_radius=8)
            pygame.draw.rect(surface, (0, 220, 255), btn_rst, 2, border_radius=8)
            t_rst = self.font_sub.render("RESTART GAME  [A] / [ENTER]", True, COLOR_GOLD)
            surface.blit(t_rst, t_rst.get_rect(center=btn_rst.center))

            btn_cls = pygame.Rect(cx + 30, y + h - 70, 360, 50)
            pygame.draw.rect(surface, (30, 35, 48), btn_cls, border_radius=8)
            pygame.draw.rect(surface, (140, 170, 200), btn_cls, 2, border_radius=8)
            t_cls = self.font_sub.render("CLOSE  [B] / [ESC]", True, (210, 230, 250))
            surface.blit(t_cls, t_cls.get_rect(center=btn_cls.center))
            
        elif state == update_mgr.STATE_ERROR:
            t_icon = self.font_speed.render("⚠", True, (255, 75, 75))
            surface.blit(t_icon, t_icon.get_rect(center=(cx, cy - 65)))
            
            t_title = self.font_menu.render("UPDATE CHECK FAILED", True, (255, 75, 75))
            surface.blit(t_title, t_title.get_rect(center=(cx, cy - 10)))
            
            err_msg = update_mgr.error_message or "Network connection error."
            err_lines = wrap_text(self.font_sub, err_msg, w - 100)
            for idx, eline in enumerate(err_lines[:2]):
                t_msg = self.font_sub.render(eline, True, (255, 190, 190))
                surface.blit(t_msg, t_msg.get_rect(center=(cx, cy + 28 + idx * 24)))
            
            t_sub = self.font_caption.render("Please verify your internet connection and try again.", True, (180, 210, 240))
            surface.blit(t_sub, t_sub.get_rect(center=(cx, cy + 76)))
            
            btn_err = pygame.Rect(cx - 240, y + h - 70, 480, 50)
            pygame.draw.rect(surface, (45, 20, 25), btn_err, border_radius=8)
            pygame.draw.rect(surface, (240, 75, 75), btn_err, 2, border_radius=8)
            t_err = self.font_sub.render("CLOSE  [ENTER] / [A] / [B]", True, (255, 190, 190))
            surface.blit(t_err, t_err.get_rect(center=btn_err.center))
