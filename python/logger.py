"""
logger.py
Centralized logging, system telemetry, and crash diagnostic system for Nihongo Master.
Handles rolling runtime logs, low-level C faults (faulthandler), unhandled Python
exceptions (sys.excepthook & threading.excepthook), and subprocess crash reporting.
"""

import os
import sys
import time
import datetime
import logging
import logging.handlers
import platform
import traceback
import threading
import signal
import faulthandler
from collections import deque

LOGGER_NAME = "NihongoMaster"
DEFAULT_APP_VERSION = "1.5.6"

# Ring buffer for recent in-memory log entries (captures context leading to a crash)
_RECENT_LOG_BUFFER = deque(maxlen=150)
_BUFFER_LOCK = threading.Lock()
_LOG_DIR = None
_LOG_FILE = None
_CRASH_FILE = None
_CRASH_FD = None
_IS_INITIALIZED = False
_APP_VERSION = DEFAULT_APP_VERSION
_TELEMETRY_CACHE = {}


class RingBufferHandler(logging.Handler):
    """Logging handler that retains the last N formatted records in memory."""
    def emit(self, record):
        try:
            msg = self.format(record)
            with _BUFFER_LOCK:
                _RECENT_LOG_BUFFER.append(msg)
        except Exception:
            pass


def resolve_log_dir() -> str:
    """Determine the best writable directory for storing Nihongo Master logs."""
    global _LOG_DIR
    if _LOG_DIR and os.path.isdir(_LOG_DIR):
        return _LOG_DIR

    # 1. Standard XDG Data Home on Linux / SteamOS (~/.local/share/nihongo-master/logs)
    xdg_data = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    candidates = [
        os.path.join(xdg_data, "nihongo-master", "logs"),
        os.path.expanduser("~/.config/nihongo-master/logs"),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs")),
        "/tmp/nihongo-master-logs"
    ]

    for cand in candidates:
        try:
            os.makedirs(cand, exist_ok=True)
            test_file = os.path.join(cand, ".write_test")
            with open(test_file, "w") as f:
                f.write("ok")
            os.remove(test_file)
            _LOG_DIR = cand
            return _LOG_DIR
        except Exception:
            continue

    # Absolute fallback
    fallback = "/tmp/nihongo-master-logs"
    os.makedirs(fallback, exist_ok=True)
    _LOG_DIR = fallback
    return _LOG_DIR


def get_log_dir() -> str:
    return resolve_log_dir()


def get_log_file_path() -> str:
    global _LOG_FILE
    if not _LOG_FILE:
        _LOG_FILE = os.path.join(resolve_log_dir(), "nihongo_master.log")
    return _LOG_FILE


def get_crash_log_file_path() -> str:
    global _CRASH_FILE
    if not _CRASH_FILE:
        _CRASH_FILE = os.path.join(resolve_log_dir(), "nihongo_master_crash.log")
    return _CRASH_FILE


