"""
main.py
Entry point for Nihongo Master (Python Edition).
Integrated with enterprise-grade logging, hardware telemetry, and crash diagnostics.
"""

import os
import sys
import argparse
from game_config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, VIRTUAL_WIDTH, VIRTUAL_HEIGHT,
    GAME_VERSION, detect_maximum_resolution, compute_aspect_ratio
)
from logger import (
    init_logging, get_logger, get_log_dir, get_log_file_path,
    get_crash_log_file_path, write_crash_report
)

def print_log_info():
    """CLI utility function to display current log file locations and recent entries."""
    log_file = get_log_file_path()
    crash_file = get_crash_log_file_path()
    log_dir = get_log_dir()

    print("=" * 70)
    print(" Nihongo Master - System & Crash Log Information")
    print("=" * 70)
    print(f"Log Directory:    {log_dir}")
    print(f"Runtime Log File: {log_file} (Exists: {os.path.isfile(log_file)})")
    print(f"Crash Dump File:  {crash_file} (Exists: {os.path.isfile(crash_file)})")
    print("=" * 70)

    if os.path.isfile(crash_file):
        print("\n--- Recent Crash Dump (Last 40 lines) ---")
        try:
            with open(crash_file, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                for line in lines[-40:]:
                    print(line, end="")
        except Exception as e:
            print(f"Error reading crash log: {e}")

    if os.path.isfile(log_file):
        print("\n--- Recent Runtime Log (Last 25 lines) ---")
        try:
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                for line in lines[-25:]:
                    print(line, end="")
        except Exception as e:
            print(f"Error reading runtime log: {e}")
    print("\n" + "=" * 70)

def main():
    parser = argparse.ArgumentParser(description="Nihongo Master (Python Edition)")
    parser.add_argument("--mode", type=str, default=None, choices=["hiragana", "katakana", "cards", "hiragana_cards", "katakana_cards", "sniper", "hiragana_sniper", "katakana_sniper"], help="Game mode (hiragana, katakana, cards, sniper, etc.)")
    parser.add_argument("--stage", type=int, default=None, help="Stage to start on (1-11)")
    parser.add_argument("--trackdist", type=float, default=0.0, help="Initial track distance")
    parser.add_argument("--title", action="store_true", help="Force title screen")
    parser.add_argument("--titlemenu", type=int, default=0, help="Title screen menu index")
    parser.add_argument("--menu", action="store_true", help="Open audio settings menu immediately")
    parser.add_argument("--pause", action="store_true", help="Start game paused")
    parser.add_argument("--stageclear", action="store_true", help="Start with stage clear banner")
    parser.add_argument("--stageselect", action="store_true", help="Start directly in stage select screen")
    parser.add_argument("--screenshot", type=str, default="", help="Save screenshot to path after frames and exit")
    parser.add_argument("--windowed", action="store_true", help="Run in windowed mode instead of fullscreen")
    parser.add_argument("--headless", action="store_true", help="Run without graphical display")
    parser.add_argument("--res", type=str, default="", help="Force resolution WIDTHxHEIGHT (e.g. 1920x1080, 1280x800)")
    parser.add_argument("--aspect", type=str, default="auto", choices=["auto", "stretch"], help="Aspect ratio mode ('auto' or 'stretch')")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug logging")
    parser.add_argument("--logs", action="store_true", help="Print log file paths and recent entries, then exit")
    args = parser.parse_args()

    # 1. Quick CLI log inspector
    if args.logs:
        print_log_info()
        sys.exit(0)

    # 2. Initialize Centralized Logging & Crash Capture System
    logger = init_logging(app_version=GAME_VERSION, debug=args.debug)
    logger.info(f"CLI arguments received: {sys.argv[1:]}")

    if args.headless:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        logger.info("Headless execution mode active (SDL dummy drivers enabled)")

    # Prevent SDL from minimizing the fullscreen window when losing focus to child processes (e.g. Godot)
    os.environ["SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS"] = "0"

    try:
        import pygame
        pygame.init()
        pygame.display.set_caption("Nihongo Master - 日本語 マスター")

        # 3. Auto-detect maximum display resolution supported by system
        detected_max = detect_maximum_resolution()
        target_w, target_h = detected_max

        if args.res:
            try:
                parts = args.res.lower().split("x")
                target_w, target_h = int(parts[0]), int(parts[1])
            except Exception:
                logger.warning(f"Invalid --res format '{args.res}', falling back to detected {target_w}x{target_h}")

        disp_ratio, aspect_label = compute_aspect_ratio(target_w, target_h)
        logger.info(f"Detected Maximum Resolution: {target_w}x{target_h}")
        logger.info(f"Auto Aspect Ratio: {aspect_label} ({disp_ratio:.3f})")

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        if not args.windowed and not args.headless:
            flags |= pygame.FULLSCREEN

        # 4. Display mode initialization with graceful fallback chain
        screen = None
        if not args.windowed and not args.headless:
            try:
                # Try maximum detected resolution in fullscreen
                screen = pygame.display.set_mode((target_w, target_h), flags)
            except Exception as e1:
                logger.warning(f"Fullscreen mode ({target_w}x{target_h}) notice: {e1}, attempting desktop fallback (0, 0)")
                try:
                    # Try SDL desktop mode fallback (0, 0)
                    screen = pygame.display.set_mode((0, 0), flags)
                except Exception as e2:
                    logger.warning(f"Desktop mode (0,0) notice: {e2}, falling back to windowed mode")
                    screen = pygame.display.set_mode((min(target_w, 1920), min(target_h, 1200)), pygame.DOUBLEBUF)
        else:
            if args.res:
                win_w, win_h = target_w, target_h
            else:
                if target_w >= 1920 and target_h >= 1200:
                    win_w, win_h = 1920, 1200
                else:
                    win_w, win_h = 1280, 800
            screen = pygame.display.set_mode((win_w, win_h), pygame.DOUBLEBUF)

        actual_w, actual_h = screen.get_size()
        logger.info(f"Active Screen Resolution: {actual_w}x{actual_h}")

        # Immediately hide mouse cursor on startup
        try:
            invis_cursor = pygame.cursors.Cursor((8, 8), (0, 0), (0,)*8, (0,)*8)
            pygame.mouse.set_cursor(invis_cursor)
        except Exception:
            pass
        pygame.mouse.set_visible(False)

        stage_to_start = args.stage if args.stage is not None else 1
        skip_title = not args.title and (args.stage is not None or args.trackdist > 0.0 or args.pause or args.stageclear)

        # Import GameEngine after pygame.init() and display.set_mode()
        from game_engine import GameEngine

        engine = GameEngine(
            start_stage=stage_to_start,
            skip_title=skip_title,
            custom_dist=args.trackdist,
            start_paused=args.pause,
            start_menu=args.menu,
            start_stageclear=args.stageclear,
            detected_res=(actual_w, actual_h),
            aspect_mode=args.aspect,
            game_mode=args.mode if args.mode else "hiragana"
        )
        if args.mode:
            engine.game_mode = args.mode
            if args.mode in ("cards", "hiragana_cards"):
                engine.title_menu_index = 2
            elif args.mode == "katakana_cards":
                engine.title_menu_index = 3
            elif args.mode in ("sniper", "hiragana_sniper"):
                engine.title_menu_index = 4
            elif args.mode == "katakana_sniper":
                engine.title_menu_index = 5
            elif args.mode == "katakana":
                engine.title_menu_index = 1
                if engine.is_title_screen:
                    engine.player.update_kana("ア")
                engine.player.hiragana_extras = True
                engine.player.arcade_extras = True
                engine.road.rebuild_stage11_gantries(args.mode)
            else:
                engine.title_menu_index = 0
                if engine.is_title_screen:
                    engine.player.update_kana("あ")
                engine.player.hiragana_extras = True
                engine.player.arcade_extras = True
                engine.road.rebuild_stage11_gantries(args.mode)

        if args.titlemenu > 0:
            engine.title_menu_index = args.titlemenu

        if args.stageselect:
            engine.is_title_screen = True
            engine.is_stage_select = True

        if args.screenshot:
            # Run 25 frames to settle physics & textures, capture, then exit
            for _ in range(25):
                engine.run_frame(1.0 / 60.0)
            pygame.image.save(screen, args.screenshot)
            logger.info(f"Screenshot successfully saved to: {args.screenshot}")
            pygame.quit()
            sys.exit(0)

        # Standard game loop
        engine.run()

    except Exception as e:
        logger.critical(f"Fatal unhandled exception in main: {e}", exc_info=True)
        crash_path = write_crash_report(*sys.exc_info(), reason=f"Fatal Exception in main: {e}")
        try:
            pygame.quit()
        except Exception:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()
