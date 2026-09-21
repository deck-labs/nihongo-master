"""
road_renderer.py
Road curvature calculations, slice-by-slice rendering, stage environments, and finish line.
"""

import math
import random
import pygame
from game_config import (
    GAME_X, GAME_W, ROAD_MARGIN, SCREEN_WIDTH, SCREEN_HEIGHT,
    STAGE_TRACK_LENGTH, PLAYER_SCREEN_Y,
    COLOR_WATER_DEEP, COLOR_WATER_MID, COLOR_WATER_SWELL,
    COLOR_WATER_FOAM, COLOR_BRIDGE_SHADOW, COLOR_WALKWAY_DARK,
    COLOR_RAILING, COLOR_BARRIER_RED, COLOR_WHITE, COLOR_GOLD,
    COLOR_NEON_PURPLE, COLOR_NEON_AMBER, COLOR_NEON_CYAN,
    get_asset_path
)

class RoadRenderer:
    def __init__(self):
        self.track_distance = 0.0
        self.current_stage = 1
        self.frames = 0
        
        # Textures and sprites
        self.tex_asphalt = None
        self.tex_grass = None
        self.tex_concrete = None
        self.tex_water = None
        self.tex_sand = None
        self.tex_rock_ground = None
        
        self.tex_tree = None
        self.tex_palm_tree = None
        self.tex_pine_tree = None
        self.tex_boulder = None
        self.tex_finish_banner = None
        self.font_gantry = None

        # Realistic Ocean Water Assets
        self.tex_deep_ocean = None
        self.tex_caustics = None
        self.tex_foam_wake = None
        self.surf_bridge_shadow = None
        self.surf_wake = None
        self.ocean_sparkles = []
        
        # Scenery collections
        self.stage1_trees = []
        self.stage3_palms = []
        self.stage4_scenery = []
        self.stage5_buildings = []
        self.stage5_lamps = []
        self.stage5_gantries = []
        self.stage6_scenery = []
        self.stage6_magma_vents = []
        self.stage7_scenery = []
        self.stage7_ice_crystals = []
        self.stage8_sakura_trees = []
        self.stage8_lanterns = []
        self.stage8_petals = []
        self.stage9_cacti = []
        self.stage9_mesas = []
        self.stage9_tumbleweeds = []
        self.stage10_grandstands = []
        self.stage10_banners = []
        self.stage10_searchlights = []
        self.stage11_stars = []
        self.stage11_crystals = []
        self.stage11_torii = []
        self.stage11_gantries = []
        self.game_mode = "hiragana"
        
        self._load_assets()
        self._generate_scenery()

    def _load_assets(self):
        def load_img(subpath):
            path = get_asset_path(subpath)
            try:
                surf = pygame.image.load(path)
                return surf.convert_alpha()
            except Exception as e:
                print(f"Warning: Failed to load {subpath}: {e}")
                # Fallback blank surface
                s = pygame.Surface((64, 64), pygame.SRCALPHA)
                s.fill((100, 100, 100, 255))
                return s

        def load_cropped(subpath):
            img = load_img(subpath)
            if img:
                bbox = img.get_bounding_rect()
                if bbox.width > 0 and bbox.height > 0:
                    cropped = pygame.Surface(bbox.size, pygame.SRCALPHA)
                    cropped.blit(img, (0, 0), bbox)
                    return cropped
            return img

        self.tex_asphalt = load_img("textures/asphalt.png")
        self.tex_grass = load_img("textures/grass.png")
        self.tex_concrete = load_img("textures/concrete.png")
        self.tex_water = load_img("textures/water.png")
        self.tex_sand = load_img("textures/sand.png")
        self.tex_rock_ground = load_img("textures/rock_ground.png")

        # Realistic Ocean Water Assets
        self.tex_deep_ocean = load_img("textures/water_deep_ocean.png")
        self.tex_caustics = load_img("textures/water_caustics.png")
        self.tex_foam_wake = load_img("textures/water_foam_wake.png")
        
        # Pre-allocated translucent bridge shadow & hydrodynamic pylon wake
        self.surf_bridge_shadow = pygame.Surface((32, 6), pygame.SRCALPHA)
        self.surf_bridge_shadow.fill((4, 12, 28, 135))
        
        self.surf_wake = pygame.Surface((16, 6), pygame.SRCALPHA)
        self.surf_wake.fill((235, 250, 255, 175))
        
        # Fixed pseudo-random sparkle locations for deterministic specular glimmer
        self.ocean_sparkles = []
        rnd = random.Random(42)
        for _ in range(140):
            sx = rnd.uniform(GAME_X + 15, GAME_X + GAME_W - 15)
            sy = rnd.uniform(20, 1180)
            phase = rnd.uniform(0.0, math.pi * 2.0)
            spd = rnd.uniform(2.5, 4.8)
            self.ocean_sparkles.append((sx, sy, phase, spd))
        
        self.tex_tree = load_cropped("sprites/tree.png")
        self.tex_palm_tree = load_cropped("sprites/palm_tree.png")
        self.tex_pine_tree = load_cropped("sprites/pine_tree.png")
        self.tex_boulder = load_cropped("sprites/boulder.png")
        self.tex_finish_banner = load_img("sprites/finish_banner.png")
        try:
            self.font_gantry = pygame.font.Font(get_asset_path("fonts/DejaVuSans-Bold.ttf"), 14)
        except Exception:
            self.font_gantry = pygame.font.Font(None, 16)

        # Precompute 3D drop shadow surfaces & pre-scale sprites
        # 1. Stage 1 Deciduous Tree (72x94)
        self.tree_w, self.tree_h = 72, 94
        if self.tex_tree:
            self.sprite_tree = pygame.transform.smoothscale(self.tex_tree, (self.tree_w, self.tree_h))
        else:
            self.sprite_tree = None

        sh_tw = self.tree_w + 40
        sh_th = int(self.tree_h * 0.6) + 30
        self.shadow_tree = pygame.Surface((sh_tw, sh_th), pygame.SRCALPHA)
        # Ground contact ellipse at trunk base
        pygame.draw.ellipse(self.shadow_tree, (0, 0, 0, 130), (12, 8, 30, 14))
        # Angled trunk cast shadow connecting trunk to canopy
        pygame.draw.line(self.shadow_tree, (0, 0, 0, 95), (27, 14), (45, 28), 6)
        # Soft outer canopy penumbra
        pygame.draw.ellipse(self.shadow_tree, (0, 0, 0, 50), (22, 14, 60, 38))
        # Core inner canopy umbra
        pygame.draw.ellipse(self.shadow_tree, (0, 0, 0, 95), (26, 18, 52, 30))

        # 2. Stage 3 Tropical Palm Tree (76x82)
        self.palm_w, self.palm_h = 76, 82
        if self.tex_palm_tree:
            self.sprite_palm = pygame.transform.smoothscale(self.tex_palm_tree, (self.palm_w, self.palm_h))
        else:
            self.sprite_palm = None

        sh_pw = self.palm_w + 35
        sh_ph = int(self.palm_h * 0.6) + 35
        self.shadow_palm = pygame.Surface((sh_pw, sh_ph), pygame.SRCALPHA)
        # Trunk base contact ellipse
        pygame.draw.ellipse(self.shadow_palm, (0, 0, 0, 135), (10, 8, 24, 12))
        # Long curving trunk cast shadow on beach sand
        pygame.draw.line(self.shadow_palm, (0, 0, 0, 90), (22, 14), (44, 30), 5)
        # Radiating starburst palm frond canopy shadow
        cx_f, cy_f = 46, 32
        pygame.draw.ellipse(self.shadow_palm, (0, 0, 0, 45), (16, 14, 60, 36))
        for i in range(7):
            ang = i * (math.pi / 3.5)
            ex = cx_f + math.cos(ang) * 26
            ey = cy_f + math.sin(ang) * 16
            pygame.draw.line(self.shadow_palm, (0, 0, 0, 90), (cx_f, cy_f), (int(ex), int(ey)), 6)
        pygame.draw.circle(self.shadow_palm, (0, 0, 0, 105), (cx_f, cy_f), 12)

        # 3. Stage 4/6/7 Alpine / Scorched / Snowy Pine Tree (54x76)
        self.pine_w, self.pine_h = 54, 76
        if self.tex_pine_tree:
            self.sprite_pine = pygame.transform.smoothscale(self.tex_pine_tree, (self.pine_w, self.pine_h))
        else:
            self.sprite_pine = None

        sh_pnw = self.pine_w + 24
        sh_pnh = int(self.pine_h * 0.6) + 20
        self.shadow_pine = pygame.Surface((sh_pnw, sh_pnh), pygame.SRCALPHA)
        # Trunk contact ellipse
        pygame.draw.ellipse(self.shadow_pine, (0, 0, 0, 140), (8, 14, 22, 10))
        # Outer soft penumbra
        pygame.draw.ellipse(self.shadow_pine, (0, 0, 0, 40), (12, 4, 52, 36))
        # Tiered conical foliage shadow
        pygame.draw.ellipse(self.shadow_pine, (0, 0, 0, 95), (14, 14, 38, 22))
        pygame.draw.ellipse(self.shadow_pine, (0, 0, 0, 90), (24, 8, 28, 18))
        pygame.draw.ellipse(self.shadow_pine, (0, 0, 0, 85), (34, 2, 20, 14))
        pygame.draw.line(self.shadow_pine, (0, 0, 0, 110), (19, 20), (30, 16), 4)

        # 4. Stage 4/6/7 Canyon & Basalt Boulders (58x42)
        self.boulder_w, self.boulder_h = 58, 42
        if self.tex_boulder:
            self.sprite_boulder = pygame.transform.smoothscale(self.tex_boulder, (self.boulder_w, self.boulder_h))
        else:
            self.sprite_boulder = None

        sh_bw = self.boulder_w + 20
        sh_bh = self.boulder_h + 12
        self.shadow_boulder = pygame.Surface((sh_bw, sh_bh), pygame.SRCALPHA)
        # Outer ambient penumbra offset down-right (+10, +6)
        pygame.draw.ellipse(self.shadow_boulder, (0, 0, 0, 55), (10, 8, self.boulder_w + 6, int(self.boulder_h * 0.65)))
        # Core contact shadow directly beneath boulder
        pygame.draw.ellipse(self.shadow_boulder, (0, 0, 0, 145), (4, 6, self.boulder_w, int(self.boulder_h * 0.55)))

    def _get_safe_verge_x(self, stage: int, world_y: float, side: int, obj_w: float, road_clearance: float = 28.0, screen_pad: float = 12.0, rng: random.Random = None) -> tuple[float, int]:
        """Calculates a guaranteed safe verge X coordinate outside the road for any stage at world_y.
        Returns (x, actual_side) where actual_side is -1 for left verge, 1 for right verge.
        If the requested side is too narrow due to road curvature, shifts placement to the wide verge."""
        if rng is None:
            rng = random
        rl, rr = self.get_road_edges(stage, world_y)
        min_lx = GAME_X + screen_pad + obj_w * 0.5
        max_lx = rl - road_clearance - obj_w * 0.5
        min_rx = rr + road_clearance + obj_w * 0.5
        max_rx = (GAME_X + GAME_W) - screen_pad - obj_w * 0.5
        
        if side == -1:
            if max_lx >= min_lx:
                return rng.uniform(min_lx, max_lx), -1
            elif max_rx >= min_rx:
                return rng.uniform(min_rx, max_rx), 1
            else:
                return max_lx, -1
        else:
            if max_rx >= min_rx:
                return rng.uniform(min_rx, max_rx), 1
            elif max_lx >= min_lx:
                return rng.uniform(min_lx, max_lx), -1
            else:
                return min_rx, 1

    def _generate_scenery(self):
        rng = random.Random(12345)
        
        # Stage 1: Trees on grass verges
        y = 200.0
        while y < STAGE_TRACK_LENGTH - 800.0:
            y += rng.uniform(180.0, 320.0)
            lx, _ = self._get_safe_verge_x(1, y, -1, self.tree_w, road_clearance=50.0, rng=rng)
            rx, _ = self._get_safe_verge_x(1, y, 1, self.tree_w, road_clearance=32.0, rng=rng)
            self.stage1_trees.append((lx, y))
            self.stage1_trees.append((rx, y))
            
        # Stage 3: Tropical Palms along beach
        y = 200.0
        while y < STAGE_TRACK_LENGTH - 800.0:
            y += rng.uniform(200.0, 360.0)
            px, _ = self._get_safe_verge_x(3, y, -1, self.palm_w, road_clearance=32.0, rng=rng)
            self.stage3_palms.append((px, y))
            
        # Stage 4: Mountain Canyon Pines and Boulders
        y = 200.0
        while y < STAGE_TRACK_LENGTH - 800.0:
            y += rng.uniform(160.0, 290.0)
            is_pine_l = rng.random() > 0.45
            w_l = self.pine_w if is_pine_l else self.boulder_w
            lx, _ = self._get_safe_verge_x(4, y, -1, w_l, road_clearance=32.0, rng=rng)
            self.stage4_scenery.append({"pos": (lx, y), "is_pine": is_pine_l})
            
            is_pine_r = rng.random() > 0.45
            w_r = self.pine_w if is_pine_r else self.boulder_w
            rx, _ = self._get_safe_verge_x(4, y, 1, w_r, road_clearance=32.0, rng=rng)
            self.stage4_scenery.append({"pos": (rx, y), "is_pine": is_pine_r})

        # Stage 5: Neon Metropolis Skyscrapers, Street Lamps, and Expressway Gantries
        y = 100.0
        while y < STAGE_TRACK_LENGTH - 400.0:
            bw = rng.uniform(85.0, 115.0)
            bh = rng.uniform(160.0, 280.0)
            rl, rr = self.get_road_edges(5, y)
            
            # Left building footprint (constrained outside left railing)
            lx = GAME_X + rng.uniform(4.0, 14.0)
            max_lw = max(40.0, rl - 26.0 - lx)
            cur_bw_l = min(bw, max_lw)
            
            # Right building footprint (constrained outside right railing)
            rx_right = (GAME_X + GAME_W) - rng.uniform(4.0, 14.0)
            max_rw = max(40.0, rx_right - (rr + 26.0))
            cur_bw_r = min(bw, max_rw)
            rx = rx_right - cur_bw_r
            
            # Precompute window rows x cols
            rows = max(4, int(bh // 26))
            cols_l = max(3, int(cur_bw_l // 18))
            cols_r = max(3, int(cur_bw_r // 18))
            win_palette = [
                (0, 225, 255),    # Neon Cyan
                (255, 180, 20),   # Warm Amber
                (245, 248, 255),  # Pure White
                (220, 60, 240),   # Neon Magenta
                (28, 34, 48),     # Unlit
                (28, 34, 48),     # Unlit
                (28, 34, 48)      # Unlit
            ]
            l_wins = [[rng.choice(win_palette) for _ in range(cols_l)] for _ in range(rows)]
            r_wins = [[rng.choice(win_palette) for _ in range(cols_r)] for _ in range(rows)]
            
            self.stage5_buildings.append({
                "x": lx, "y": y, "w": cur_bw_l, "h": bh,
                "col": rng.choice([(18, 22, 34), (24, 28, 44), (14, 18, 30)]),
                "windows": l_wins,
                "beacon": rng.random() > 0.4
            })
            self.stage5_buildings.append({
                "x": rx, "y": y, "w": cur_bw_r, "h": bh,
                "col": rng.choice([(18, 22, 34), (24, 28, 44), (14, 18, 30)]),
                "windows": r_wins,
                "beacon": rng.random() > 0.4
            })
            y += rng.uniform(220.0, 360.0)
            
        # Street lamps along left and right highway shoulders
        ly = 80.0
        while ly < STAGE_TRACK_LENGTH - 400.0:
            self.stage5_lamps.append(ly)
            ly += 180.0
            
        # Overhead expressway gantries
        gy = 2800.0
        while gy < STAGE_TRACK_LENGTH - 1500.0:
            self.stage5_gantries.append(gy)
            gy += 4500.0

        # Stage 6: Volcano Caldera Scenery (basalt boulders, scorched pine trees, glowing magma vents)
        y = 200.0
        while y < STAGE_TRACK_LENGTH - 800.0:
            side = -1 if rng.random() < 0.5 else 1
            is_pine = (rng.random() < 0.35)
            obj_w = self.pine_w if is_pine else self.boulder_w
            px, _ = self._get_safe_verge_x(6, y, side, obj_w, road_clearance=32.0, rng=rng)
            self.stage6_scenery.append({
                "pos": (px, y),
                "is_pine": is_pine
            })
            y += rng.uniform(85.0, 180.0)
            
        vy = 300.0
        while vy < STAGE_TRACK_LENGTH - 600.0:
            side = -1 if rng.random() < 0.5 else 1
            rad = rng.uniform(16, 28)
            vx, _ = self._get_safe_verge_x(6, vy, side, rad * 2.0, road_clearance=24.0, rng=rng)
            self.stage6_magma_vents.append({
                "x": vx,
                "y": vy,
                "radius": rad
            })
            vy += rng.uniform(220.0, 380.0)

        # Stage 7: Glacier Tundra Scenery (snowy pines, frosted boulders, crystalline ice spires)
        y = 180.0
        while y < STAGE_TRACK_LENGTH - 800.0:
            side = -1 if rng.random() < 0.5 else 1
            is_pine = (rng.random() < 0.5)
            obj_w = self.pine_w if is_pine else self.boulder_w
            px, _ = self._get_safe_verge_x(7, y, side, obj_w, road_clearance=32.0, rng=rng)
            self.stage7_scenery.append({
                "pos": (px, y),
                "is_pine": is_pine
            })
            y += rng.uniform(80.0, 170.0)
            
        cy = 240.0
        while cy < STAGE_TRACK_LENGTH - 600.0:
            side = -1 if rng.random() < 0.5 else 1
            cw = rng.uniform(16, 26)
            cx, _ = self._get_safe_verge_x(7, cy, side, cw, road_clearance=24.0, rng=rng)
            self.stage7_ice_crystals.append({
                "x": cx,
                "y": cy,
                "height": rng.uniform(30, 52),
                "width": cw
            })
            cy += rng.uniform(160.0, 300.0)

        # Stage 8: Sakura Trees, Stone Lanterns, and Drifting Blossom Petals
        y = 160.0
        while y < STAGE_TRACK_LENGTH - 800.0:
            side = -1 if rng.random() < 0.5 else 1
            scale = rng.uniform(0.9, 1.25)
            tree_dia = 70.0 * scale
            tx, _ = self._get_safe_verge_x(8, y, side, tree_dia, road_clearance=36.0, rng=rng)
            self.stage8_sakura_trees.append({
                "pos": (tx, y),
                "scale": scale,
                "tone": rng.choice([0, 1, 2])
            })
            y += rng.uniform(70.0, 150.0)

        ly = 280.0
        while ly < STAGE_TRACK_LENGTH - 1000.0:
            side = -1 if rng.random() < 0.5 else 1
            lx, _ = self._get_safe_verge_x(8, ly, side, 36.0, road_clearance=26.0, rng=rng)
            self.stage8_lanterns.append({
                "pos": (lx, ly),
                "h": rng.uniform(34, 46)
            })
            ly += rng.uniform(260.0, 420.0)

        for _ in range(65):
            self.stage8_petals.append({
                "rx": rng.uniform(0.0, float(GAME_W)),
                "ry": rng.uniform(0.0, 1200.0),
                "speed_y": rng.uniform(80.0, 180.0),
                "drift_freq": rng.uniform(1.2, 2.6),
                "drift_amp": rng.uniform(18.0, 38.0),
                "size": rng.uniform(3.5, 6.5),
                "phase": rng.uniform(0.0, 6.28),
                "color": rng.choice([
                    (255, 192, 203),
                    (255, 182, 193),
                    (255, 215, 225),
                    (255, 165, 185)
                ])
            })

        # Stage 9: Saguaro Cacti, Sandstone Mesas, and Drifting Tumbleweeds
        y = 150.0
        while y < STAGE_TRACK_LENGTH - 800.0:
            side = -1 if rng.random() < 0.5 else 1
            cx, _ = self._get_safe_verge_x(9, y, side, 34.0, road_clearance=26.0, rng=rng)
            self.stage9_cacti.append({
                "pos": (cx, y),
                "h": rng.uniform(42, 66),
                "arms": rng.choice([1, 2, 3]),
                "arm_y": rng.uniform(0.35, 0.65)
            })
            y += rng.uniform(75.0, 160.0)

        my = 260.0
        while my < STAGE_TRACK_LENGTH - 1000.0:
            side = -1 if rng.random() < 0.5 else 1
            mw = rng.uniform(60, 95)
            mx, _ = self._get_safe_verge_x(9, my, side, mw, road_clearance=24.0, rng=rng)
            self.stage9_mesas.append({
                "pos": (mx, my),
                "w": mw,
                "h": rng.uniform(36, 52),
                "col_idx": rng.choice([0, 1, 2])
            })
            my += rng.uniform(280.0, 450.0)

        for _ in range(40):
            self.stage9_tumbleweeds.append({
                "rx": rng.uniform(0.0, float(GAME_W)),
                "ry": rng.uniform(0.0, 1200.0),
                "speed_y": rng.uniform(140.0, 260.0),
                "speed_x": rng.uniform(-40.0, 40.0),
                "rad": rng.uniform(6.0, 12.0),
                "rot": rng.uniform(0.0, 6.28)
            })

        # Stage 10: Circuit Grandstands and Celebration Searchlights
        gy = 200.0
        while gy < STAGE_TRACK_LENGTH - 1000.0:
            side = -1 if rng.random() < 0.5 else 1
            gx, _ = self._get_safe_verge_x(10, gy, side, 75.0, road_clearance=28.0, rng=rng)
            self.stage10_grandstands.append({
                "pos": (gx, gy),
                "w": 75.0,
                "h": 50.0,
                "banner_col": rng.choice([(225, 40, 40), (40, 130, 230), (245, 185, 20), (35, 185, 85)])
            })
            gy += rng.uniform(220.0, 360.0)

        sy = 300.0
        while sy < STAGE_TRACK_LENGTH - 1200.0:
            side = -1 if rng.random() < 0.5 else 1
            sx, _ = self._get_safe_verge_x(10, sy, side, 20.0, road_clearance=24.0, rng=rng)
            self.stage10_searchlights.append({
                "pos": (sx, sy),
                "phase": rng.uniform(0.0, 6.28),
                "sweep_speed": rng.uniform(1.2, 2.4)
            })
            sy += rng.uniform(320.0, 500.0)

        # Stage 11: Rainbow Skyway (Secret All-Hiragana Mastery Gauntlet)
        for _ in range(100):
            self.stage11_stars.append({
                "x": rng.uniform(GAME_X, GAME_X + GAME_W),
                "y": rng.uniform(0.0, 1080.0),
                "r": rng.uniform(1.0, 3.0),
                "phase": rng.uniform(0.0, 6.28),
                "speed": rng.uniform(1.5, 3.5),
                "color": rng.choice([(255, 255, 255), (180, 230, 255), (255, 220, 240), (255, 240, 180)])
            })

        cy = 200.0
        while cy < STAGE_TRACK_LENGTH - 600.0:
            lx, _ = self._get_safe_verge_x(11, cy, -1, 24.0, road_clearance=24.0, rng=rng)
            rx, _ = self._get_safe_verge_x(11, cy, 1, 24.0, road_clearance=24.0, rng=rng)
            self.stage11_crystals.append({"pos": (lx, cy), "color": rng.choice([(0, 235, 255), (255, 120, 240), (255, 215, 0), (120, 255, 180)])})
            self.stage11_crystals.append({"pos": (rx, cy), "color": rng.choice([(0, 235, 255), (255, 120, 240), (255, 215, 0), (120, 255, 180)])})
            cy += rng.uniform(220.0, 360.0)

        ty = 800.0
        while ty < STAGE_TRACK_LENGTH - 1200.0:
            self.stage11_torii.append({
                "y": ty,
                "color": rng.choice([(255, 45, 85), (0, 220, 255), (255, 215, 0)])
            })
            ty += rng.uniform(3200.0, 4600.0)

        self.rebuild_stage11_gantries(self.game_mode)

    def rebuild_stage11_gantries(self, game_mode: str = "hiragana"):
        self.game_mode = game_mode
        self.stage11_gantries.clear()
        if game_mode == "katakana":
            g_messages = [
                "★ SECRET STAGE: ALL 71 KATAKANA GAUNTLET ★",
                "★ NO-DAMAGE CHAMPION // PROVE YOUR MASTERY ★",
                "★ ア・カ・サ・タ・ナ・ハ・マ・ヤ・ラ・ワ・ン ★",
                "★ BONUS STAGE: REFUEL +35% // SCORE +100 ★",
                "★ MASTER EVERY KATAKANA // FLAWLESS VICTORY ★"
            ]
        else:
            g_messages = [
                "★ SECRET STAGE: ALL 71 HIRAGANA GAUNTLET ★",
                "★ NO-DAMAGE CHAMPION // PROVE YOUR MASTERY ★",
                "★ あ・か・さ・た・な・は・ま・や・ら・わ・ん ★",
                "★ BONUS STAGE: REFUEL +35% // SCORE +100 ★",
                "★ MASTER EVERY HIRAGANA // FLAWLESS VICTORY ★"
            ]
        gy = 1800.0
        g_idx = 0
        while gy < STAGE_TRACK_LENGTH - 1500.0:
            self.stage11_gantries.append({
                "y": gy,
                "text": g_messages[g_idx % len(g_messages)]
            })
            gy += 6500.0
            g_idx += 1

    def get_road_edges(self, stage: int, world_y: float) -> tuple[float, float]:
        """Calculates (left_edge, right_edge) for any track coordinate."""
        normal_left = GAME_X + ROAD_MARGIN
        normal_right = GAME_X + GAME_W - ROAD_MARGIN
        
        if stage == 1 or world_y < 0.0:
            return (normal_left, normal_right)
            
        if stage == 2:
            # Elevated Bridge Bottlenecks
            if world_y >= STAGE_TRACK_LENGTH - 2000.0:
                return (normal_left, normal_right)
                
            seg_len = 2000.0
            seg_idx = int(world_y / seg_len)
            seg_pos = world_y % seg_len
            
            target_left = normal_left
            target_right = normal_right
            
            b_type = abs(seg_idx) % 3
            if b_type == 0:
                target_left = normal_left + 150.0   # Left pinch
            elif b_type == 1:
                target_right = normal_right - 150.0 # Right pinch
            else:
                target_left = normal_left + 100.0   # Center bottleneck
                target_right = normal_right - 100.0
                
            if seg_pos < 550.0:
                return (normal_left, normal_right)
            elif seg_pos < 800.0:
                t = (seg_pos - 550.0) / 250.0
                smooth_t = 0.5 - 0.5 * math.cos(t * math.pi)
                return (
                    normal_left + (target_left - normal_left) * smooth_t,
                    normal_right + (target_right - normal_right) * smooth_t
                )
            elif seg_pos < 1550.0:
                return (target_left, target_right)
            elif seg_pos < 1800.0:
                t = (seg_pos - 1550.0) / 250.0
                smooth_t = 0.5 - 0.5 * math.cos(t * math.pi)
                return (
                    target_left + (normal_left - target_left) * smooth_t,
                    target_right + (normal_right - target_right) * smooth_t
                )
            else:
                return (normal_left, normal_right)
                
        if stage == 3:
            # Coastal Beach Sweeping Curves
            if world_y >= STAGE_TRACK_LENGTH - 2400.0:
                return (normal_left, normal_right)
                
            seg_len = 2400.0
            seg_idx = int(world_y / seg_len)
            seg_pos = world_y % seg_len
            pattern = abs(seg_idx) % 4
            curve_shift = 0.0
            
            if pattern == 0:
                # Sweeping left bend
                if 350.0 <= seg_pos < 850.0:
                    t = (seg_pos - 350.0) / 500.0
                    curve_shift = -95.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    curve_shift = -95.0
                elif 1550.0 <= seg_pos < 2050.0:
                    t = (seg_pos - 1550.0) / 500.0
                    curve_shift = -95.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 1:
                # Sweeping right ocean bend
                if 350.0 <= seg_pos < 850.0:
                    t = (seg_pos - 350.0) / 500.0
                    curve_shift = 95.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    curve_shift = 95.0
                elif 1550.0 <= seg_pos < 2050.0:
                    t = (seg_pos - 1550.0) / 500.0
                    curve_shift = 95.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 2:
                # Coastal S-Chicane
                if 300.0 <= seg_pos < 800.0:
                    t = (seg_pos - 300.0) / 500.0
                    curve_shift = -90.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 800.0 <= seg_pos < 1600.0:
                    t = (seg_pos - 800.0) / 800.0
                    curve_shift = -90.0 + 180.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1600.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1600.0) / 500.0
                    curve_shift = 90.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            else:
                # Reverse S-Chicane
                if 300.0 <= seg_pos < 800.0:
                    t = (seg_pos - 300.0) / 500.0
                    curve_shift = 90.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 800.0 <= seg_pos < 1600.0:
                    t = (seg_pos - 800.0) / 800.0
                    curve_shift = 90.0 - 180.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1600.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1600.0) / 500.0
                    curve_shift = -90.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                    
            return (normal_left + curve_shift, normal_right + curve_shift)
            
        if stage == 4:
            # Mountain Canyon Pass & Technical Bottlenecks
            if world_y >= STAGE_TRACK_LENGTH - 2400.0:
                return (normal_left, normal_right)
                
            seg_len = 2400.0
            seg_idx = int(world_y / seg_len)
            seg_pos = world_y % seg_len
            pattern = abs(seg_idx) % 4
            
            cur_left = normal_left
            cur_right = normal_right
            
            if pattern == 0:
                # Canyon winding S-curves
                shift = 0.0
                if 250.0 <= seg_pos < 750.0:
                    t = (seg_pos - 250.0) / 500.0
                    shift = -110.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 750.0 <= seg_pos < 1550.0:
                    t = (seg_pos - 750.0) / 800.0
                    shift = -110.0 + 220.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1550.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1550.0) / 550.0
                    shift = 110.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                cur_left = normal_left + shift
                cur_right = normal_right + shift
            elif pattern == 1:
                # Canyon Gorge Bottleneck (narrows from 640px to 440px)
                pinch = 0.0
                if 350.0 <= seg_pos < 750.0:
                    t = (seg_pos - 350.0) / 400.0
                    pinch = 100.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 750.0 <= seg_pos < 1650.0:
                    pinch = 100.0
                elif 1650.0 <= seg_pos < 2050.0:
                    t = (seg_pos - 1650.0) / 400.0
                    pinch = 100.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                cur_left = normal_left + pinch
                cur_right = normal_right - pinch
            elif pattern == 2:
                # Mountain Hairpin & Cliffside Switchback
                shift = 0.0
                pinch = 0.0
                if 300.0 <= seg_pos < 800.0:
                    t = (seg_pos - 300.0) / 500.0
                    shift = -120.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                    pinch = 40.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 800.0 <= seg_pos < 1550.0:
                    shift = -120.0
                    pinch = 40.0
                elif 1550.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1550.0) / 550.0
                    shift = -120.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                    pinch = 40.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                cur_left = normal_left + shift + pinch * 0.5
                cur_right = normal_right + shift - pinch * 0.5
            else:
                # Alpine Ridge Bluff Bend
                shift = 0.0
                if 300.0 <= seg_pos < 800.0:
                    t = (seg_pos - 300.0) / 500.0
                    shift = 115.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 800.0 <= seg_pos < 1550.0:
                    t = (seg_pos - 800.0) / 750.0
                    shift = 115.0 - 200.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1550.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1550.0) / 550.0
                    shift = -85.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                cur_left = normal_left + shift
                cur_right = normal_right + shift
                
            return (cur_left, cur_right)

        if stage == 5:
            # Neon Metropolis Expressway - High-speed urban sweeps, flyover chicanes, and wide straights
            if world_y >= STAGE_TRACK_LENGTH - 2400.0:
                return (normal_left, normal_right)
                
            seg_len = 2400.0
            seg_idx = int(world_y / seg_len)
            seg_pos = world_y % seg_len
            pattern = abs(seg_idx) % 4
            
            shift = 0.0
            if pattern == 0:
                # Fast sweeping left expressway bend
                if 300.0 <= seg_pos < 850.0:
                    t = (seg_pos - 300.0) / 550.0
                    shift = -100.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    shift = -100.0
                elif 1550.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1550.0) / 550.0
                    shift = -100.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 1:
                # Fast sweeping right expressway bend
                if 300.0 <= seg_pos < 850.0:
                    t = (seg_pos - 300.0) / 550.0
                    shift = 100.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    shift = 100.0
                elif 1550.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1550.0) / 550.0
                    shift = 100.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 2:
                # Urban elevated flyover chicane (left to right)
                if 250.0 <= seg_pos < 750.0:
                    t = (seg_pos - 250.0) / 500.0
                    shift = -90.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 750.0 <= seg_pos < 1600.0:
                    t = (seg_pos - 750.0) / 850.0
                    shift = -90.0 + 180.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1600.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1600.0) / 500.0
                    shift = 90.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            else:
                # High-speed straight with subtle undulating overpass
                if 400.0 <= seg_pos < 900.0:
                    t = (seg_pos - 400.0) / 500.0
                    shift = 50.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 900.0 <= seg_pos < 1500.0:
                    shift = 50.0
                elif 1500.0 <= seg_pos < 2000.0:
                    t = (seg_pos - 1500.0) / 500.0
                    shift = 50.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                    
            return (normal_left + shift, normal_right + shift)

        if stage == 6:
            # Volcano Caldera - Technical volcanic ridge curves, sharp apexes, and fast straights along crater lip
            if world_y < 0.0 or world_y >= STAGE_TRACK_LENGTH - 2400.0:
                return (normal_left, normal_right)
                
            seg_len = 2400.0
            seg_idx = int(world_y / seg_len)
            seg_pos = world_y % seg_len
            pattern = abs(seg_idx) % 4
            
            shift = 0.0
            if pattern == 0:
                # Caldera Rim Left Sweeper
                if 300.0 <= seg_pos < 850.0:
                    t = (seg_pos - 300.0) / 550.0
                    shift = -110.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    shift = -110.0
                elif 1550.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1550.0) / 550.0
                    shift = -110.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 1:
                # Caldera Rim Right Sweeper
                if 300.0 <= seg_pos < 850.0:
                    t = (seg_pos - 300.0) / 550.0
                    shift = 110.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    shift = 110.0
                elif 1550.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1550.0) / 550.0
                    shift = 110.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 2:
                # Technical Volcanic Chicane (Right then Left)
                if 250.0 <= seg_pos < 750.0:
                    t = (seg_pos - 250.0) / 500.0
                    shift = 95.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 750.0 <= seg_pos < 1600.0:
                    t = (seg_pos - 750.0) / 850.0
                    shift = 95.0 - 190.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1600.0 <= seg_pos < 2100.0:
                    t = (seg_pos - 1600.0) / 500.0
                    shift = -95.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            else:
                # Ridge Crest Straight with gentle curve
                if 400.0 <= seg_pos < 900.0:
                    t = (seg_pos - 400.0) / 500.0
                    shift = -40.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 900.0 <= seg_pos < 1500.0:
                    shift = -40.0
                elif 1500.0 <= seg_pos < 2000.0:
                    t = (seg_pos - 1500.0) / 500.0
                    shift = -40.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                    
            return (normal_left + shift, normal_right + shift)

        if stage == 7:
            # Glacier Tundra - Sub-zero alpine bends, sweeping icefield curves, technical frozen chicanes
            if world_y < 0.0 or world_y >= STAGE_TRACK_LENGTH - 2400.0:
                return (normal_left, normal_right)
                
            seg_len = 2400.0
            seg_idx = int(world_y / seg_len)
            seg_pos = world_y % seg_len
            pattern = abs(seg_idx) % 4
            
            shift = 0.0
            if pattern == 0:
                # Glacier Shelf Left Sweeper
                if 250.0 <= seg_pos < 850.0:
                    t = (seg_pos - 250.0) / 600.0
                    shift = -115.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    shift = -115.0
                elif 1550.0 <= seg_pos < 2150.0:
                    t = (seg_pos - 1550.0) / 600.0
                    shift = -115.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 1:
                # Glacier Shelf Right Sweeper
                if 250.0 <= seg_pos < 850.0:
                    t = (seg_pos - 250.0) / 600.0
                    shift = 115.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    shift = 115.0
                elif 1550.0 <= seg_pos < 2150.0:
                    t = (seg_pos - 1550.0) / 600.0
                    shift = 115.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 2:
                # Frozen Icefall Chicane (Left then Right)
                if 200.0 <= seg_pos < 700.0:
                    t = (seg_pos - 200.0) / 500.0
                    shift = -95.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 700.0 <= seg_pos < 1550.0:
                    t = (seg_pos - 700.0) / 850.0
                    shift = -95.0 + 190.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1550.0 <= seg_pos < 2050.0:
                    t = (seg_pos - 1550.0) / 500.0
                    shift = 95.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            else:
                # Summit Icefield Undulating Straight
                if 350.0 <= seg_pos < 850.0:
                    t = (seg_pos - 350.0) / 500.0
                    shift = 45.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1450.0:
                    shift = 45.0
                elif 1450.0 <= seg_pos < 1950.0:
                    t = (seg_pos - 1450.0) / 500.0
                    shift = 45.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                    
            return (normal_left + shift, normal_right + shift)

        if stage == 8:
            # Sakura Boulevard - Spring drifting sweepers, high-speed blossom bends, undulating cherry grove straightaways
            if world_y < 0.0 or world_y >= STAGE_TRACK_LENGTH - 2400.0:
                return (normal_left, normal_right)
                
            seg_len = 2400.0
            seg_idx = int(world_y / seg_len)
            seg_pos = world_y % seg_len
            pattern = abs(seg_idx) % 4
            
            shift = 0.0
            if pattern == 0:
                # Blossom Sweeper Left (long, smooth sweeping curve)
                if 250.0 <= seg_pos < 850.0:
                    t = (seg_pos - 250.0) / 600.0
                    shift = -120.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    shift = -120.0
                elif 1550.0 <= seg_pos < 2150.0:
                    t = (seg_pos - 1550.0) / 600.0
                    shift = -120.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 1:
                # High-Speed Sakura Bank Right
                if 250.0 <= seg_pos < 850.0:
                    t = (seg_pos - 250.0) / 600.0
                    shift = 120.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    shift = 120.0
                elif 1550.0 <= seg_pos < 2150.0:
                    t = (seg_pos - 1550.0) / 600.0
                    shift = 120.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 2:
                # Spring S-Chicane (Flowing Left then Right)
                if 200.0 <= seg_pos < 700.0:
                    t = (seg_pos - 200.0) / 500.0
                    shift = -100.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 700.0 <= seg_pos < 1550.0:
                    t = (seg_pos - 700.0) / 850.0
                    shift = -100.0 + 200.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1550.0 <= seg_pos < 2050.0:
                    t = (seg_pos - 1550.0) / 500.0
                    shift = 100.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            else:
                # Sakura Avenue Undulating Straight
                if 300.0 <= seg_pos < 750.0:
                    t = (seg_pos - 300.0) / 450.0
                    shift = -40.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 750.0 <= seg_pos < 1250.0:
                    t = (seg_pos - 750.0) / 500.0
                    shift = -40.0 + 80.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1250.0 <= seg_pos < 1700.0:
                    t = (seg_pos - 1250.0) / 450.0
                    shift = 40.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                    
            return (normal_left + shift, normal_right + shift)

        if stage == 9:
            # Sunset Canyon - High-speed desert gorge sweeps, canyon wall bends, undulating sandstone straights
            if world_y < 0.0 or world_y >= STAGE_TRACK_LENGTH - 2400.0:
                return (normal_left, normal_right)
                
            seg_len = 2400.0
            seg_idx = int(world_y / seg_len)
            seg_pos = world_y % seg_len
            pattern = abs(seg_idx) % 4
            
            shift = 0.0
            if pattern == 0:
                # Canyon Wall Left Sweeper
                if 250.0 <= seg_pos < 850.0:
                    t = (seg_pos - 250.0) / 600.0
                    shift = -125.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    shift = -125.0
                elif 1550.0 <= seg_pos < 2150.0:
                    t = (seg_pos - 1550.0) / 600.0
                    shift = -125.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 1:
                # Red Rock Mesa Right Bank
                if 250.0 <= seg_pos < 850.0:
                    t = (seg_pos - 250.0) / 600.0
                    shift = 125.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1550.0:
                    shift = 125.0
                elif 1550.0 <= seg_pos < 2150.0:
                    t = (seg_pos - 1550.0) / 600.0
                    shift = 125.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 2:
                # Sandstone Gorge S-Chicane
                if 200.0 <= seg_pos < 700.0:
                    t = (seg_pos - 200.0) / 500.0
                    shift = -95.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 700.0 <= seg_pos < 1550.0:
                    t = (seg_pos - 700.0) / 850.0
                    shift = -95.0 + 190.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1550.0 <= seg_pos < 2050.0:
                    t = (seg_pos - 1550.0) / 500.0
                    shift = 95.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            else:
                # Desert Highway Straightaway
                if 300.0 <= seg_pos < 800.0:
                    t = (seg_pos - 300.0) / 500.0
                    shift = 35.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 800.0 <= seg_pos < 1400.0:
                    shift = 35.0
                elif 1400.0 <= seg_pos < 1900.0:
                    t = (seg_pos - 1400.0) / 500.0
                    shift = 35.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                    
            return (normal_left + shift, normal_right + shift)

        if stage == 10:
            # Fuji Speedway - Grand Championship formula circuit, 100R carousel, technical Dunlop chicane, main straight
            if world_y < 0.0 or world_y >= STAGE_TRACK_LENGTH - 2400.0:
                return (normal_left, normal_right)
                
            seg_len = 2400.0
            seg_idx = int(world_y / seg_len)
            seg_pos = world_y % seg_len
            pattern = abs(seg_idx) % 4
            
            shift = 0.0
            if pattern == 0:
                # Dunlop Technical S-Chicane
                if 200.0 <= seg_pos < 700.0:
                    t = (seg_pos - 200.0) / 500.0
                    shift = -110.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 700.0 <= seg_pos < 1550.0:
                    t = (seg_pos - 700.0) / 850.0
                    shift = -110.0 + 220.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1550.0 <= seg_pos < 2050.0:
                    t = (seg_pos - 1550.0) / 500.0
                    shift = 110.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 1:
                # 100R High-Speed Carousel Right
                if 250.0 <= seg_pos < 850.0:
                    t = (seg_pos - 250.0) / 600.0
                    shift = 130.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1600.0:
                    shift = 130.0
                elif 1600.0 <= seg_pos < 2200.0:
                    t = (seg_pos - 1600.0) / 600.0
                    shift = 130.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 2:
                # Hairpin Apex Left
                if 250.0 <= seg_pos < 850.0:
                    t = (seg_pos - 250.0) / 600.0
                    shift = -130.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1600.0:
                    shift = -130.0
                elif 1600.0 <= seg_pos < 2200.0:
                    t = (seg_pos - 1600.0) / 600.0
                    shift = -130.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            else:
                # Fuji Grand Championship Main Straightaway
                if 350.0 <= seg_pos < 850.0:
                    t = (seg_pos - 350.0) / 500.0
                    shift = 30.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1450.0:
                    shift = 30.0
                elif 1450.0 <= seg_pos < 1950.0:
                    t = (seg_pos - 1450.0) / 500.0
                    shift = 30.0 * (0.5 + 0.5 * math.cos(t * math.pi))
                    
            return (normal_left + shift, normal_right + shift)

        if stage == 11:
            # Stage 11: Rainbow Skyway - Majestic sweeping celebratory curves & cosmic super-highway
            if world_y < 0.0 or world_y >= STAGE_TRACK_LENGTH - 2400.0:
                return (normal_left, normal_right)
                
            seg_len = 2400.0
            seg_idx = int(world_y / seg_len)
            seg_pos = world_y % seg_len
            pattern = abs(seg_idx) % 4
            
            shift = 0.0
            if pattern == 0:
                # Wide sweeping left curve
                if 250.0 <= seg_pos < 850.0:
                    t = (seg_pos - 250.0) / 600.0
                    shift = -120.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1600.0:
                    shift = -120.0
                elif 1600.0 <= seg_pos < 2200.0:
                    t = (seg_pos - 1600.0) / 600.0
                    shift = -120.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 1:
                # Wide sweeping right curve
                if 250.0 <= seg_pos < 850.0:
                    t = (seg_pos - 250.0) / 600.0
                    shift = 120.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 850.0 <= seg_pos < 1600.0:
                    shift = 120.0
                elif 1600.0 <= seg_pos < 2200.0:
                    t = (seg_pos - 1600.0) / 600.0
                    shift = 120.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            elif pattern == 2:
                # Gentle cosmic S-chicane
                if 200.0 <= seg_pos < 700.0:
                    t = (seg_pos - 200.0) / 500.0
                    shift = -90.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 700.0 <= seg_pos < 1550.0:
                    t = (seg_pos - 700.0) / 850.0
                    shift = -90.0 + 180.0 * (0.5 - 0.5 * math.cos(t * math.pi))
                elif 1550.0 <= seg_pos < 2050.0:
                    t = (seg_pos - 1550.0) / 500.0
                    shift = 90.0 * (0.5 + 0.5 * math.cos(t * math.pi))
            else:
                # High-speed straightaway with subtle undulating drift
                shift = 20.0 * math.sin((world_y / 400.0) * math.pi)
                
            return (normal_left + shift, normal_right + shift)
            
        return (normal_left, normal_right)

    def draw_tiled_texture(self, surface, tex, rect):
        """Blit a repeating texture across rect."""
        if not tex:
            return
        tw, th = tex.get_size()
        rx, ry, rw, rh = int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3])
        # Simple sub-surface or clipped tiling
        surface.set_clip(pygame.Rect(rx, ry, rw, rh))
        for x in range(rx, rx + rw, tw):
            for y in range(ry, ry + rh, th):
                surface.blit(tex, (x, y))
        surface.set_clip(None)

    def draw_scrolling_texture(self, surface, tex, rect, offset_x=0.0, offset_y=0.0, alpha=255):
        """Blit a repeating texture across rect with seamless offset scrolling."""
        if not tex:
            return
        tw, th = tex.get_size()
        rx, ry, rw, rh = int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3])
        
        ox = int(offset_x) % tw
        oy = int(offset_y) % th
        
        start_x = rx - ox
        if start_x > rx:
            start_x -= tw
        start_y = ry - oy
        if start_y > ry:
            start_y -= th
            
        old_alpha = tex.get_alpha()
        if alpha < 255:
            tex.set_alpha(alpha)
            
        surface.set_clip(pygame.Rect(rx, ry, rw, rh))
        for x in range(start_x, rx + rw, tw):
            for y in range(start_y, ry + rh, th):
                surface.blit(tex, (x, y))
        surface.set_clip(None)
        
        if alpha < 255:
            tex.set_alpha(old_alpha if old_alpha is not None else 255)

    def render(self, surface: pygame.Surface, stage: int, track_dist: float, player_screen_y: float = None):
        self.frames += 1
        self.current_stage = stage
        self.track_distance = track_dist
        self.screen_height = surface.get_height()
        self.player_screen_y = player_screen_y if player_screen_y is not None else (self.screen_height - 240.0)
        
        if stage == 1:
            self._render_stage1(surface)
        elif stage == 2:
            self._render_stage2(surface)
        elif stage == 3:
            self._render_stage3(surface)
        elif stage == 4:
            self._render_stage4(surface)
        elif stage == 5:
            self._render_stage5(surface)
        elif stage == 6:
            self._render_stage6(surface)
        elif stage == 7:
            self._render_stage7(surface)
        elif stage == 8:
            self._render_stage8(surface)
        elif stage == 9:
            self._render_stage9(surface)
        elif stage == 10:
            self._render_stage10(surface)
        elif stage == 11:
            self._render_stage11(surface)
        else:
            self._render_stage10(surface)
            
        self._render_finish_line(surface)

    def _render_stage1(self, surface: pygame.Surface):
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        # Grass terrain across entire viewport
        self.draw_tiled_texture(surface, self.tex_grass, (GAME_X, 0, GAME_W, scr_h))
        
        # Asphalt
        road_left = GAME_X + ROAD_MARGIN
        road_w = GAME_W - (ROAD_MARGIN * 2.0)
        self.draw_tiled_texture(surface, self.tex_asphalt, (road_left, 0, road_w, scr_h))
        
        # Lane Markings & Curbs
        lane_w = road_w / 4.0
        slice_h = 6
        for y in range(0, scr_h, slice_h):
            dash_y = (y + int(self.track_distance)) % 60
            if dash_y < 30:
                # White lane dividers
                pygame.draw.rect(surface, (240, 240, 240), (road_left + lane_w - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (240, 240, 240), (road_left + lane_w * 3.0 - 1.5, y, 3, slice_h))
                # Yellow center divider
                pygame.draw.rect(surface, (255, 215, 30), (road_left + lane_w * 2.0 - 2.0, y, 4, slice_h))
                
            # Curbs
            is_red = ((int(y + self.track_distance) // 16) % 2 == 0)
            curb_col = COLOR_BARRIER_RED if is_red else COLOR_WHITE
            pygame.draw.rect(surface, curb_col, (road_left - 8, y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (road_left + road_w, y, 8, slice_h))
            
        # Trees with 3D Drop Shadows
        for tx, ty in self.stage1_trees:
            scr_y = ply_y - (ty - self.track_distance)
            if -120 <= scr_y <= scr_h + 120 and self.sprite_tree:
                r_l, r_r = self.get_road_edges(1, ty)
                half_w = self.tree_w // 2
                if tx < (r_l + r_r) * 0.5:
                    tx = min(tx, r_l - 48.0 - half_w)
                else:
                    tx = max(tx, r_r + 24.0 + half_w)
                # 3D Drop Shadow on grass (anchored at trunk base)
                surface.blit(self.shadow_tree, (tx - 24, scr_y - 14))
                # 3D Tree sprite
                surface.blit(self.sprite_tree, (tx - self.tree_w // 2, scr_y - self.tree_h))

    def _render_stage2(self, surface: pygame.Surface):
        slice_h = 6
        wave_time = self.frames * 0.04
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        
        # 1. Base deep ocean with forward vehicle speed + current drift
        base_ox = math.sin(wave_time * 0.35) * 32.0
        base_oy = self.track_distance * 0.4 + self.frames * 1.2
        self.draw_scrolling_texture(surface, self.tex_deep_ocean or self.tex_water, (GAME_X, 0, GAME_W, scr_h), base_ox, base_oy)

        # 2. Shimmering sunlight caustics layer (scrolling diagonally with soft blend)
        if self.tex_caustics:
            caustic_ox = math.cos(wave_time * 0.45) * 42.0 + self.frames * 0.7
            caustic_oy = -self.track_distance * 0.22 - self.frames * 1.1
            self.draw_scrolling_texture(surface, self.tex_caustics, (GAME_X, 0, GAME_W, scr_h), caustic_ox, caustic_oy, alpha=135)

        # 3. Ambient wave crest drift
        if self.tex_foam_wake:
            foam_ox = self.frames * 0.5
            foam_oy = self.track_distance * 0.32 + self.frames * 1.8
            self.draw_scrolling_texture(surface, self.tex_foam_wake, (GAME_X, 0, GAME_W, scr_h), foam_ox, foam_oy, alpha=45)

        for y in range(0, scr_h, slice_h):
            world_y = self.track_distance + (ply_y - y)
            r_left, r_right = self.get_road_edges(2, world_y)
            r_w = r_right - r_left
            
            deck_l = r_left - 24.0
            deck_r = r_right + 24.0
            
            # Bridge Pylons with hydrodynamic wake
            pylon_cycle = int(world_y) % 400
            if pylon_cycle < 48:
                pyl_w = 28.0
                pl_x = deck_l - pyl_w - 4.0
                pr_x = deck_r + 4.0
                
                # Underwater foundation base shadow
                pygame.draw.rect(surface, (4, 15, 30), (pl_x - 8, y, pyl_w + 16, slice_h))
                pygame.draw.rect(surface, (4, 15, 30), (pr_x - 8, y, pyl_w + 16, slice_h))
                
                # Concrete pillar with 3D beveled lighting
                pygame.draw.rect(surface, (115, 122, 128), (pl_x, y, pyl_w, slice_h))
                pygame.draw.rect(surface, (115, 122, 128), (pr_x, y, pyl_w, slice_h))
                pygame.draw.rect(surface, (165, 172, 180), (pl_x, y, 5, slice_h))
                pygame.draw.rect(surface, (165, 172, 180), (pr_x, y, 5, slice_h))
                pygame.draw.rect(surface, (75, 80, 85), (pl_x + pyl_w - 5, y, 5, slice_h))
                pygame.draw.rect(surface, (75, 80, 85), (pr_x + pyl_w - 5, y, 5, slice_h))
                
                # Hydrodynamic wake foam around pylon
                wake_pulse = math.sin(wave_time * 3.0 + y * 0.15) * 4.0
                wake_w = int(12.0 + wake_pulse)
                if self.surf_wake:
                    surface.blit(self.surf_wake, (pl_x - wake_w, y))
                    surface.blit(self.surf_wake, (pl_x + pyl_w, y))
                    surface.blit(self.surf_wake, (pr_x - wake_w, y))
                    surface.blit(self.surf_wake, (pr_x + pyl_w, y))
                    
            # Translucent Bridge Shadow onto water
            if self.surf_bridge_shadow:
                surface.blit(self.surf_bridge_shadow, (deck_l - 32, y))
                surface.blit(self.surf_bridge_shadow, (deck_r, y))
                
            # Bridge Catwalks & Cantilever
            pygame.draw.rect(surface, (125, 130, 135), (deck_l, y, 24, slice_h))
            pygame.draw.rect(surface, (125, 130, 135), (deck_r - 24, y, 24, slice_h))
            
            # Railing
            pygame.draw.rect(surface, COLOR_RAILING, (deck_l, y, 3, slice_h))
            pygame.draw.rect(surface, COLOR_RAILING, (deck_r - 3, y, 3, slice_h))
            
            # Asphalt
            pygame.draw.rect(surface, (61, 64, 69), (r_left, y, r_w, slice_h))
            
            # Dashed lanes
            lane_w = r_w / 4.0
            dash_cycle = (int(y + self.track_distance)) % 60
            if dash_cycle < 30:
                pygame.draw.rect(surface, (240, 240, 240), (r_left + lane_w - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (240, 240, 240), (r_left + lane_w * 3.0 - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (255, 215, 30), (r_left + lane_w * 2.0 - 2.0, y, 4, slice_h))
                
            # Curbs
            is_red = ((int(y + self.track_distance) // 16) % 2 == 0)
            curb_col = COLOR_BARRIER_RED if is_red else COLOR_WHITE
            pygame.draw.rect(surface, curb_col, (r_left - 8, y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (r_right, y, 8, slice_h))

        # Specular Sunlight Sparkles across open water (masked away from bridge)
        for sx, sy, phase, spd in self.ocean_sparkles:
            world_sy = self.track_distance + (ply_y - sy)
            sl, sr = self.get_road_edges(2, world_sy)
            if (sx < sl - 36.0) or (sx > sr + 36.0):
                twinkle = math.sin(wave_time * spd + phase)
                if twinkle > 0.65:
                    sz = int((twinkle - 0.65) * 6.0) + 1
                    col = (255, 255, 255)
                    pygame.draw.circle(surface, col, (int(sx), int(sy)), max(1, sz - 1))
                    if sz >= 3:
                        pygame.draw.line(surface, (220, 245, 255), (sx - sz, sy), (sx + sz, sy), 1)
                        pygame.draw.line(surface, (220, 245, 255), (sx, sy - sz), (sx, sy + sz), 1)

    def _render_stage3(self, surface: pygame.Surface):
        slice_h = 6
        wave_time = self.frames * 0.04
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        
        # Base Sand background
        self.draw_tiled_texture(surface, self.tex_sand, (GAME_X, 0, GAME_W, scr_h))
        
        # Ocean Backdrop on right half with dual-layer flow
        ocean_base_x = GAME_X + GAME_W * 0.42
        ocean_base_w = GAME_W * 0.58
        base_ox = math.sin(wave_time * 0.3) * 25.0
        base_oy = self.track_distance * 0.35 + self.frames * 1.0
        self.draw_scrolling_texture(surface, self.tex_deep_ocean or self.tex_water, (ocean_base_x, 0, ocean_base_w, scr_h), base_ox, base_oy)
        if self.tex_caustics:
            caustic_ox = math.cos(wave_time * 0.4) * 35.0 + self.frames * 0.6
            caustic_oy = -self.track_distance * 0.2 - self.frames * 0.9
            self.draw_scrolling_texture(surface, self.tex_caustics, (ocean_base_x, 0, ocean_base_w, scr_h), caustic_ox, caustic_oy, alpha=120)
        
        for y in range(0, scr_h, slice_h):
            world_y = self.track_distance + (ply_y - y)
            r_left, r_right = self.get_road_edges(3, world_y)
            r_w = r_right - r_left
            
            # Left Sand Verge
            sand_l_w = r_left - GAME_X
            if sand_l_w > 0:
                pygame.draw.rect(surface, (235, 214, 158), (GAME_X, y, sand_l_w, slice_h))
                
            # Right Shoreline & Waves
            dry_sand_edge = r_right + 8.0
            wave_surge = math.sin(wave_time * 1.6 + world_y * 0.014) * 16.0 + math.cos(wave_time * 0.7 + y * 0.03) * 7.0
            max_wash_reach = r_right + 18.0
            water_edge_x = max(max_wash_reach, min(GAME_X + GAME_W - 50.0, r_right + 42.0 - wave_surge))
            
            if water_edge_x > dry_sand_edge:
                pygame.draw.rect(surface, (235, 212, 153), (dry_sand_edge, y, water_edge_x - dry_sand_edge, slice_h))
                
            # Wet Sand Zone
            if water_edge_x > max_wash_reach:
                wet_w = min(water_edge_x - max_wash_reach, 24.0)
                pygame.draw.rect(surface, (168, 140, 97), (water_edge_x - wet_w, y, wet_w, slice_h))
                
            # Multi-depth ocean
            ocean_w = (GAME_X + GAME_W) - water_edge_x
            if ocean_w > 0:
                # Turquoise shallows
                shallow_w = min(ocean_w, 65.0)
                pygame.draw.rect(surface, (20, 158, 184), (water_edge_x, y, shallow_w, slice_h))
                
                # Mid-depth azure
                if ocean_w > 65.0:
                    mid_w = min(ocean_w - 65.0, 125.0)
                    pygame.draw.rect(surface, (10, 97, 148), (water_edge_x + 65.0, y, mid_w, slice_h))
                    
                # Deep ocean
                if ocean_w > 190.0:
                    deep_w = ocean_w - 190.0
                    pygame.draw.rect(surface, COLOR_WATER_DEEP, (water_edge_x + 190.0, y, deep_w, slice_h))
                    
                # Swell 1
                swell1_x = water_edge_x + 75.0 + math.sin(wave_time * 1.8 + world_y * 0.02) * 22.0
                if swell1_x < (GAME_X + GAME_W) - 15.0:
                    pygame.draw.rect(surface, (46, 184, 209), (swell1_x, y, 22, slice_h))
                    pygame.draw.rect(surface, (224, 245, 255), (swell1_x + 1, y, 4, slice_h))
                    
                # Breaking surf foam
                foam_w = 9.0 + math.sin(wave_time * 2.8 + world_y * 0.04) * 4.0
                pygame.draw.rect(surface, (245, 252, 255), (water_edge_x - 2, y, foam_w, slice_h))
                
            # Asphalt
            pygame.draw.rect(surface, (61, 64, 69), (r_left, y, r_w, slice_h))
            
            # Dashed lanes
            lane_w = r_w / 4.0
            dash_cycle = (int(y + self.track_distance)) % 60
            if dash_cycle < 30:
                pygame.draw.rect(surface, (240, 240, 240), (r_left + lane_w - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (240, 240, 240), (r_left + lane_w * 3.0 - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (255, 215, 30), (r_left + lane_w * 2.0 - 2.0, y, 4, slice_h))
                
            # Curbs
            is_red = ((int(y + self.track_distance) // 16) % 2 == 0)
            curb_col = COLOR_BARRIER_RED if is_red else COLOR_WHITE
            pygame.draw.rect(surface, curb_col, (r_left - 8, y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (r_right, y, 8, slice_h))
            
        # Palm Trees with 3D Drop Shadows
        for px, py in self.stage3_palms:
            scr_y = ply_y - (py - self.track_distance)
            if -120 <= scr_y <= scr_h + 120 and self.sprite_palm:
                r_l, r_r = self.get_road_edges(3, py)
                margin = 24.0 + self.palm_w // 2
                if px < (r_l + r_r) * 0.5:
                    px = min(px, r_l - margin)
                else:
                    px = max(px, r_r + margin)
                # 3D Drop Shadow on beach sand
                surface.blit(self.shadow_palm, (px - 22, scr_y - 14))
                # 3D Palm tree sprite
                surface.blit(self.sprite_palm, (px - self.palm_w // 2, scr_y - self.palm_h))

    def _render_stage4(self, surface: pygame.Surface):
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        # Base rocky ground across entire viewport
        self.draw_tiled_texture(surface, self.tex_rock_ground, (GAME_X, 0, GAME_W, scr_h))
        
        slice_h = 6
        for y in range(0, scr_h, slice_h):
            world_y = self.track_distance + (ply_y - y)
            r_left, r_right = self.get_road_edges(4, world_y)
            r_w = r_right - r_left
            
            # Cliff Rock Walls on boundaries
            cliff_l = r_left - 24.0
            if cliff_l > GAME_X:
                pygame.draw.rect(surface, (46, 41, 38), (GAME_X, y, 40, slice_h))
                pygame.draw.rect(surface, (71, 64, 56), (GAME_X + 40, y, cliff_l - (GAME_X + 40), slice_h))
                if int(world_y * 0.1) % 14 < 3:
                    pygame.draw.rect(surface, (122, 112, 97), (GAME_X + 15, y, 18, slice_h))
                    
            cliff_r = r_right + 24.0
            if cliff_r < GAME_X + GAME_W:
                pygame.draw.rect(surface, (71, 64, 56), (cliff_r, y, (GAME_X + GAME_W - 40) - cliff_r, slice_h))
                pygame.draw.rect(surface, (46, 41, 38), (GAME_X + GAME_W - 40, y, 40, slice_h))
                if int(world_y * 0.1) % 14 < 3:
                    pygame.draw.rect(surface, (122, 112, 97), (GAME_X + GAME_W - 33, y, 18, slice_h))
                    
            # Gravel shoulders
            pygame.draw.rect(surface, (56, 51, 46), (r_left - 24, y, 16, slice_h))
            pygame.draw.rect(surface, (56, 51, 46), (r_right + 8, y, 16, slice_h))
            
            # Asphalt
            pygame.draw.rect(surface, (56, 56, 61), (r_left, y, r_w, slice_h))
            
            # Lane markings & Bottlenecks
            dash_cycle = (int(y + self.track_distance)) % 60
            if r_w < 520.0:
                # Narrow gorge bottleneck: 2-lane layout with yellow center line
                half_w = r_w * 0.5
                if dash_cycle < 30:
                    pygame.draw.rect(surface, (255, 215, 30), (r_left + half_w - 2.0, y, 4, slice_h))
                # Hazard stripes on shoulders
                if (int(world_y * 0.05) % 8) < 4:
                    pygame.draw.rect(surface, (255, 178, 25), (r_left - 18, y, 8, slice_h))
                    pygame.draw.rect(surface, (255, 178, 25), (r_right + 10, y, 8, slice_h))
            else:
                lane_w = r_w / 4.0
                if dash_cycle < 30:
                    pygame.draw.rect(surface, (235, 235, 235), (r_left + lane_w - 1.5, y, 3, slice_h))
                    pygame.draw.rect(surface, (235, 235, 235), (r_left + lane_w * 3.0 - 1.5, y, 3, slice_h))
                    pygame.draw.rect(surface, (255, 215, 30), (r_left + lane_w * 2.0 - 2.0, y, 4, slice_h))
                    
            # Curbs
            is_red = ((int(y + self.track_distance) // 16) % 2 == 0)
            curb_col = COLOR_BARRIER_RED if is_red else COLOR_WHITE
            pygame.draw.rect(surface, curb_col, (r_left - 8, y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (r_right, y, 8, slice_h))
            
            # Barrier posts
            if int(world_y) % 80 < 10:
                pygame.draw.rect(surface, (191, 199, 209), (r_left - 11, y, 3, slice_h))
                pygame.draw.rect(surface, (191, 199, 209), (r_right + 8, y, 3, slice_h))
                
        # Scenery: Pines & Boulders with 3D Drop Shadows
        for item in self.stage4_scenery:
            px, py = item["pos"]
            is_pine = item["is_pine"]
            scr_y = ply_y - (py - self.track_distance)
            if -100 <= scr_y <= scr_h + 100:
                r_l, r_r = self.get_road_edges(4, py)
                half_w = self.pine_w // 2 if is_pine else self.boulder_w // 2
                margin = 24.0 + half_w
                if px < (r_l + r_r) * 0.5:
                    px = min(px, r_l - margin)
                else:
                    px = max(px, r_r + margin)
                if is_pine and self.sprite_pine:
                    # Tiered conical foliage shadow on rocky ground
                    surface.blit(self.shadow_pine, (px - 19, scr_y - 20))
                    # 3D Pine tree sprite
                    surface.blit(self.sprite_pine, (px - self.pine_w // 2, scr_y - self.pine_h))
                elif not is_pine and self.sprite_boulder:
                    # Ground contact + ambient penumbra shadow
                    surface.blit(self.shadow_boulder, (px - self.boulder_w // 2 - 4, scr_y - int(self.boulder_h * 0.40)))
                    # 3D Boulder sprite
                    surface.blit(self.sprite_boulder, (px - self.boulder_w // 2, scr_y - self.boulder_h))

    def _render_stage5(self, surface: pygame.Surface):
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        # 1. Midnight / Twilight Night Sky Base
        pygame.draw.rect(surface, (10, 14, 24), (GAME_X, 0, GAME_W, scr_h))
        
        # 2. Elevated Expressway Concrete Deck across Entire Viewport
        self.draw_tiled_texture(surface, self.tex_concrete, (GAME_X, 0, GAME_W, scr_h))
        
        # Nighttime atmospheric shading on concrete
        night_shading = pygame.Surface((int(GAME_W), scr_h), pygame.SRCALPHA)
        night_shading.fill((10, 14, 26, 185))
        surface.blit(night_shading, (GAME_X, 0))
        
        # 3. Skyscraper Silhouettes in Background Verges
        for b in self.stage5_buildings:
            bx, by, bw, bh = b["x"], b["y"], b["w"], b["h"]
            scr_y = ply_y - (by - self.track_distance)
            if -bh <= scr_y <= scr_h + 50:
                # Building facade
                b_rect = pygame.Rect(int(bx), int(scr_y), int(bw), int(bh))
                pygame.draw.rect(surface, b["col"], b_rect)
                pygame.draw.rect(surface, (12, 16, 26), b_rect, 1)
                
                # Rooftop beacon light
                if b["beacon"]:
                    is_blink = (int(self.frames // 18) % 2 == 0)
                    if is_blink:
                        pygame.draw.circle(surface, (255, 40, 40), (int(bx + bw * 0.5), int(scr_y - 2)), 3)
                        pygame.draw.circle(surface, (255, 140, 140), (int(bx + bw * 0.5), int(scr_y - 2)), 1)
                        
                # Window grid
                wins = b["windows"]
                for r_idx, row in enumerate(wins):
                    wy = scr_y + 16 + r_idx * 18
                    if 0 <= wy <= scr_h:
                        for c_idx, w_col in enumerate(row):
                            wx = bx + 8 + c_idx * 14
                            pygame.draw.rect(surface, w_col, (int(wx), int(wy), 8, 10))

        # 4. Slices: Roadway, Asphalt, Neon Curbs, and Reflective Markings
        slice_h = 6
        for y in range(0, scr_h, slice_h):
            world_y = self.track_distance + (ply_y - y)
            r_left, r_right = self.get_road_edges(5, world_y)
            r_w = r_right - r_left
            
            # Outer Elevated Railing Barrier
            guard_l = r_left - 18.0
            guard_r = r_right + 18.0
            pygame.draw.rect(surface, (25, 30, 42), (guard_l, y, 18, slice_h))
            pygame.draw.rect(surface, (25, 30, 42), (r_right, y, 18, slice_h))
            
            # Sleek Dark Midnight Asphalt
            pygame.draw.rect(surface, (36, 38, 44), (r_left, y, r_w, slice_h))
            
            # Dashed Lane Dividers (Bright Cool White)
            lane_w = r_w / 4.0
            dash_cycle = (int(y + self.track_distance)) % 60
            if dash_cycle < 30:
                pygame.draw.rect(surface, (235, 245, 255), (r_left + lane_w - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (235, 245, 255), (r_left + lane_w * 3.0 - 1.5, y, 3, slice_h))
                # Double Amber Center Line
                pygame.draw.rect(surface, (255, 195, 25), (r_left + lane_w * 2.0 - 3.0, y, 2, slice_h))
                pygame.draw.rect(surface, (255, 195, 25), (r_left + lane_w * 2.0 + 1.0, y, 2, slice_h))
                
            # Neon Curbs (Alternating Electric Cyan & Vivid Amber)
            curb_cycle = (int(y + self.track_distance) // 20) % 2
            curb_col = COLOR_NEON_CYAN if curb_cycle == 0 else COLOR_NEON_AMBER
            pygame.draw.rect(surface, curb_col, (r_left - 8, y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (r_right, y, 8, slice_h))
            
            # Glowing Cat's-Eye Reflectors along Barriers every 50m
            if int(world_y) % 50 < 6:
                pygame.draw.rect(surface, (0, 240, 255), (r_left - 14, y + 1, 4, 4))
                pygame.draw.rect(surface, (0, 240, 255), (r_right + 10, y + 1, 4, 4))

        # 5. Street Light Lamp Posts along Highway Shoulders
        for ly in self.stage5_lamps:
            scr_y = ply_y - (ly - self.track_distance)
            if -80 <= scr_y <= scr_h + 80:
                r_l, r_r = self.get_road_edges(5, ly)
                
                # Left Lamp Post
                lp_lx = r_l - 22.0
                # 3D Drop Shadow on concrete shoulder
                pygame.draw.line(surface, (0, 0, 0, 75), (lp_lx + 2, scr_y), (lp_lx + 24, scr_y + 16), 3)
                pygame.draw.ellipse(surface, (0, 0, 0, 90), (lp_lx + 18, scr_y + 12, 12, 7))
                pygame.draw.rect(surface, (140, 150, 165), (lp_lx, scr_y - 45, 4, 45))
                pygame.draw.rect(surface, (170, 180, 195), (lp_lx, scr_y - 45, 16, 4)) # Arm pointing right
                pygame.draw.rect(surface, (255, 250, 210), (lp_lx + 12, scr_y - 43, 6, 5)) # Lamp head
                # Translucent light glow
                pygame.draw.circle(surface, (255, 245, 180), (int(lp_lx + 15), int(scr_y - 40)), 7)
                
                # Right Lamp Post
                lp_rx = r_r + 22.0
                # 3D Drop Shadow on concrete shoulder
                pygame.draw.line(surface, (0, 0, 0, 75), (lp_rx - 2, scr_y), (lp_rx + 20, scr_y + 16), 3)
                pygame.draw.ellipse(surface, (0, 0, 0, 90), (lp_rx + 14, scr_y + 12, 12, 7))
                pygame.draw.rect(surface, (140, 150, 165), (lp_rx - 4, scr_y - 45, 4, 45))
                pygame.draw.rect(surface, (170, 180, 195), (lp_rx - 16, scr_y - 45, 16, 4)) # Arm pointing left
                pygame.draw.rect(surface, (255, 250, 210), (lp_rx - 18, scr_y - 43, 6, 5)) # Lamp head
                # Translucent light glow
                pygame.draw.circle(surface, (255, 245, 180), (int(lp_rx - 15), int(scr_y - 40)), 7)

        # 6. Overhead Expressway Gantries
        for gy in self.stage5_gantries:
            scr_y = ply_y - (gy - self.track_distance)
            if -80 <= scr_y <= scr_h + 80:
                r_l, r_r = self.get_road_edges(5, gy)
                gw = (r_r - r_l) + 50.0
                gx = r_l - 25.0
                
                # 3D Pillar Base Shadows
                pygame.draw.ellipse(surface, (0, 0, 0, 110), (gx - 2, scr_y - 4, 14, 8))
                pygame.draw.ellipse(surface, (0, 0, 0, 110), (gx + gw - 10, scr_y - 4, 14, 8))
                
                # Steel Truss Arch
                pygame.draw.rect(surface, (85, 95, 110), (gx, scr_y - 65, gw, 10))
                pygame.draw.rect(surface, (110, 120, 135), (gx, scr_y - 65, gw, 2))
                # Pillars
                pygame.draw.rect(surface, (70, 80, 95), (gx, scr_y - 65, 8, 65))
                pygame.draw.rect(surface, (70, 80, 95), (gx + gw - 8, scr_y - 65, 8, 65))
                
                # Highway Directional Signs (Japanese Green Highway Signs)
                sign_w = gw * 0.42
                sign_h = 32
                s1_x = gx + 20
                s2_x = gx + gw - sign_w - 20
                for sx, txt_code in [(s1_x, "C1 首都高 // SHUTO"), (s2_x, "湾岸線 // WANGAN")]:
                    pygame.draw.rect(surface, (16, 120, 68), (sx, scr_y - 60, sign_w, sign_h), border_radius=3)
                    pygame.draw.rect(surface, (240, 245, 250), (sx, scr_y - 60, sign_w, sign_h), 1, border_radius=3)
                    if hasattr(self, 'font_gantry') and self.font_gantry:
                        ts = self.font_gantry.render(txt_code, True, (255, 255, 255))
                        surface.blit(ts, ts.get_rect(center=(int(sx + sign_w * 0.5), int(scr_y - 44))))

    def _render_stage6(self, surface: pygame.Surface):
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        
        # 1. Dark Volcanic Twilight Sky & Basalt Bedrock Base
        pygame.draw.rect(surface, (18, 12, 16), (GAME_X, 0, GAME_W, scr_h))
        
        # 2. Volcanic Rock Ground across Entire Terrain
        self.draw_tiled_texture(surface, self.tex_rock_ground, (GAME_X, 0, GAME_W, scr_h))
        
        # Dark volcanic ash shading overlay across entire terrain
        ash_overlay = pygame.Surface((int(GAME_W), scr_h), pygame.SRCALPHA)
        ash_overlay.fill((25, 12, 16, 175))
        surface.blit(ash_overlay, (GAME_X, 0))
        
        # 3. Glowing Magma Vents / Caldera Fissures in the verges
        import time
        pulse = 0.5 + 0.5 * math.sin(time.time() * 3.5)
        for vent in self.stage6_magma_vents:
            vx, vy, vr = vent["x"], vent["y"], vent["radius"]
            scr_y = ply_y - (vy - self.track_distance)
            if -40 <= scr_y <= scr_h + 40:
                r_l, r_r = self.get_road_edges(6, vy)
                margin = 22.0 + vr
                if vx < (r_l + r_r) * 0.5:
                    vx = min(vx, r_l - margin)
                else:
                    vx = max(vx, r_r + margin)
                pygame.draw.circle(surface, (180, 40, 10), (int(vx), int(scr_y)), int(vr))
                pygame.draw.circle(surface, (255, 95, 20), (int(vx), int(scr_y)), int(vr * 0.7))
                pygame.draw.circle(surface, (255, 200, 50), (int(vx), int(scr_y)), int(vr * 0.4 * (0.8 + pulse * 0.4)))
                
        # 4. Scorched Trees & Basalt Crags with 3D Drop Shadows
        for item in self.stage6_scenery:
            px, py = item["pos"]
            is_pine = item["is_pine"]
            scr_y = ply_y - (py - self.track_distance)
            if -100 <= scr_y <= scr_h + 100:
                r_l, r_r = self.get_road_edges(6, py)
                half_w = self.pine_w // 2 if is_pine else self.boulder_w // 2
                margin = 24.0 + half_w
                if px < (r_l + r_r) * 0.5:
                    px = min(px, r_l - margin)
                else:
                    px = max(px, r_r + margin)
                if is_pine and self.sprite_pine:
                    # Conical shadow on volcanic basalt
                    surface.blit(self.shadow_pine, (px - 19, scr_y - 20))
                    surface.blit(self.sprite_pine, (px - self.pine_w // 2, scr_y - self.pine_h))
                elif not is_pine and self.sprite_boulder:
                    # Heavy basalt rock contact + ambient penumbra
                    surface.blit(self.shadow_boulder, (px - self.boulder_w // 2 - 4, scr_y - int(self.boulder_h * 0.40)))
                    surface.blit(self.sprite_boulder, (px - self.boulder_w // 2, scr_y - self.boulder_h))
                    
        # 5. Slices: Roadway, Asphalt, Fiery Curbs, Road Markings
        slice_h = 6
        for y in range(0, scr_h, slice_h):
            world_y = self.track_distance + (ply_y - y)
            r_left, r_right = self.get_road_edges(6, world_y)
            r_w = r_right - r_left
            
            # Heavy Rock-Guard Barrier
            pygame.draw.rect(surface, (40, 25, 28), (r_left - 16.0, y, 16, slice_h))
            pygame.draw.rect(surface, (40, 25, 28), (r_right, y, 16, slice_h))
            
            # Dark Basalt Asphalt Road Surface
            pygame.draw.rect(surface, (34, 32, 36), (r_left, y, r_w, slice_h))
            
            # Dashed Lane Dividers (Warm White / Pale Ember)
            lane_w = r_w / 4.0
            dash_cycle = (int(y + self.track_distance)) % 60
            if dash_cycle < 30:
                pygame.draw.rect(surface, (245, 235, 220), (r_left + lane_w - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (245, 235, 220), (r_left + lane_w * 3.0 - 1.5, y, 3, slice_h))
                # Double Magma Gold Center Line
                pygame.draw.rect(surface, (255, 175, 25), (r_left + lane_w * 2.0 - 3.0, y, 2, slice_h))
                pygame.draw.rect(surface, (255, 175, 25), (r_left + lane_w * 2.0 + 1.0, y, 2, slice_h))
                
            # Fiery Neon Curbs (Alternating Vivid Magma Amber & Molten Red)
            curb_cycle = (int(y + self.track_distance) // 18) % 2
            curb_col = (255, 130, 20) if curb_cycle == 0 else (225, 40, 25)
            pygame.draw.rect(surface, curb_col, (r_left - 8, y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (r_right, y, 8, slice_h))
            
            # Glowing amber hazard reflectors along road edge every 40m
            if int(world_y) % 40 < 6:
                pygame.draw.rect(surface, (255, 195, 40), (r_left - 12, y + 1, 4, 4))
                pygame.draw.rect(surface, (255, 195, 40), (r_right + 8, y + 1, 4, 4))

    def _render_stage7(self, surface: pygame.Surface):
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        
        # 1. Polar Twilight Sky & Glacial Bedrock Base
        pygame.draw.rect(surface, (10, 16, 28), (GAME_X, 0, GAME_W, scr_h))
        
        # 2. Frozen Rock Ground across Entire Terrain
        self.draw_tiled_texture(surface, self.tex_rock_ground, (GAME_X, 0, GAME_W, scr_h))
        
        # Frost & Snowfield overlay (sub-zero glacial white-cyan tint) across entire terrain
        frost_overlay = pygame.Surface((int(GAME_W), scr_h), pygame.SRCALPHA)
        frost_overlay.fill((210, 235, 255, 195))
        surface.blit(frost_overlay, (GAME_X, 0))
        
        # 3. Crystalline Ice Spires / Frozen Formations in the verges
        import time
        now = time.time()
        for crystal in self.stage7_ice_crystals:
            cx, cy = crystal["x"], crystal["y"]
            ch, cw = crystal["height"], crystal["width"]
            scr_y = ply_y - (cy - self.track_distance)
            if -60 <= scr_y <= scr_h + 60:
                r_l, r_r = self.get_road_edges(7, cy)
                margin = 20.0 + cw * 0.5
                if cx < (r_l + r_r) * 0.5:
                    cx = min(cx, r_l - margin)
                else:
                    cx = max(cx, r_r + margin)
                # Sparkling shimmer factor
                shimmer = 0.5 + 0.5 * math.sin(now * 4.0 + cy * 0.05)
                # Outer diamond ice spire
                pts_outer = [
                    (cx, scr_y - ch),
                    (cx + cw * 0.5, scr_y - ch * 0.3),
                    (cx, scr_y),
                    (cx - cw * 0.5, scr_y - ch * 0.3)
                ]
                # 3D Ice Crystal Drop Shadow on snow (cool blue-tinted shadow cast down-right)
                pygame.draw.ellipse(surface, (15, 30, 60, 110), (int(cx - cw * 0.4), int(scr_y - 4), int(cw * 0.8), 8))
                pygame.draw.polygon(surface, (15, 30, 60, 60), [
                    (cx - cw * 0.3, scr_y),
                    (cx + cw * 0.3, scr_y),
                    (cx + cw * 0.8, scr_y + ch * 0.35),
                    (cx + cw * 0.5, scr_y + ch * 0.35)
                ])

                # Ice-blue outer body
                pygame.draw.polygon(surface, (100, 205, 255), pts_outer)
                pygame.draw.polygon(surface, (180, 235, 255), pts_outer, 1)
                
                # Inner crystalline facet highlight
                pts_inner = [
                    (cx, scr_y - ch),
                    (cx + cw * 0.25, scr_y - ch * 0.3),
                    (cx, scr_y - 2),
                    (cx, scr_y - ch)
                ]
                highlight_val = int(220 + 35 * shimmer)
                pygame.draw.polygon(surface, (highlight_val, 250, 255), pts_inner)
                
                # Apex twinkle glint
                glint_radius = int(2 + 2 * shimmer)
                pygame.draw.circle(surface, (255, 255, 255), (int(cx), int(scr_y - ch)), glint_radius)

        # 4. Snowy Evergreens & Snow-Capped Boulders with 3D Drop Shadows
        for item in self.stage7_scenery:
            px, py = item["pos"]
            is_pine = item["is_pine"]
            scr_y = ply_y - (py - self.track_distance)
            if -100 <= scr_y <= scr_h + 100:
                r_l, r_r = self.get_road_edges(7, py)
                half_w = self.pine_w // 2 if is_pine else self.boulder_w // 2
                margin = 24.0 + half_w
                if px < (r_l + r_r) * 0.5:
                    px = min(px, r_l - margin)
                else:
                    px = max(px, r_r + margin)
                if is_pine and self.sprite_pine:
                    # Blue-tinted soft snow shadow
                    surface.blit(self.shadow_pine, (px - 19, scr_y - 20))
                    surface.blit(self.sprite_pine, (px - self.pine_w // 2, scr_y - self.pine_h))
                    # Crisp white snow caps on the pine foliage tiers
                    # Top tier snow cap
                    pygame.draw.polygon(surface, (248, 252, 255), [
                        (px, scr_y - 66),
                        (px + 10, scr_y - 52),
                        (px, scr_y - 50),
                        (px - 10, scr_y - 52)
                    ])
                    # Middle tier snow cap
                    pygame.draw.polygon(surface, (240, 248, 255), [
                        (px - 16, scr_y - 38),
                        (px, scr_y - 42),
                        (px + 16, scr_y - 38),
                        (px + 12, scr_y - 34),
                        (px - 12, scr_y - 34)
                    ])
                    # Bottom tier snow cap
                    pygame.draw.polygon(surface, (232, 244, 255), [
                        (px - 22, scr_y - 20),
                        (px, scr_y - 24),
                        (px + 22, scr_y - 20),
                        (px + 18, scr_y - 17),
                        (px - 18, scr_y - 17)
                    ])
                elif not is_pine and self.sprite_boulder:
                    # Ground contact shadow on snow
                    surface.blit(self.shadow_boulder, (px - self.boulder_w // 2 - 4, scr_y - int(self.boulder_h * 0.40)))
                    surface.blit(self.sprite_boulder, (px - self.boulder_w // 2, scr_y - self.boulder_h))
                    # Crisp snow cap on top of boulder
                    pygame.draw.ellipse(surface, (242, 250, 255), (px - 22, scr_y - 42, 44, 18))
                    pygame.draw.ellipse(surface, (185, 220, 245), (px - 22, scr_y - 42, 44, 18), 1)

        # 5. Slices: Roadway, Asphalt, Glacier Curbs, Road Markings
        slice_h = 6
        for y in range(0, scr_h, slice_h):
            world_y = self.track_distance + (ply_y - y)
            r_left, r_right = self.get_road_edges(7, world_y)
            r_w = r_right - r_left
            
            # Frosted Heavy Guard Barrier (Steel blue with icy trim)
            pygame.draw.rect(surface, (45, 62, 80), (r_left - 16.0, y, 16, slice_h))
            pygame.draw.rect(surface, (45, 62, 80), (r_right, y, 16, slice_h))
            pygame.draw.rect(surface, (150, 200, 235), (r_left - 16.0, y, 2, slice_h))
            pygame.draw.rect(surface, (150, 200, 235), (r_right + 14.0, y, 2, slice_h))
            
            # Frosted Slate Asphalt Road Surface
            pygame.draw.rect(surface, (32, 38, 50), (r_left, y, r_w, slice_h))
            
            # Dashed Lane Dividers (Crisp Snow White)
            lane_w = r_w / 4.0
            dash_cycle = (int(y + self.track_distance)) % 60
            if dash_cycle < 30:
                pygame.draw.rect(surface, (245, 250, 255), (r_left + lane_w - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (245, 250, 255), (r_left + lane_w * 3.0 - 1.5, y, 3, slice_h))
                # Double Glacier Cyan Center Line
                pygame.draw.rect(surface, (0, 215, 255), (r_left + lane_w * 2.0 - 3.0, y, 2, slice_h))
                pygame.draw.rect(surface, (0, 215, 255), (r_left + lane_w * 2.0 + 1.0, y, 2, slice_h))
                
            # Glacier Curbs (Alternating Vivid Glacier Cyan & Snow White)
            curb_cycle = (int(y + self.track_distance) // 18) % 2
            curb_col = (0, 195, 245) if curb_cycle == 0 else (245, 250, 255)
            pygame.draw.rect(surface, curb_col, (r_left - 8, y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (r_right, y, 8, slice_h))
            
            # Diamond blue roadside ice reflectors every 40m
            if int(world_y) % 40 < 6:
                pygame.draw.rect(surface, (140, 235, 255), (r_left - 12, y + 1, 4, 4))
                pygame.draw.rect(surface, (140, 235, 255), (r_right + 8, y + 1, 4, 4))

    def _render_stage8(self, surface: pygame.Surface):
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        
        # 1. Spring Twilight Sky (deep violet-rose gradient base)
        pygame.draw.rect(surface, (28, 18, 38), (GAME_X, 0, GAME_W, scr_h))
        
        # 2. Fresh Spring Turf Grass across Entire Terrain
        self.draw_tiled_texture(surface, self.tex_grass, (GAME_X, 0, GAME_W, scr_h))
        
        # Twilight Spring Rose-tint overlay across entire terrain
        verge_overlay = pygame.Surface((int(GAME_W), scr_h), pygame.SRCALPHA)
        verge_overlay.fill((55, 20, 42, 60))
        surface.blit(verge_overlay, (GAME_X, 0))
        
        # 3. Traditional Japanese Stone Lanterns (ishidōrō) along roadside
        import time
        now = time.time()
        for lantern in self.stage8_lanterns:
            lx, ly = lantern["pos"]
            lh = lantern["h"]
            scr_y = ply_y - (ly - self.track_distance)
            if -60 <= scr_y <= scr_h + 60:
                r_l, r_r = self.get_road_edges(8, ly)
                margin = 32.0
                if lx < (r_l + r_r) * 0.5:
                    lx = min(lx, r_l - margin)
                else:
                    lx = max(lx, r_r + margin)
                # 3D Stone Lantern Drop Shadow
                pygame.draw.ellipse(surface, (0, 0, 0, 115), (int(lx - 12), int(scr_y - 6), 26, 12))
                pygame.draw.ellipse(surface, (0, 0, 0, 65), (int(lx - 4), int(scr_y - 2), 30, 16))

                # Stone Base (pedestal / kiso)
                pygame.draw.rect(surface, (110, 115, 125), (lx - 12, scr_y - 8, 24, 8))
                # Stone Column (sao)
                pygame.draw.rect(surface, (130, 135, 145), (lx - 5, scr_y - 22, 10, 14))
                # Middle Platform (chūdai)
                pygame.draw.polygon(surface, (120, 125, 135), [
                    (lx - 14, scr_y - 22), (lx + 14, scr_y - 22),
                    (lx + 8, scr_y - 26), (lx - 8, scr_y - 26)
                ])
                # Light Chamber (hibukuro) - warm amber glow
                glow_flicker = 0.85 + 0.15 * math.sin(now * 3.5 + ly * 0.05)
                amber_val = int(220 * glow_flicker)
                pygame.draw.rect(surface, (255, amber_val, 50), (lx - 8, scr_y - 38, 16, 12))
                # Wooden lattice window frame
                pygame.draw.line(surface, (40, 25, 20), (lx, scr_y - 38), (lx, scr_y - 26), 2)
                pygame.draw.line(surface, (40, 25, 20), (lx - 8, scr_y - 32), (lx + 8, scr_y - 32), 2)
                pygame.draw.rect(surface, (100, 105, 115), (lx - 8, scr_y - 38, 16, 12), 1)
                # Umbrella Roof (kasa) - flanged pagoda eaves
                pygame.draw.polygon(surface, (140, 145, 155), [
                    (lx - 18, scr_y - 38), (lx + 18, scr_y - 38),
                    (lx + 10, scr_y - 46), (lx - 10, scr_y - 46)
                ])
                # Finial Jewel (hōju) on top
                pygame.draw.circle(surface, (160, 165, 175), (int(lx), int(scr_y - 48)), 3)

        # 4. Blooming Cherry Blossom Trees (Sakura Trees) with 3D Drop Shadows
        for item in self.stage8_sakura_trees:
            tx, ty = item["pos"]
            scale = item["scale"]
            tone = item["tone"]
            scr_y = ply_y - (ty - self.track_distance)
            if -120 <= scr_y <= scr_h + 120:
                r_l, r_r = self.get_road_edges(8, ty)
                margin = 24.0 + 35.0 * scale
                if tx < (r_l + r_r) * 0.5:
                    tx = min(tx, r_l - margin)
                else:
                    tx = max(tx, r_r + margin)
                # 3D Drop Shadow: Multi-lobed blossom canopy shadow on grass
                sh_w = int(88 * scale)
                sh_h = int(50 * scale)
                sh_surf = pygame.Surface((sh_w + 20, sh_h + 20), pygame.SRCALPHA)
                puffs = [(-22, -10, 22), (22, -8, 22), (0, -18, 26), (14, 6, 18), (-12, 4, 18)]
                cx_s = (sh_w + 20) // 2
                cy_s = (sh_h + 20) // 2
                for ox, oy, r in puffs:
                    pygame.draw.circle(sh_surf, (0, 0, 0, 35), (cx_s + int(ox * 0.7), cy_s + int(oy * 0.7)), int(r * scale * 0.75 + 4))
                for ox, oy, r in puffs:
                    pygame.draw.circle(sh_surf, (0, 0, 0, 80), (cx_s + int(ox * 0.7), cy_s + int(oy * 0.7)), int(r * scale * 0.75))
                pygame.draw.ellipse(sh_surf, (0, 0, 0, 130), (cx_s - int(24 * scale), cy_s - 2, int(28 * scale), int(12 * scale)))
                surface.blit(sh_surf, (tx + int(18 * scale) - sh_w // 2, scr_y + int(14 * scale) - sh_h // 2))

                # Fallen petals patch on ground beneath tree
                petal_spread = int(32 * scale)
                for pr in range(5):
                    px_f = tx + math.sin(pr * 1.3) * petal_spread * 0.7
                    py_f = scr_y - 4 + math.cos(pr * 1.7) * 8
                    pygame.draw.circle(surface, (255, 185, 205), (int(px_f), int(py_f)), 3)

                # Gnarled Trunk and Main Branches
                tw = int(12 * scale)
                th = int(48 * scale)
                # Trunk base
                pygame.draw.rect(surface, (62, 40, 32), (tx - tw // 2, scr_y - th, tw, th))
                # Trunk texture / highlight
                pygame.draw.line(surface, (88, 58, 46), (tx - tw // 4, scr_y - th), (tx - tw // 4, scr_y - 2), 2)
                # Branches spreading outward
                pygame.draw.line(surface, (62, 40, 32), (tx, scr_y - int(th * 0.7)), (tx - int(24 * scale), scr_y - int(th * 1.1)), int(4 * scale))
                pygame.draw.line(surface, (62, 40, 32), (tx, scr_y - int(th * 0.6)), (tx + int(24 * scale), scr_y - int(th * 1.05)), int(4 * scale))

                # Blossom Canopy: Layered puffs of cherry blossoms
                if tone == 0:
                    base_pink = (235, 140, 165)
                    mid_pink = (255, 182, 198)
                    high_pink = (255, 220, 232)
                elif tone == 1:
                    base_pink = (225, 125, 155)
                    mid_pink = (255, 168, 188)
                    high_pink = (255, 210, 225)
                else:
                    base_pink = (240, 150, 175)
                    mid_pink = (255, 195, 210)
                    high_pink = (255, 230, 240)

                # Multi-tiered blossom cloud puffs (Layer 1: base shadow puffs)
                puffs = [
                    (-22, -44, 22), (22, -42, 22), (0, -56, 26),
                    (-14, -68, 20), (14, -66, 20), (0, -78, 18)
                ]
                for ox, oy, rad in puffs:
                    cx = tx + int(ox * scale)
                    cy = scr_y + int(oy * scale)
                    r = int(rad * scale)
                    pygame.draw.circle(surface, base_pink, (cx, cy + 2), r)
                # Layer 2: middle blossom bulk
                for ox, oy, rad in puffs:
                    cx = tx + int(ox * scale)
                    cy = scr_y + int(oy * scale)
                    r = int(rad * scale)
                    pygame.draw.circle(surface, mid_pink, (cx, cy), r)
                # Layer 3: highlight sunlit crests
                for ox, oy, rad in puffs:
                    cx = tx + int(ox * scale)
                    cy = scr_y + int((oy - 4) * scale)
                    r = max(2, int((rad - 7) * scale))
                    pygame.draw.circle(surface, high_pink, (cx, cy), r)

        # 5. Slices: Roadway, Asphalt, Sakura Rose Curbs, Markings
        slice_h = 6
        for y in range(0, scr_h, slice_h):
            world_y = self.track_distance + (ply_y - y)
            r_left, r_right = self.get_road_edges(8, world_y)
            r_w = r_right - r_left
            
            # Bronze Mahogany Guard Barrier with Sakura Rose Trim
            pygame.draw.rect(surface, (46, 32, 38), (r_left - 16.0, y, 16, slice_h))
            pygame.draw.rect(surface, (46, 32, 38), (r_right, y, 16, slice_h))
            pygame.draw.rect(surface, (240, 165, 185), (r_left - 16.0, y, 2, slice_h))
            pygame.draw.rect(surface, (240, 165, 185), (r_right + 14.0, y, 2, slice_h))
            
            # Dark Slate Asphalt Road Surface
            pygame.draw.rect(surface, (34, 36, 42), (r_left, y, r_w, slice_h))
            
            # Dashed Lane Dividers (Crisp Snow White)
            lane_w = r_w / 4.0
            dash_cycle = (int(y + self.track_distance)) % 60
            if dash_cycle < 30:
                pygame.draw.rect(surface, (250, 245, 245), (r_left + lane_w - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (250, 245, 245), (r_left + lane_w * 3.0 - 1.5, y, 3, slice_h))
                # Double Golden Honey Center Line
                pygame.draw.rect(surface, (255, 195, 45), (r_left + lane_w * 2.0 - 3.0, y, 2, slice_h))
                pygame.draw.rect(surface, (255, 195, 45), (r_left + lane_w * 2.0 + 1.0, y, 2, slice_h))
                
            # Sakura Rose & Pure Pearl White Alternating Curbs
            curb_cycle = (int(y + self.track_distance) // 18) % 2
            curb_col = (255, 125, 165) if curb_cycle == 0 else (255, 255, 255)
            pygame.draw.rect(surface, curb_col, (r_left - 8, y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (r_right, y, 8, slice_h))
            
            # Soft Rose-Gold Roadside Reflectors every 40m
            if int(world_y) % 40 < 6:
                pygame.draw.rect(surface, (255, 195, 160), (r_left - 12, y + 1, 4, 4))
                pygame.draw.rect(surface, (255, 195, 160), (r_right + 8, y + 1, 4, 4))

        # 6. Dynamic Drifting Sakura Petals (Screen & Road Overlay)
        for petal in self.stage8_petals:
            drift_x = math.sin(petal["phase"] + self.frames * 0.025 * petal["drift_freq"]) * petal["drift_amp"]
            px = GAME_X + (petal["rx"] + drift_x) % GAME_W
            py = (petal["ry"] + self.frames * (petal["speed_y"] / 60.0) + self.track_distance * 0.15) % scr_h
            sz = int(petal["size"])
            pygame.draw.ellipse(surface, petal["color"], (int(px - sz), int(py - sz // 2), sz * 2, max(2, sz)))
            pygame.draw.circle(surface, (255, 240, 245), (int(px), int(py)), max(1, sz // 3))

    def _render_stage9(self, surface: pygame.Surface):
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        
        # 1. Sunset Canyon Dusk Sky (rich crimson-amber twilight base)
        pygame.draw.rect(surface, (54, 22, 26), (GAME_X, 0, GAME_W, scr_h))
        
        # 2. Sandstone Desert Terrain across Entire Viewport
        self.draw_tiled_texture(surface, self.tex_rock_ground, (GAME_X, 0, GAME_W, scr_h))
        
        # Warm sunset amber wash overlay across entire terrain
        sand_overlay = pygame.Surface((int(GAME_W), scr_h), pygame.SRCALPHA)
        sand_overlay.fill((190, 75, 35, 140))
        surface.blit(sand_overlay, (GAME_X, 0))
        
        # 3. Distant Sandstone Mesas & Buttes
        for mesa in self.stage9_mesas:
            mx, my = mesa["pos"]
            mw, mh = mesa["w"], mesa["h"]
            col_idx = mesa["col_idx"]
            scr_y = ply_y - (my - self.track_distance)
            if -80 <= scr_y <= scr_h + 80:
                r_l, r_r = self.get_road_edges(9, my)
                margin = 24.0 + mw * 0.5
                if mx < (r_l + r_r) * 0.5:
                    mx = min(mx, r_l - margin)
                else:
                    mx = max(mx, r_r + margin)
                col_base = (145, 62, 38) if col_idx == 0 else ((160, 68, 42) if col_idx == 1 else (135, 55, 34))
                col_top = (175, 78, 48) if col_idx == 0 else ((190, 85, 52) if col_idx == 1 else (165, 70, 42))
                # 3D Mesa Ground Shadow
                pygame.draw.polygon(surface, (0, 0, 0, 90), [
                    (mx - mw * 0.45, scr_y),
                    (mx + mw * 0.45, scr_y),
                    (mx + mw * 0.55, scr_y + 12),
                    (mx - mw * 0.35, scr_y + 12)
                ])

                # Base mesa slope
                pygame.draw.polygon(surface, col_base, [
                    (mx - mw * 0.5, scr_y),
                    (mx - mw * 0.35, scr_y - mh * 0.5),
                    (mx + mw * 0.35, scr_y - mh * 0.5),
                    (mx + mw * 0.5, scr_y)
                ])
                # Top sheer plateau
                pygame.draw.polygon(surface, col_top, [
                    (mx - mw * 0.35, scr_y - mh * 0.5),
                    (mx - mw * 0.30, scr_y - mh),
                    (mx + mw * 0.30, scr_y - mh),
                    (mx + mw * 0.35, scr_y - mh * 0.5)
                ])
                # Sunlit plateau rim
                pygame.draw.line(surface, (235, 135, 75), (mx - mw * 0.30, scr_y - mh), (mx + mw * 0.30, scr_y - mh), 2)

        # 4. Towering Saguaro Cacti along Roadside with 3D Drop Shadows
        for cactus in self.stage9_cacti:
            cx, cy = cactus["pos"]
            ch = cactus["h"]
            arms = cactus["arms"]
            arm_y = cactus["arm_y"]
            scr_y = ply_y - (cy - self.track_distance)
            if -90 <= scr_y <= scr_h + 90:
                r_l, r_r = self.get_road_edges(9, cy)
                margin = 32.0
                if cx < (r_l + r_r) * 0.5:
                    cx = min(cx, r_l - margin)
                else:
                    cx = max(cx, r_r + margin)
                # 3D Saguaro Cactus Drop Shadow on desert sand
                sh_surf = pygame.Surface((int(ch + 30), int(ch * 0.7)), pygame.SRCALPHA)
                pygame.draw.line(sh_surf, (0, 0, 0, 80), (8, 8), (int(ch * 0.75), int(ch * 0.42)), 6)
                pygame.draw.line(sh_surf, (0, 0, 0, 75), (int(ch * 0.35), int(ch * 0.20)), (int(ch * 0.35) - 6, int(ch * 0.32)), 4)
                if arms >= 2:
                    pygame.draw.line(sh_surf, (0, 0, 0, 75), (int(ch * 0.50), int(ch * 0.28)), (int(ch * 0.50) + 12, int(ch * 0.22)), 4)
                pygame.draw.ellipse(sh_surf, (0, 0, 0, 125), (0, 2, 16, 10))
                surface.blit(sh_surf, (cx - 6, scr_y - 6))

                # Main trunk
                pygame.draw.rect(surface, (36, 78, 45), (cx - 5, scr_y - ch, 10, ch), border_radius=4)
                pygame.draw.line(surface, (55, 110, 65), (cx - 1, scr_y - ch + 2), (cx - 1, scr_y - 2), 2)
                # Left branching arm
                ay1 = int(scr_y - ch * arm_y)
                ay2 = int(scr_y - ch * (arm_y + 0.32))
                pygame.draw.lines(surface, (36, 78, 45), False, [(cx - 4, ay1), (cx - 16, ay1), (cx - 16, ay2)], 5)
                pygame.draw.circle(surface, (36, 78, 45), (int(cx - 16), int(ay2)), 3)
                # Right branching arm
                if arms >= 2:
                    ry1 = int(scr_y - ch * (arm_y + 0.12))
                    ry2 = int(scr_y - ch * (arm_y + 0.44))
                    pygame.draw.lines(surface, (36, 78, 45), False, [(cx + 4, ry1), (cx + 16, ry1), (cx + 16, ry2)], 5)
                    pygame.draw.circle(surface, (36, 78, 45), (int(cx + 16), int(ry2)), 3)

        # 5. Slices: Roadway, Asphalt, Sunset Curbs, Road Markings
        slice_h = 6
        for y in range(0, scr_h, slice_h):
            world_y = self.track_distance + (ply_y - y)
            r_left, r_right = self.get_road_edges(9, world_y)
            r_w = r_right - r_left
            
            # Heavy Canyon Steel Guard Barrier (Dark bronze with amber trim)
            pygame.draw.rect(surface, (55, 34, 30), (r_left - 16.0, y, 16, slice_h))
            pygame.draw.rect(surface, (55, 34, 30), (r_right, y, 16, slice_h))
            pygame.draw.rect(surface, (255, 165, 45), (r_left - 16.0, y, 2, slice_h))
            pygame.draw.rect(surface, (255, 165, 45), (r_right + 14.0, y, 2, slice_h))
            
            # Sun-Baked Sandstone Slate Asphalt
            pygame.draw.rect(surface, (38, 35, 38), (r_left, y, r_w, slice_h))
            
            # Dashed Lane Dividers (Sun-Bleached White)
            lane_w = r_w / 4.0
            dash_cycle = (int(y + self.track_distance)) % 60
            if dash_cycle < 30:
                pygame.draw.rect(surface, (245, 235, 220), (r_left + lane_w - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (245, 235, 220), (r_left + lane_w * 3.0 - 1.5, y, 3, slice_h))
                # Double Sunset Sunburst Center Line
                pygame.draw.rect(surface, (255, 170, 30), (r_left + lane_w * 2.0 - 3.0, y, 2, slice_h))
                pygame.draw.rect(surface, (255, 170, 30), (r_left + lane_w * 2.0 + 1.0, y, 2, slice_h))
                
            # Curbs: Alternating Sunset Amber and Obsidian Dark
            curb_cycle = (int(y + self.track_distance) // 18) % 2
            curb_col = (255, 140, 25) if curb_cycle == 0 else (28, 22, 26)
            pygame.draw.rect(surface, curb_col, (r_left - 8, y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (r_right, y, 8, slice_h))
            
            # Soft Sunset Golden Reflectors every 40m
            if int(world_y) % 40 < 6:
                pygame.draw.rect(surface, (255, 205, 75), (r_left - 12, y + 1, 4, 4))
                pygame.draw.rect(surface, (255, 205, 75), (r_right + 8, y + 1, 4, 4))

        # 6. Dynamic Rolling Tumbleweeds (Drifting across desert road)
        for tw in self.stage9_tumbleweeds:
            px = GAME_X + (tw["rx"] + self.frames * (tw["speed_x"] / 60.0)) % GAME_W
            py = (tw["ry"] + self.frames * (tw["speed_y"] / 60.0) + self.track_distance * 0.15) % scr_h
            rad = tw["rad"]
            rot = tw["rot"] + self.frames * 0.05
            # Tumbleweed shadow
            pygame.draw.ellipse(surface, (0, 0, 0, 70), (int(px - rad * 0.8), int(py + rad * 0.7), int(rad * 1.6), int(rad * 0.7)))
            # Tumbleweed branches
            pygame.draw.circle(surface, (175, 130, 85), (int(px), int(py)), int(rad))
            pygame.draw.circle(surface, (150, 110, 70), (int(px), int(py)), int(rad * 0.75), 2)
            pygame.draw.line(surface, (135, 95, 60), (px - rad * 0.7, py), (px + rad * 0.7, py), 2)
            pygame.draw.line(surface, (135, 95, 60), (px, py - rad * 0.7), (px, py + rad * 0.7), 2)

    def _render_stage10(self, surface: pygame.Surface):
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        import time
        now = time.time()
        
        # 1. Dark Championship Circuit Base
        pygame.draw.rect(surface, (18, 24, 32), (GAME_X, 0, GAME_W, scr_h))
        
        # 2. Championship Manicured Racing Turf across Entire Viewport
        self.draw_tiled_texture(surface, self.tex_grass, (GAME_X, 0, GAME_W, scr_h))
        
        # Manicured emerald race verge overlay across entire terrain
        turf_overlay = pygame.Surface((int(GAME_W), scr_h), pygame.SRCALPHA)
        turf_overlay.fill((20, 75, 35, 75))
        surface.blit(turf_overlay, (GAME_X, 0))

        # 3. Circuit Grandstands & Cheering Spectators
        for stand in self.stage10_grandstands:
            gx, gy = stand["pos"]
            gw, gh = stand["w"], stand["h"]
            b_col = stand["banner_col"]
            scr_y = ply_y - (gy - self.track_distance)
            if -80 <= scr_y <= scr_h + 80:
                r_l, r_r = self.get_road_edges(10, gy)
                margin = 24.0 + gw * 0.5
                if gx < (r_l + r_r) * 0.5:
                    gx = min(gx, r_l - margin)
                else:
                    gx = max(gx, r_r + margin)
                # 3D Grandstand Ground Shadow on turf
                pygame.draw.ellipse(surface, (0, 0, 0, 110), (int(gx - gw * 0.45), int(scr_y - 4), int(gw * 0.9), 12))
                pygame.draw.polygon(surface, (0, 0, 0, 75), [
                    (gx - gw * 0.45, scr_y),
                    (gx + gw * 0.45, scr_y),
                    (gx + gw * 0.55, scr_y + 14),
                    (gx - gw * 0.35, scr_y + 14)
                ])

                # Canopy roof
                pygame.draw.rect(surface, (45, 52, 68), (gx - gw * 0.5, scr_y - gh, gw, 10), border_radius=3)
                # Tiers with crowd colors
                pygame.draw.rect(surface, (30, 36, 50), (gx - gw * 0.45, scr_y - gh + 10, gw * 0.9, gh - 18))
                for cr in range(4):
                    for cc in range(6):
                        c_dot_col = (240, 200, 180) if (cr + cc) % 2 == 0 else (220, 60, 60)
                        pygame.draw.circle(surface, c_dot_col, (int(gx - gw * 0.4 + cc * 10), int(scr_y - gh + 14 + cr * 6)), 2)
                # Championship Banner along front
                pygame.draw.rect(surface, b_col, (gx - gw * 0.48, scr_y - 8, gw * 0.96, 8), border_radius=2)

        # 4. Animated Celebration Searchlights
        for light in self.stage10_searchlights:
            sx, sy = light["pos"]
            ph = light["phase"]
            spd = light["sweep_speed"]
            scr_y = ply_y - (sy - self.track_distance)
            if -100 <= scr_y <= scr_h + 100:
                r_l, r_r = self.get_road_edges(10, sy)
                margin = 26.0
                if sx < (r_l + r_r) * 0.5:
                    sx = min(sx, r_l - margin)
                else:
                    sx = max(sx, r_r + margin)
                # 3D Searchlight Base Drop Shadow
                pygame.draw.ellipse(surface, (0, 0, 0, 120), (int(sx - 10), int(scr_y - 4), 20, 10))
                # Searchlight base unit
                pygame.draw.rect(surface, (70, 75, 90), (sx - 8, scr_y - 12, 16, 12), border_radius=2)
                pygame.draw.circle(surface, (255, 255, 220), (int(sx), int(scr_y - 12)), 5)
                # Sweeping radiant beam
                sweep_ang = math.sin(now * spd + ph) * 0.5
                beam_dx = math.sin(sweep_ang) * 220
                pygame.draw.line(surface, (255, 245, 200), (sx, scr_y - 12), (sx + beam_dx, scr_y - 200), 3)

        # 5. Slices: Circuit Asphalt, Championship Gold & Crimson Curbs, Markings
        slice_h = 6
        for y in range(0, scr_h, slice_h):
            world_y = self.track_distance + (ply_y - y)
            r_left, r_right = self.get_road_edges(10, world_y)
            r_w = r_right - r_left
            
            # Championship Safety Armco Barrier (Carbon Grey with Victory Gold Rail)
            pygame.draw.rect(surface, (38, 42, 52), (r_left - 16.0, y, 16, slice_h))
            pygame.draw.rect(surface, (38, 42, 52), (r_right, y, 16, slice_h))
            pygame.draw.rect(surface, (255, 215, 0), (r_left - 16.0, y, 2, slice_h))
            pygame.draw.rect(surface, (255, 215, 0), (r_right + 14.0, y, 2, slice_h))
            
            # Formula-Grade Race Asphalt Surface
            pygame.draw.rect(surface, (26, 28, 34), (r_left, y, r_w, slice_h))
            
            # Dashed Lane Dividers (Crisp Track White)
            lane_w = r_w / 4.0
            dash_cycle = (int(y + self.track_distance)) % 60
            if dash_cycle < 30:
                pygame.draw.rect(surface, (250, 250, 250), (r_left + lane_w - 1.5, y, 3, slice_h))
                pygame.draw.rect(surface, (250, 250, 250), (r_left + lane_w * 3.0 - 1.5, y, 3, slice_h))
                # Double Grand Championship Gold & Cyan Center Line
                pygame.draw.rect(surface, (255, 215, 0), (r_left + lane_w * 2.0 - 3.0, y, 2, slice_h))
                pygame.draw.rect(surface, (0, 220, 255), (r_left + lane_w * 2.0 + 1.0, y, 2, slice_h))
                
            # Curbs: Alternating Championship Gold and Victory Crimson
            curb_cycle = (int(y + self.track_distance) // 18) % 2
            curb_col = (255, 215, 0) if curb_cycle == 0 else (225, 35, 35)
            pygame.draw.rect(surface, curb_col, (r_left - 8, y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (r_right, y, 8, slice_h))
            
            # High-Luminance Diamond Apex Beacons every 40m
            if int(world_y) % 40 < 6:
                pygame.draw.rect(surface, (180, 240, 255), (r_left - 12, y + 1, 4, 4))
                pygame.draw.rect(surface, (180, 240, 255), (r_right + 8, y + 1, 4, 4))

    def _render_stage11(self, surface: pygame.Surface):
        """Stage 11: Rainbow Skyway - Secret All-46 Hiragana Mastery Bonus Stage."""
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        slice_h = 6
        import time
        now = time.time()

        # 1. Cosmic Aurora & Celestial Void Background
        pygame.draw.rect(surface, (12, 10, 26), (GAME_X, 0, GAME_W, scr_h))
        
        # Cosmic Aurora ribbons in the upper sky
        aurora_h = int(scr_h * 0.45)
        for ay in range(0, aurora_h, 8):
            t_a = ay / aurora_h
            a_surf = pygame.Surface((int(GAME_W), 8), pygame.SRCALPHA)
            r = int(60 + 120 * (0.5 + 0.5 * math.sin(now + ay * 0.03)))
            g = int(30 + 80 * (0.5 + 0.5 * math.cos(now * 0.8 + ay * 0.02)))
            b = int(140 + 90 * (0.5 + 0.5 * math.sin(now * 1.2 + ay * 0.04)))
            alpha = int(75 * (1.0 - t_a))
            pygame.draw.rect(a_surf, (r, g, b, alpha), (0, 0, int(GAME_W), 8))
            surface.blit(a_surf, (GAME_X, ay))

        # Twinkling Cosmic Stars
        for st in self.stage11_stars:
            twinkle = 0.5 + 0.5 * math.sin(now * st["speed"] + st["phase"])
            sx = int(st["x"])
            sy = int((st["y"] + self.track_distance * 0.05) % scr_h)
            scol = tuple(int(c * twinkle) for c in st["color"])
            pygame.draw.circle(surface, scol, (sx, sy), int(st["r"]))

        # 2. Road Slices & Pulsing RGB Rainbow Curbs
        road_left_base = GAME_X + ROAD_MARGIN
        road_w_base = GAME_W - (ROAD_MARGIN * 2.0)
        lane_w = road_w_base / 4.0

        for y in range(0, scr_h, slice_h):
            world_y = self.track_distance + (ply_y - y)
            r_left, r_right = self.get_road_edges(11, world_y)
            r_w = r_right - r_left

            # Verges: Dark cosmic twilight shoulders
            verge_l_w = r_left - GAME_X
            verge_r_w = (GAME_X + GAME_W) - r_right
            if verge_l_w > 0:
                pygame.draw.rect(surface, (16, 14, 34), (GAME_X, y, int(verge_l_w), slice_h))
            if verge_r_w > 0:
                pygame.draw.rect(surface, (16, 14, 34), (int(r_right), y, int(verge_r_w), slice_h))

            # Road Surface: Sleek midnight cosmic asphalt
            pygame.draw.rect(surface, (22, 24, 36), (int(r_left), y, int(r_w), slice_h))

            # Pulsing RGB Rainbow Curbs (smooth hue rotation along distance & time)
            hue = int((world_y * 0.15 + now * 140.0)) % 360
            rb_color = pygame.Color(0)
            rb_color.hsva = (hue, 85, 100, 100)
            curb_col = (rb_color.r, rb_color.g, rb_color.b)

            pygame.draw.rect(surface, curb_col, (int(r_left - 8), y, 8, slice_h))
            pygame.draw.rect(surface, curb_col, (int(r_right), y, 8, slice_h))

            # Glowing Neon Lane Dividers
            dash_cycle = (int(y + self.track_distance)) % 60
            if dash_cycle < 30:
                # Outer dividers: Neon Cyan
                pygame.draw.rect(surface, (0, 225, 255), (int(r_left + lane_w - 1.5), y, 3, slice_h))
                pygame.draw.rect(surface, (0, 225, 255), (int(r_left + lane_w * 3.0 - 1.5), y, 3, slice_h))
                # Center divider: Glowing Electric Gold
                pygame.draw.rect(surface, (255, 220, 40), (int(r_left + lane_w * 2.0 - 2.0), y, 4, slice_h))

        # 3. Glowing Prismatic Crystals along Roadside with 3D Drop Shadows
        for cry in self.stage11_crystals:
            cx, cy = cry["pos"]
            ccol = cry["color"]
            scr_y = ply_y - (cy - self.track_distance)
            if -80 <= scr_y <= scr_h + 80:
                r_l, r_r = self.get_road_edges(11, cy)
                margin = 24.0
                if cx < (r_l + r_r) * 0.5:
                    cx = min(cx, r_l - margin)
                else:
                    cx = max(cx, r_r + margin)
                # 3D Drop shadow offset (+12, +8) down-right
                pygame.draw.ellipse(surface, (0, 0, 0, 120), (int(cx - 10 + 10), int(scr_y - 4 + 8), 24, 12))
                pygame.draw.ellipse(surface, (0, 0, 0, 140), (int(cx - 12), int(scr_y - 4), 24, 10))
                # Diamond / Prismatic Crystal
                cw = 18
                ch = 44
                pts_cry = [
                    (int(cx), int(scr_y - ch)),
                    (int(cx + cw * 0.5), int(scr_y - ch * 0.45)),
                    (int(cx), int(scr_y)),
                    (int(cx - cw * 0.5), int(scr_y - ch * 0.45))
                ]
                pygame.draw.polygon(surface, ccol, pts_cry)
                pts_facet = [
                    (int(cx), int(scr_y - ch)),
                    (int(cx), int(scr_y)),
                    (int(cx - cw * 0.5), int(scr_y - ch * 0.45))
                ]
                highlight = tuple(min(255, int(c * 1.35)) for c in ccol)
                pygame.draw.polygon(surface, highlight, pts_facet)
                pygame.draw.polygon(surface, (255, 255, 255), pts_cry, 1)

        # 4. Floating Cyber-Torii Arches Spanning the Road
        for tor in self.stage11_torii:
            ty = tor["y"]
            tcol = tor["color"]
            scr_y = ply_y - (ty - self.track_distance)
            if -120 <= scr_y <= scr_h + 120:
                r_l, r_r = self.get_road_edges(11, ty)
                arch_w = (r_r - r_l) + 60.0
                ax = (r_l + r_r) * 0.5
                arch_h = 75.0
                # Pillar 3D shadows at bases
                pygame.draw.ellipse(surface, (0, 0, 0, 140), (int(r_l - 30 + 10), int(scr_y - 4 + 8), 24, 12))
                pygame.draw.ellipse(surface, (0, 0, 0, 140), (int(r_r + 6 + 10), int(scr_y - 4 + 8), 24, 12))
                # Pillars
                pygame.draw.rect(surface, tcol, (int(r_l - 26), int(scr_y - arch_h), 14, int(arch_h)), border_radius=2)
                pygame.draw.rect(surface, tcol, (int(r_r + 12), int(scr_y - arch_h), 14, int(arch_h)), border_radius=2)
                # Main curved crossbeam (Kasagi)
                pygame.draw.rect(surface, tcol, (int(ax - arch_w * 0.55), int(scr_y - arch_h - 10), int(arch_w * 1.1), 12), border_radius=4)
                pygame.draw.rect(surface, (255, 255, 255), (int(ax - arch_w * 0.55), int(scr_y - arch_h - 10), int(arch_w * 1.1), 12), 1, border_radius=4)
                # Secondary crossbeam (Nuki)
                pygame.draw.rect(surface, tcol, (int(ax - arch_w * 0.5), int(scr_y - arch_h + 12), int(arch_w), 8), border_radius=2)

        # 5. Holographic Gantries with Japanese / Romanji Mastery Text
        for gan in self.stage11_gantries:
            gy = gan["y"]
            msg = gan["text"]
            scr_y = ply_y - (gy - self.track_distance)
            if -100 <= scr_y <= scr_h + 100:
                r_l, r_r = self.get_road_edges(11, gy)
                gw = (r_r - r_l) + 40.0
                gx = (r_l + r_r) * 0.5
                gh = 55.0
                # 3D Gantry pillar drop shadows
                pygame.draw.ellipse(surface, (0, 0, 0, 130), (int(r_l - 24 + 10), int(scr_y - 4 + 8), 22, 10))
                pygame.draw.ellipse(surface, (0, 0, 0, 130), (int(r_r + 2 + 10), int(scr_y - 4 + 8), 22, 10))
                # Posts
                pygame.draw.rect(surface, (40, 50, 70), (int(r_l - 20), int(scr_y - gh), 10, int(gh)))
                pygame.draw.rect(surface, (40, 50, 70), (int(r_r + 10), int(scr_y - gh), 10, int(gh)))
                # Holographic signboard
                board_rect = pygame.Rect(int(gx - gw * 0.5), int(scr_y - gh - 8), int(gw), 36)
                pygame.draw.rect(surface, (10, 18, 32), board_rect, border_radius=4)
                pygame.draw.rect(surface, (0, 220, 255), board_rect, 2, border_radius=4)
                if self.font_gantry:
                    txt = self.font_gantry.render(msg, True, (255, 230, 80))
                    surface.blit(txt, txt.get_rect(center=board_rect.center))

    def _render_finish_line(self, surface: pygame.Surface):
        scr_h = self.screen_height
        ply_y = self.player_screen_y
        remaining = STAGE_TRACK_LENGTH - self.track_distance
        finish_y = ply_y - remaining
        if -80.0 <= finish_y <= scr_h + 80.0:
            r_left, r_right = self.get_road_edges(self.current_stage, STAGE_TRACK_LENGTH)
            r_w = r_right - r_left
            
            # Checkered Banner
            if self.tex_finish_banner:
                surface.blit(pygame.transform.scale(self.tex_finish_banner, (int(r_w), 40)), (r_left, finish_y - 20))
                
            # Goal Posts
            post_l = r_left - 18.0
            post_r = r_right + 2.0
            for side_x in [post_l, post_r]:
                for pr in range(4):
                    col = (230, 38, 38) if pr % 2 == 0 else (242, 242, 242)
                    pygame.draw.rect(surface, col, (side_x, finish_y - 16 + pr * 12, 16, 12))
                    pygame.draw.rect(surface, (0, 0, 0), (side_x, finish_y - 16 + pr * 12, 16, 12), 1)
