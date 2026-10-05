"""
hiragana_extras.py
Arcade Racer gameplay & graphics extras (Road Fighter style) for Hiragana & Katakana:
  * Road hazards (oil slicks, traffic cones) with advance warning
  * Rival personalities (cruiser / weaver / speedster / truck)
  * Slipstream drafting, near-miss bonus, match combo multiplier
  * Pooled particles, speed lines, screen shake, floating text, HUD chips

Active for both Hiragana and Katakana Arcade racers.
"""

import math
import random
import pygame

from game_config import (
    GAME_X, GAME_W, STAGE_TRACK_LENGTH, SCORE_REWARD, MAX_FUEL
)
from entities import TrafficCar, get_latin_font

OIL_SLIP_TIME = 1.2
DRAFT_BOOST = 1.10        # track speed multiplier while slipstreaming
MAX_PARTICLES = 120

BEHAVIOR_BADGE = {
    "weaver": (0, 215, 255),
    "speedster": (255, 130, 25),
    "truck": (170, 175, 185),
}


def lanes_for_width(road_w: float) -> list[int]:
    """Same lane availability rule the traffic spawner uses."""
    if road_w < 400.0:
        return [1, 2]
    if road_w < 560.0:
        return [0, 1, 2]
    return [0, 1, 2, 3]


class Hazard:
    def __init__(self, kind: str, world_y: float, lane_idx: int):
        self.kind = kind            # "oil" or "cone"
        self.world_y = world_y
        self.lane_idx = lane_idx
        self.x = 0.0
        self.y = -1000.0
        self.hit = False
        self.to_remove = False

    def hitbox(self) -> pygame.Rect:
        if self.kind == "oil":
            return pygame.Rect(self.x - 38, self.y - 17, 76, 34)
        return pygame.Rect(self.x - 13, self.y - 13, 26, 26)