def collect_system_telemetry(extra_info: dict = None) -> dict:
    """Gather comprehensive runtime system, hardware, and environment telemetry."""
    global _TELEMETRY_CACHE
    telemetry = dict(_TELEMETRY_CACHE)

    # Basic system info
    telemetry["timestamp_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    telemetry["app_version"] = _APP_VERSION
    telemetry["python_version"] = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} ({platform.python_implementation()})"
    telemetry["platform"] = platform.platform()
    telemetry["system"] = platform.system()
    telemetry["release"] = platform.release()
    telemetry["machine"] = platform.machine()

    # Steam Deck detection
    is_steam_deck = False
    os_name = ""
    try:
        if os.path.isfile("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                for line in f:
                    if line.startswith("PRETTY_NAME="):
                        os_name = line.strip().split("=", 1)[1].strip('"\'')
                    if "SteamOS" in line or "steamos" in line.lower():
                        is_steam_deck = True
    except Exception:
        pass
    telemetry["os_name"] = os_name or platform.system()
    telemetry["is_steam_deck"] = is_steam_deck or os.environ.get("SteamDeck", "") == "1"

    # Environment variables
    telemetry["session_type"] = os.environ.get("XDG_SESSION_TYPE", "unknown")
    telemetry["display"] = os.environ.get("DISPLAY", "none")
    telemetry["wayland_display"] = os.environ.get("WAYLAND_DISPLAY", "none")
    telemetry["sdl_videodriver"] = os.environ.get("SDL_VIDEODRIVER", "default")
    telemetry["sdl_audiodriver"] = os.environ.get("SDL_AUDIODRIVER", "default")
    telemetry["appimage"] = os.environ.get("APPIMAGE", "none")

    # Pygame / SDL telemetry if pygame is imported and initialized
    if "pygame" in sys.modules:
        try:
            import pygame
            telemetry["pygame_version"] = pygame.version.ver
            sdl_ver = pygame.get_sdl_version()
            telemetry["sdl_version"] = f"{sdl_ver[0]}.{sdl_ver[1]}.{sdl_ver[2]}"
            if pygame.display.get_init():
                telemetry["display_driver"] = pygame.display.get_driver()
                surf = pygame.display.get_surface()
                if surf:
                    telemetry["window_size"] = f"{surf.get_width()}x{surf.get_height()}"
                info = pygame.display.Info()
                telemetry["screen_hardware_max"] = f"{info.current_w}x{info.current_h}"
            if pygame.mixer.get_init():
                freq, size, channels = pygame.mixer.get_init()
                telemetry["audio_mixer"] = f"{freq}Hz, {size}bit, {channels}ch"
            if pygame.joystick.get_init():
                count = pygame.joystick.get_count()
                joy_names = []
                for i in range(count):
                    try:
                        j = pygame.joystick.Joystick(i)
                        joy_names.append(j.get_name())
                    except Exception:
                        joy_names.append(f"Joystick {i}")
                telemetry["joysticks_connected"] = f"{count} ({', '.join(joy_names) if joy_names else 'none'})"
        except Exception:
            pass

    if extra_info:
        telemetry.update(extra_info)

    return telemetry


def write_crash_report(exc_type=None, exc_value=None, exc_tb=None, reason: str = "Unhandled Exception", extra_context: dict = None) -> str:
    """Generate and write an exhaustive crash report to disk."""
    log_dir = resolve_log_dir()
    crash_path = get_crash_log_file_path()
    
    # Also create a timestamped copy to prevent losing historical crashes
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    timestamped_crash_path = os.path.join(log_dir, f"crash_{timestamp_str}.log")

    telemetry = collect_system_telemetry(extra_context)

    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append(f" NIHONGO MASTER - FATAL CRASH REPORT")
    report_lines.append("=" * 80)
    report_lines.append(f"Timestamp (UTC): {telemetry.get('timestamp_utc')}")
    report_lines.append(f"Game Version:    {telemetry.get('app_version')}")
    report_lines.append(f"Crash Reason:    {reason}")
    report_lines.append("")

    report_lines.append("--------------------------------------------------------------------------------")
    report_lines.append(" SYSTEM & HARDWARE TELEMETRY")
    report_lines.append("--------------------------------------------------------------------------------")
    for key, val in sorted(telemetry.items()):
        report_lines.append(f"  {key:<22}: {val}")
    report_lines.append("")

    report_lines.append("--------------------------------------------------------------------------------")
    report_lines.append(" ACTIVE THREADS")
    report_lines.append("--------------------------------------------------------------------------------")
    for th in threading.enumerate():
        report_lines.append(f"  Thread ID: {th.ident:<16} Name: {th.name:<24} Daemon: {th.daemon} Alive: {th.is_alive()}")
    report_lines.append("")

    report_lines.append("--------------------------------------------------------------------------------")
    report_lines.append(" EXCEPTION TRACEBACK")
    report_lines.append("--------------------------------------------------------------------------------")
    if exc_type and exc_value:
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        report_lines.append("".join(tb_lines).rstrip())
    else:
        report_lines.append("  (No Python exception object provided - likely low-level C fault or subgame crash)")
        # Dump current call stack of this thread
        report_lines.append("".join(traceback.format_stack()).rstrip())
    report_lines.append("")

    report_lines.append("--------------------------------------------------------------------------------")
    report_lines.append(" RECENT LOG HISTORY (Ring Buffer - Last Events Leading to Crash)")
    report_lines.append("--------------------------------------------------------------------------------")
    with _BUFFER_LOCK:
        if _RECENT_LOG_BUFFER:
            for item in _RECENT_LOG_BUFFER:
                report_lines.append(f"  {item}")
        else:
            report_lines.append("  (Log buffer empty)")
    report_lines.append("")
    report_lines.append("=" * 80)
    report_lines.append(" END OF CRASH REPORT")
    report_lines.append("=" * 80)
    report_lines.append("")

    report_content = "\n".join(report_lines)

    # Write to primary crash log
    try:
        with open(crash_path, "w", encoding="utf-8") as f:
            f.write(report_content)
    except Exception as e:
        print(f"[NihongoMaster] Warning: Failed to write {crash_path}: {e}", file=sys.stderr)

    # Write timestamped copy
    try:
        with open(timestamped_crash_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        _prune_old_crash_reports(log_dir, keep=5)
    except Exception:
        pass

    # Print loud alert to console/stderr
    print("\n" + "=" * 80, file=sys.stderr)
    print(" [CRASH DETECTED] Nihongo Master encountered a fatal error!", file=sys.stderr)
    print(f" A detailed crash diagnostic report has been saved to:", file=sys.stderr)
    print(f"   --> {crash_path}", file=sys.stderr)
    print("=" * 80 + "\n", file=sys.stderr)

    return crash_path


def _prune_old_crash_reports(log_dir: str, keep: int = 5):
    """Keep only the N most recent timestamped crash reports to avoid disk clutter."""
    try:
        files = []
        for name in os.listdir(log_dir):
            if name.startswith("crash_") and name.endswith(".log"):
                p = os.path.join(log_dir, name)
                files.append((os.path.getmtime(p), p))
        files.sort(reverse=True)
        for _, p in files[keep:]:
            try:
                os.remove(p)
            except Exception:
                pass
    except Exception:
        pass


def _unhandled_exception_hook(exc_type, exc_value, exc_tb):
    """Global sys.excepthook to intercept unhandled exceptions in the main thread."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_tb)
        return

    logger = get_logger()
    logger.critical("Unhandled exception caught by global hook!", exc_info=(exc_type, exc_value, exc_tb))
    write_crash_report(exc_type, exc_value, exc_tb, reason="Unhandled Main Thread Exception")
    # Flush handlers
    logging.shutdown()
    sys.exit(1)


def _threading_exception_hook(args):
    """Global threading.excepthook to intercept unhandled exceptions in background threads."""
    logger = get_logger()
    logger.critical(f"Unhandled exception in thread '{args.thread.name}'!", exc_info=(args.exc_type, args.exc_value, args.exc_traceback))
    write_crash_report(args.exc_type, args.exc_value, args.exc_traceback, reason=f"Unhandled Thread Exception ({args.thread.name})")


def _signal_handler(signum, frame):
    """Graceful signal handler for SIGTERM and SIGINT."""
    sig_name = signal.Signals(signum).name if hasattr(signal, "Signals") else str(signum)
    logger = get_logger()
    logger.info(f"Received termination signal: {sig_name}. Performing clean shutdown.")
    logging.shutdown()
    sys.exit(0)


def init_logging(app_version: str = DEFAULT_APP_VERSION, debug: bool = False) -> logging.Logger:
    """Initialize the Nihongo Master logging and crash reporting framework."""
    global _IS_INITIALIZED, _APP_VERSION, _CRASH_FD
    if _IS_INITIALIZED:
        return logging.getLogger(LOGGER_NAME)

    _APP_VERSION = app_version
    log_dir = resolve_log_dir()
    log_file = get_log_file_path()
    crash_file = get_crash_log_file_path()

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    for h in list(logger.handlers):
        try:
            h.close()
        except Exception:
            pass
    logger.handlers.clear()

    if _CRASH_FD:
        try:
            _CRASH_FD.close()
        except Exception:
            pass
        _CRASH_FD = None

    # Formatter
    fmt = logging.Formatter(
        fmt="[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(name)s:%(module)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Console Handler (stdout)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG if debug else logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # 2. Rolling File Handler (5 MB max, keep 3 backups)
    try:
        fh = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        )
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    except Exception as e:
        print(f"[NihongoMaster] Warning: Failed to initialize file logger at {log_file}: {e}", file=sys.stderr)

    # 3. In-Memory Ring Buffer Handler
    rb = RingBufferHandler()
    rb.setLevel(logging.DEBUG)
    rb.setFormatter(fmt)
    logger.addHandler(rb)

    # 4. Low-level C crash handler (faulthandler)
    try:
        _CRASH_FD = open(crash_file, "a", encoding="utf-8")
        faulthandler.enable(file=_CRASH_FD, all_threads=True)
    except Exception as e:
        print(f"[NihongoMaster] Warning: Could not enable faulthandler: {e}", file=sys.stderr)

    # 5. Global Exception Hooks
    sys.excepthook = _unhandled_exception_hook
    if hasattr(threading, "excepthook"):
        threading.excepthook = _threading_exception_hook

    # 6. Signals
    try:
        signal.signal(signal.SIGTERM, _signal_handler)
        signal.signal(signal.SIGINT, _signal_handler)
    except Exception:
        pass

    _IS_INITIALIZED = True

    # Initial session banner
    telemetry = collect_system_telemetry()
    logger.info("=" * 68)
    logger.info(f"Nihongo Master v{app_version} - Session Started")
    logger.info(f"Platform: {telemetry.get('platform')} | OS: {telemetry.get('os_name')}")
    logger.info(f"Python: {telemetry.get('python_version')}")
    logger.info(f"Session: {telemetry.get('session_type')} | Display: {telemetry.get('display')} | Wayland: {telemetry.get('wayland_display')}")
    logger.info(f"Log Path: {log_file}")
    logger.info("=" * 68)

    return logger


def get_logger() -> logging.Logger:
    """Retrieve the main application logger instance."""
    if not _IS_INITIALIZED:
        return init_logging()
    return logging.getLogger(LOGGER_NAME)


def log_subgame_execution(cmd: list[str], env: dict, returncode: int, stdout_text: str = "", stderr_text: str = ""):
    """Log subgame process exit status and record errors if non-zero exit code detected."""
    logger = get_logger()
    subgame_name = os.path.basename(cmd[0]) if cmd else "unknown_subgame"
    
    if returncode == 0:
        logger.info(f"Subgame '{subgame_name}' exited normally (returncode 0).")
        if stderr_text and stderr_text.strip():
            logger.debug(f"Subgame '{subgame_name}' stderr notice:\n{stderr_text.strip()}")
    else:
        sig_note = ""
        if returncode < 0:
            sig_num = -returncode
            try:
                sig_note = f" (Killed by Signal {signal.Signals(sig_num).name})"
            except Exception:
                sig_note = f" (Killed by Signal {sig_num})"

        logger.critical(
            f"Subgame '{subgame_name}' crashed or exited abnormally with returncode {returncode}{sig_note}!\n"
            f"Command: {' '.join(cmd)}\n"
            f"Captured STDERR:\n{stderr_text.strip() or '(none)'}\n"
            f"Captured STDOUT:\n{stdout_text.strip() or '(none)'}"
        )

        # Trigger crash report for subgame crash
        write_crash_report(
            reason=f"Subgame Crash ({subgame_name} returncode {returncode}{sig_note})",
            extra_context={
                "subgame_name": subgame_name,
                "subgame_cmd": " ".join(cmd),
                "subgame_returncode": returncode,
                "subgame_signal": sig_note,
                "subgame_stderr": stderr_text[:2000],
                "subgame_stdout": stdout_text[:2000]
            }
        )