class HiraganaExtras:
    def __init__(self):
        self._build_sprites()
        self._speed_lines = []
        rng = random.Random(7)
        for i in range(28):
            left = (i % 2 == 0)
            off = rng.uniform(6, 95)
            self._speed_lines.append({
                "dx": off if left else GAME_W - off,
                "y": rng.uniform(0, 1200),
                "k": rng.uniform(0.7, 1.4),
            })
        self._text_cache = {}
        self.reset(1)

    # ------------------------------------------------------------------ setup
    def _build_sprites(self):
        # Oil slick: dark glossy puddle with a purple/teal rainbow sheen
        oil = pygame.Surface((96, 56), pygame.SRCALPHA)
        pygame.draw.ellipse(oil, (10, 10, 16, 225), (4, 6, 88, 44))
        pygame.draw.ellipse(oil, (24, 22, 38, 235), (10, 10, 70, 34))
        pygame.draw.ellipse(oil, (60, 40, 105, 200), (20, 14, 40, 18))
        pygame.draw.ellipse(oil, (30, 120, 130, 170), (34, 20, 30, 12))
        pygame.draw.arc(oil, (200, 170, 255, 210), (16, 12, 56, 28), 3.5, 5.4, 2)
        pygame.draw.ellipse(oil, (10, 10, 16, 200), (62, 30, 22, 14))
        self.spr_oil = oil

        # Traffic cone seen from above: square base, orange rings, white band
        cone = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.rect(cone, (30, 30, 30, 255), (4, 4, 32, 32), border_radius=4)
        pygame.draw.circle(cone, (255, 110, 15), (20, 20), 14)
        pygame.draw.circle(cone, (250, 250, 250), (20, 20), 10)
        pygame.draw.circle(cone, (255, 110, 15), (20, 20), 6)
        pygame.draw.circle(cone, (255, 190, 90), (18, 18), 2)
        self.spr_cone = cone

        # Warning triangle shown while a hazard is still off-screen ahead
        warn = pygame.Surface((46, 42), pygame.SRCALPHA)
        pygame.draw.polygon(warn, (255, 205, 20), [(23, 2), (44, 39), (2, 39)])
        pygame.draw.polygon(warn, (20, 20, 25), [(23, 2), (44, 39), (2, 39)], 3)
        pygame.draw.rect(warn, (20, 20, 25), (21, 14, 4, 14))
        pygame.draw.rect(warn, (20, 20, 25), (21, 31, 4, 4))
        self.spr_warn = warn

    def reset(self, stage: int):
        self.stage = stage
        self.hazards: list[Hazard] = []
        self.hazard_timer = -4.0
        self.particles: list[list] = []
        self.floaters: list[list] = []
        self.combo = 0
        self.best_combo = 0
        self.near_misses = 0
        self.slip_timer = 0.0
        self.slip_dir = 1.0
        self.heat = 0.0
        self.overheated = False
        self.drafting = False
        self.draft_mult = 1.0
        self.shake_timer = 0.0
        self.shake_amp = 0.0
        self.scroll = 0.0
        self.t = 0.0

    @staticmethod
    def active(engine) -> bool:
        return engine.game_mode in ("hiragana", "katakana")

    # ------------------------------------------------------- rival behaviours
    def assign_behavior(self, engine, car: TrafficCar):
        if not self.active(engine) or engine.current_stage >= 11:
            return
        st = engine.current_stage
        weaver_p = min(0.40, 0.04 + 0.04 * st)
        speed_p = 0.0 if st < 3 else 0.10
        truck_p = 0.0 if st < 2 else 0.10
        r = random.random()
        if r < weaver_p:
            car.set_behavior("weaver")
        elif r < weaver_p + speed_p:
            car.set_behavior("speedster")
            car.speed_kmh = random.uniform(150.0, 172.0)
        elif r < weaver_p + speed_p + truck_p:
            car.set_behavior("truck")
            car.speed_kmh = random.uniform(50.0, 68.0)

    def lanes_blocked(self, engine, world_y: float) -> set:
        if not self.active(engine):
            return set()
        return {h.lane_idx for h in self.hazards if abs(h.world_y - world_y) < 240.0}

    # ----------------------------------------------------------- input hooks
    def modify_steer(self, engine, steer: float, delta: float) -> float:
        if not self.active(engine):
            return steer
        if self.slip_timer > 0.0:
            self.slip_timer = max(0.0, self.slip_timer - delta)
            k = self.slip_timer / OIL_SLIP_TIME
            return max(-1.0, min(1.0, steer * 0.35 + self.slip_dir * 0.65 * k))
        return steer

    def gate_turbo(self, engine, turbo_down: bool, delta: float) -> bool:
        return turbo_down

    def track_multiplier(self, engine) -> float:
        return self.draft_mult if self.active(engine) else 1.0

    # ------------------------------------------------------- match / crash
    def on_match(self, engine, car):
        if not self.active(engine):
            return
        self.combo += 1
        self.best_combo = max(self.best_combo, self.combo)
        mult = min(4, 1 + self.combo // 2)
        if mult > 1:
            engine.score += SCORE_REWARD * (mult - 1)
        if mult >= 4:
            engine.fuel = min(MAX_FUEL, engine.fuel + 5.0)
        label = f"+{int(SCORE_REWARD * mult)}"
        if mult > 1:
            label += f"  x{mult} COMBO"
        self._float(car.x, car.y - 40, label, (255, 225, 60))
        self._burst(car.x, car.y, 26, [(255, 225, 60), (255, 255, 255), (120, 255, 190)], 260.0, 0.6, 5, 0.1)

    def on_crash(self, engine, car):
        if not self.active(engine):
            return
        if self.combo >= 2:
            self._float(engine.player.x, engine.player.y - 90, "COMBO LOST", (255, 90, 70))
        self.combo = 0
        self.shake_timer = 0.35
        self.shake_amp = 7.0
        mx = (engine.player.x + car.x) * 0.5
        my = (engine.player.y + car.y) * 0.5
        self._burst(mx, my, 24, [(255, 150, 30), (255, 245, 200), (90, 90, 95)], 300.0, 0.6, 5, 0.2)

    # ---------------------------------------------------------------- update
    def update(self, engine, delta: float, dist_step: float):
        if not self.active(engine):
            return
        self.t += delta
        self.scroll = dist_step
        p = engine.player
        screen_h = engine.virtual_height

        if self.shake_timer > 0.0:
            self.shake_timer = max(0.0, self.shake_timer - delta)

        self._update_hazards(engine, delta, screen_h)
        self._update_weavers(engine, delta, screen_h)
        self._update_draft_and_near_miss(engine)
        self._emit_player_fx(engine, delta)
        self._update_particles(delta)
        for f in self.floaters:
            f[2] -= 46.0 * delta
            f[3] -= delta
        self.floaters = [f for f in self.floaters if f[3] > 0.0]

    def _lane_x(self, engine, lane_idx: int, world_y: float) -> float:
        r_left, r_right = engine.road.get_road_edges(engine.current_stage, world_y)
        margin = TrafficCar.WIDTH * 0.5 + 8.0
        avail = max(TrafficCar.WIDTH, (r_right - r_left) - margin * 2.0)
        return r_left + margin + TrafficCar.LANE_FRACTIONS[lane_idx] * avail

    def _update_hazards(self, engine, delta: float, screen_h: float):
        st = engine.current_stage
        # Spawn
        if st < 11 and engine.track_distance < STAGE_TRACK_LENGTH - 1800.0 and len(self.hazards) < 3:
            self.hazard_timer += delta
            interval = max(5.0, 14.0 - st * 0.9)
            if self.hazard_timer >= interval:
                self.hazard_timer = interval - 1.0  # retry soon if blocked
                self._try_spawn_hazard(engine)

        p = engine.player
        pbox = p.get_hitbox()
        for hz in self.hazards:
            hz.y = engine.player_screen_y - (hz.world_y - engine.track_distance)
            hz.x = self._lane_x(engine, hz.lane_idx, hz.world_y)
            if hz.y > screen_h + 120.0:
                hz.to_remove = True
            if hz.hit:
                continue
            if pbox.colliderect(hz.hitbox()):
                hz.hit = True
                if hz.kind == "oil":
                    self.slip_timer = OIL_SLIP_TIME
                    self.slip_dir = random.choice((-1.0, 1.0))
                    self._float(p.x, p.y - 90, "SLIP!", (190, 150, 255))
                    self._burst(p.x, p.y + 50, 12, [(200, 200, 210), (140, 140, 150)], 110.0, 0.7, 9, 0.9)
                else:
                    hz.to_remove = True
                    p.speed_kmh = max(40.0, p.speed_kmh * 0.82)
                    p.wobble_timer = max(p.wobble_timer, 0.3)
                    engine.fuel = max(0.0, engine.fuel - 5.0)
                    engine.audio.play_crash()
                    self.shake_timer = max(self.shake_timer, 0.2)
                    self.shake_amp = max(self.shake_amp, 4.0)
                    self._float(p.x, p.y - 90, "-5 FUEL", (255, 120, 60))
                    self._burst(hz.x, hz.y, 16, [(255, 120, 20), (255, 255, 255)], 240.0, 0.6, 5, 0.2)
        self.hazards = [h for h in self.hazards if not h.to_remove]

    def _try_spawn_hazard(self, engine):
        st = engine.current_stage
        world_y = engine.track_distance + 1500.0
        edges = engine.road.get_road_edges(st, world_y)
        lanes = lanes_for_width(edges[1] - edges[0])
        for car in engine.traffic_cars:
            if car.is_active and abs(car.world_y - world_y) < 320.0 and car.lane_idx in lanes:
                lanes = [l for l in lanes if l != car.lane_idx]
        for h in self.hazards:
            if abs(h.world_y - world_y) < 500.0:
                lanes = [l for l in lanes if l != h.lane_idx]
        if not lanes:
            return
        kind = "oil" if (st < 3 or random.random() > 0.45) else "cone"
        self.hazards.append(Hazard(kind, world_y, random.choice(lanes)))
        self.hazard_timer = random.uniform(-2.0, 1.5)

    def _update_weavers(self, engine, delta: float, screen_h: float):
        p = engine.player
        for car in engine.traffic_cars:
            if car.behavior != "weaver" or not car.is_active:
                continue
            car.weave_timer -= delta
            if car.weave_timer > 0.0 or car.lane_change_timer > 0.0:
                continue
            # Only swerve when not right in the player's face
            if not (car.y < p.y - 380.0 or car.y > p.y + 150.0) or car.y < -100.0:
                continue
            car.weave_timer = random.uniform(2.2, 4.2)
            edges = engine.road.get_road_edges(engine.current_stage, car.world_y)
            max_lane = max(lanes_for_width(edges[1] - edges[0]))
            min_lane = min(lanes_for_width(edges[1] - edges[0]))
            options = [l for l in (car.lane_idx - 1, car.lane_idx + 1) if min_lane <= l <= max_lane]
            free = []
            for opt in options:
                ok = True
                for other in engine.traffic_cars:
                    if other is car or not other.is_active:
                        continue
                    if abs(other.world_y - car.world_y) < 260.0 and other.lane_idx == opt:
                        ok = False
                        break
                if ok:
                    free.append(opt)
            if free:
                car.attempt_lane_change(random.choice(free))

    def _update_draft_and_near_miss(self, engine):
        p = engine.player
        pbox = p.get_hitbox()
        drafting = False
        for car in engine.traffic_cars:
            if not car.is_active:
                continue
            # Slipstream: directly behind (below) a car, close but not touching
            gap = p.y - car.y
            if 40.0 < gap < 300.0 and abs(car.x - p.x) < 44.0 and p.speed_kmh > 120.0:
                drafting = True
            # Near miss: just passed a car with a thin sideways gap, no contact
            if not car.near_missed and car.y > p.y - 10.0:
                cbox = car.get_hitbox()
                if (not pbox.colliderect(cbox)) and pbox.inflate(24, -10).colliderect(cbox):
                    car.near_missed = True
                    self.near_misses += 1
                    engine.score += 10.0
                    self._float(p.x, p.y - 110, "NEAR MISS +10", (110, 235, 255))
                    side = 1.0 if car.x > p.x else -1.0
                    self._burst(p.x + side * 44, p.y, 8, [(255, 255, 255), (110, 235, 255)], 180.0, 0.35, 3, 0.3)
        self.drafting = drafting
        self.draft_mult = DRAFT_BOOST if drafting else 1.0

    # ------------------------------------------------------------- particles
    def _burst(self, x, y, n, colors, speed, life, size, ground):
        for _ in range(n):
            if len(self.particles) >= MAX_PARTICLES:
                return
            a = random.uniform(0, math.tau)
            s = random.uniform(0.25, 1.0) * speed
            self.particles.append([x, y, math.cos(a) * s, math.sin(a) * s,
                                   random.uniform(0.6, 1.0) * life, life,
                                   random.uniform(0.6, 1.0) * size, random.choice(colors), ground])

    def _puff(self, x, y, vx, vy, life, size, color, ground):
        if len(self.particles) < MAX_PARTICLES:
            self.particles.append([x, y, vx, vy, life, life, size, color, ground])

    def _emit_player_fx(self, engine, delta: float):
        p = engine.player
        rear_y = p.y + p.HEIGHT * 0.5 - 4
        if p.is_braking and p.speed_kmh > 70.0 and random.random() < 0.7:
            for sx in (-30, 30):
                self._puff(p.x + sx, rear_y, random.uniform(-14, 14), random.uniform(10, 40),
                           0.55, random.uniform(7, 12), (205, 205, 212), 0.9)
        if p.is_turbo and p.speed_kmh > 110.0:
            for sx in (-11, 11):
                self._puff(p.x + sx, rear_y + 6, random.uniform(-25, 25), random.uniform(90, 170),
                           0.28, random.uniform(3, 5), random.choice([(255, 190, 40), (255, 120, 20), (0, 220, 255)]), 0.2)
        if (self.slip_timer > 0.0 or p.wobble_timer > 0.0) and random.random() < 0.6:
            for sx in (-30, 30):
                self._puff(p.x + sx, rear_y, random.uniform(-30, 30), random.uniform(5, 40),
                           0.6, random.uniform(8, 13), (190, 190, 198), 0.9)
        if self.drafting and random.random() < 0.5:
            self._puff(p.x + random.uniform(-30, 30), p.y - p.HEIGHT * 0.5, random.uniform(-10, 10),
                       random.uniform(180, 260), 0.3, 3, (180, 235, 255), 0.0)

    def _update_particles(self, delta: float):
        alive = []
        for pt in self.particles:
            pt[4] -= delta
            if pt[4] <= 0.0:
                continue
            pt[0] += pt[2] * delta
            pt[1] += pt[3] * delta + self.scroll * pt[8]
            pt[2] *= 0.96
            pt[3] *= 0.96
            alive.append(pt)
        self.particles = alive

    def _float(self, x, y, text, color):
        if len(self.floaters) < 8:
            self.floaters.append([x, y, y, 1.1, text, color])

    # ---------------------------------------------------------------- render
    def render_back(self, engine, surface: pygame.Surface):
        """Speed lines + road hazards (drawn under the cars)."""
        if not self.active(engine):
            return
        screen_h = engine.virtual_height
        p = engine.player
        inten = max(0.0, min(1.0, (p.speed_kmh - 185.0) / 80.0))
        if inten > 0.02:
            shade = int(120 + 90 * inten)
            col = (shade, shade + 6, shade + 22)
            ln = int(34 + 70 * inten)
            for sl in self._speed_lines:
                sl["y"] = (sl["y"] + self.scroll * 1.7 * sl["k"]) % (screen_h + 120)
                x = int(GAME_X + sl["dx"])
                y = int(sl["y"]) - 60
                pygame.draw.line(surface, col, (x, y), (x, y + ln), 2)

        for hz in self.hazards:
            if hz.hit and hz.kind == "cone":
                continue
            if hz.y < -10.0:
                # Advance warning pinned to the top edge of the road
                if hz.y > -520.0:
                    if int(self.t * 4) % 2 == 0:
                        surface.blit(self.spr_warn, (int(hz.x - 23), 6))
                continue
            if hz.kind == "oil":
                surface.blit(self.spr_oil, (int(hz.x - 48), int(hz.y - 28)))
            else:
                surface.blit(self.spr_cone, (int(hz.x - 20), int(hz.y - 20)))

    def render_front(self, engine, surface: pygame.Surface):
        """Particles, floating text and HUD chips (drawn over the cars)."""
        if not self.active(engine):
            return
        for x, y, vx, vy, life, mlife, size, color, g in self.particles:
            f = life / mlife
            r = max(1, int(size * (0.45 + 0.55 * f)))
            if size > 6.0:  # smoke grows then fades to the road colour
                r = max(1, int(size * (1.6 - 0.8 * f)))
                c = (int(color[0] * f + 60 * (1 - f)), int(color[1] * f + 62 * (1 - f)), int(color[2] * f + 68 * (1 - f)))
            else:
                c = color
            pygame.draw.circle(surface, c, (int(x), int(y)), r)

        p = engine.player
        # Brake lights are drawn by PlayerCar; DRAFT chip here
        if self.drafting:
            self._text(surface, "DRAFT", p.x, p.y - p.HEIGHT * 0.5 - 22, (120, 235, 255), 22)

        for x, y0, y, life, text, color in self.floaters:
            self._text(surface, text, x, y, color, 26, shadow=True)

        # Combo chip in the top-left of the playfield with arcade pill backing
        cx, cy = GAME_X + 20, 20
        pill_w, pill_h = 270, 36
        mult = min(4, 1 + self.combo // 2)
        if self.combo >= 1:
            pill_rect = pygame.Rect(cx, cy, pill_w, pill_h)
            pygame.draw.rect(surface, (12, 18, 28), pill_rect, border_radius=6)
            pygame.draw.rect(surface, (255, 215, 0), pill_rect, 2, border_radius=6)
            combo_str = f"COMBO {self.combo}  [x{mult}]"
            self._text(surface, combo_str, pill_rect.centerx, pill_rect.centery, (255, 225, 60), 22, left=False)

    def _text(self, surface, text, x, y, color, size, left=False, shadow=False):
        key = (text, color, size)
        spr = self._text_cache.get(key)
        if spr is None:
            if len(self._text_cache) > 80:
                self._text_cache.clear()
            spr = get_latin_font(size).render(text, True, color)
            self._text_cache[key] = spr
        rect = spr.get_rect()
        if left:
            rect.midleft = (int(x), int(y))
        else:
            rect.center = (int(x), int(y))
        if shadow:
            sh = get_latin_font(size).render(text, True, (10, 10, 18)) if (text, (10, 10, 18), size) not in self._text_cache else self._text_cache[(text, (10, 10, 18), size)]
            self._text_cache[(text, (10, 10, 18), size)] = sh
            surface.blit(sh, rect.move(2, 2))
        surface.blit(spr, rect)

    def apply_shake(self, engine):
        """Cheap whole-frame shake via in-place scroll (crash feedback)."""
        if not self.active(engine) or self.shake_timer <= 0.0:
            return
        amp = self.shake_amp * min(1.0, self.shake_timer / 0.25)
        dx = int(random.uniform(-amp, amp))
        dy = int(random.uniform(-amp, amp))
        if dx or dy:
            engine.virtual_screen.scroll(dx, dy)
