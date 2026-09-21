"""
update_manager.py
Background thread auto-updater for Nihongo Master.
Checks GitHub repository / releases, downloads updates with progress,
and performs atomic file replacement while preserving the exact filename
and path so Steam shortcuts and desktop launchers never break.
"""

import os
import sys
import json
import time
import ssl
import urllib.request
import urllib.error
import threading
import subprocess
import pygame

from game_config import (
    GAME_VERSION, GITHUB_REPO, VERSION_CHECK_URL, RELEASES_API_URL
)

def get_ssl_context():
    """Create a resilient SSL context with CA bundle detection and fallback."""
    # 1. Try certifi if installed
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        pass

    # 2. Try standard system CA bundles on Linux / SteamOS
    ca_candidates = [
        "/etc/ssl/certs/ca-certificates.crt", # Debian, Ubuntu, Arch, SteamOS
        "/etc/pki/tls/certs/ca-bundle.crt",   # Fedora, RHEL, CentOS
        "/etc/ssl/cert.pem",                   # Alpine, Arch
        "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem",
    ]
    for ca_path in ca_candidates:
        if os.path.isfile(ca_path):
            try:
                return ssl.create_default_context(cafile=ca_path)
            except Exception:
                pass

    # 3. Default OpenSSL context
    try:
        return ssl.create_default_context()
    except Exception:
        pass

    # 4. Fallback to unverified context to ensure network requests never fail on SteamOS
    try:
        return ssl._create_unverified_context()
    except Exception:
        return None

def parse_version(v_str: str) -> tuple[int, ...]:
    """Parse version string into comparable tuple (e.g., 'v1.0.1' -> (1, 0, 1))."""
    if not v_str:
        return (0,)
    clean = v_str.strip().lstrip("vV")
    parts = []
    for p in clean.split("."):
        num = "".join(filter(str.isdigit, p))
        parts.append(int(num) if num else 0)
    return tuple(parts)

class UpdateManager:
    # State constants
    STATE_IDLE = "IDLE"
    STATE_CHECKING = "CHECKING"
    STATE_UP_TO_DATE = "UP_TO_DATE"
    STATE_UPDATE_AVAILABLE = "UPDATE_AVAILABLE"
    STATE_DOWNLOADING = "DOWNLOADING"
    STATE_SUCCESS = "SUCCESS"
    STATE_ERROR = "ERROR"

    def __init__(self):
        self.state = self.STATE_IDLE
        self.current_version = GAME_VERSION
        self.remote_version = None
        self.release_name = None
        self.changelog = None
        self.download_url = None
        self.fallback_url = None
        self.target_path = self.get_target_appimage_path()
        
        # Download telemetry
        self.bytes_downloaded = 0
        self.bytes_total = 0
        self.progress_percent = 0.0
        self.error_message = ""
        self.lock = threading.Lock()

    @staticmethod
    def get_target_appimage_path() -> str:
        """Resolve exact AppImage path to preserve filename and Steam shortcuts."""
        # 1. If launched via AppImage runtime, APPIMAGE environment variable has the exact path
        env_appimage = os.environ.get("APPIMAGE")
        if env_appimage and os.path.isfile(env_appimage):
            return os.path.abspath(env_appimage)

        # 2. Check argv[0] if invoked directly as .AppImage
        if sys.argv and sys.argv[0].endswith(".AppImage") and os.path.isfile(sys.argv[0]):
            return os.path.abspath(sys.argv[0])

        # 3. Standard Steam Deck / Linux downloads location
        downloads_path = os.path.expanduser("~/Downloads/Nihongo_Master-x86_64.AppImage")
        if os.path.isfile(downloads_path):
            return os.path.abspath(downloads_path)

        # 4. Local workspace copy fallback
        app_path = "/home/deck/Applications/nihongo-master/Nihongo_Master-x86_64.AppImage"
        if os.path.isfile(app_path):
            return app_path

        local_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Nihongo_Master-x86_64.AppImage"))
        if os.path.isfile(local_path):
            return local_path

        return downloads_path

    def check_for_updates(self, force: bool = False):
        """Start asynchronous update check."""
        if self.state in (self.STATE_CHECKING, self.STATE_DOWNLOADING) and not force:
            return
        self.state = self.STATE_CHECKING
        self.error_message = ""
        threading.Thread(target=self._run_check, daemon=True).start()

    def _run_check(self):
        time.sleep(0.3) # Brief UI transition ease
        try:
            remote_info = self._fetch_version_metadata()
            if not remote_info:
                with self.lock:
                    self.state = self.STATE_ERROR
                    self.error_message = "Unable to retrieve version data from GitHub."
                return

            r_ver = remote_info.get("version", "")
            r_url = remote_info.get("download_url") or remote_info.get("fallback_raw_url")
            r_desc = remote_info.get("changelog") or remote_info.get("name", "")
            
            with self.lock:
                self.remote_version = r_ver
                self.release_name = remote_info.get("name", f"Version {r_ver}")
                self.changelog = r_desc
                self.download_url = r_url
                self.fallback_url = remote_info.get("fallback_raw_url")

                cur_tup = parse_version(self.current_version)
                rem_tup = parse_version(r_ver)

                if rem_tup > cur_tup:
                    self.state = self.STATE_UPDATE_AVAILABLE
                else:
                    self.state = self.STATE_UP_TO_DATE

        except Exception as e:
            with self.lock:
                self.state = self.STATE_ERROR
                self.error_message = f"Check failed: {e}"

    def _fetch_version_metadata(self) -> dict:
        ctx = get_ssl_context()
        headers = {
            "User-Agent": "NihongoMaster-Updater/1.0.1",
            "Accept": "application/vnd.github.v3+json, application/json, text/plain",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }

        candidates = []

        # 1. GitHub Releases API (Immediate, bypasses CDN cache)
        try:
            req = urllib.request.Request(RELEASES_API_URL, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                if resp.status == 200:
                    rel = json.loads(resp.read().decode("utf-8"))
                    tag = rel.get("tag_name", "").lstrip("vV")
                    assets = rel.get("assets", [])
                    d_url = None
                    for a in assets:
                        if a.get("name", "").endswith(".AppImage"):
                            d_url = a.get("browser_download_url")
                            break
                    candidates.append({
                        "version": tag,
                        "name": rel.get("name", f"Release {tag}"),
                        "changelog": rel.get("body", "Updated release on GitHub."),
                        "download_url": d_url,
                        "fallback_raw_url": f"https://github.com/{GITHUB_REPO}/releases/download/v{tag}/Nihongo_Master-x86_64.AppImage"
                    })
        except Exception:
            pass

        # 2. Raw version.json on raw.githubusercontent.com
        try:
            cachebust_url = f"{VERSION_CHECK_URL}?t={int(time.time())}"
            req = urllib.request.Request(cachebust_url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    candidates.append(data)
        except Exception:
            pass

        # 3. Fallback: curl CLI if urllib encounters SSL/network blocks
        if not candidates:
            try:
                out = subprocess.check_output(
                    ["curl", "-s", "-L", "--max-time", "10",
                     "-H", "User-Agent: NihongoMaster-Updater/1.0.1",
                     "-H", "Cache-Control: no-cache",
                     f"{VERSION_CHECK_URL}?t={int(time.time())}"],
                    stderr=subprocess.DEVNULL
                )
                if out:
                    data = json.loads(out.decode("utf-8"))
                    candidates.append(data)
            except Exception:
                pass

        if not candidates:
            return None

        # Return candidate with highest version
        candidates.sort(key=lambda c: parse_version(c.get("version", "")), reverse=True)
        return candidates[0]

    def start_download(self):
        """Start asynchronous download and atomic replacement."""
        if self.state == self.STATE_DOWNLOADING:
            return
        self.state = self.STATE_DOWNLOADING
        self.bytes_downloaded = 0
        self.bytes_total = 0
        self.progress_percent = 0.0
        self.error_message = ""
        threading.Thread(target=self._run_download, daemon=True).start()

    download_and_apply_update = start_download

    def _run_download(self):
        urls_to_try = [self.download_url, self.fallback_url]
        urls_to_try = [u for u in urls_to_try if u]
        
        target = self.get_target_appimage_path()
        target_dir = os.path.dirname(target)
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir, exist_ok=True)
            
        temp_file = target + ".tmp_update"
        
        download_ok = False
        headers = {
            "User-Agent": "NihongoMaster-Updater/1.0.1",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
        ctx = get_ssl_context()

        for url in urls_to_try:
            try:
                sep = "&" if "?" in url else "?"
                busted_url = f"{url}{sep}t={int(time.time())}"
                req = urllib.request.Request(busted_url, headers=headers)
                with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                    if resp.status != 200:
                        continue
                    
                    total_size = resp.headers.get("Content-Length")
                    with self.lock:
                        self.bytes_total = int(total_size) if total_size else 47000000
                        self.bytes_downloaded = 0

                    with open(temp_file, "wb") as out_f:
                        chunk_size = 65536
                        while True:
                            chunk = resp.read(chunk_size)
                            if not chunk:
                                break
                            out_f.write(chunk)
                            with self.lock:
                                self.bytes_downloaded += len(chunk)
                                if self.bytes_total > 0:
                                    self.progress_percent = min(100.0, (self.bytes_downloaded / self.bytes_total) * 100.0)

                # Validate downloaded file has reasonable size (> 5MB)
                if os.path.isfile(temp_file) and os.path.getsize(temp_file) > 5 * 1024 * 1024:
                    download_ok = True
                    break
                else:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
            except Exception:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except Exception:
                        pass
                continue

        # Fallback to curl if urllib failed
        if not download_ok and urls_to_try:
            for url in urls_to_try:
                try:
                    with self.lock:
                        self.bytes_total = 47000000
                        self.bytes_downloaded = 23500000
                        self.progress_percent = 50.0
                    res = subprocess.run(
                        ["curl", "-L", "-f", "--max-time", "120",
                         "-H", "User-Agent: NihongoMaster-Updater/1.0.1",
                         "-o", temp_file, url],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    if res.returncode == 0 and os.path.isfile(temp_file) and os.path.getsize(temp_file) > 5 * 1024 * 1024:
                        download_ok = True
                        with self.lock:
                            self.progress_percent = 100.0
                            self.bytes_downloaded = os.path.getsize(temp_file)
                        break
                except Exception:
                    pass

        if not download_ok:
            with self.lock:
                self.state = self.STATE_ERROR
                self.error_message = "Failed to download update from release servers."
            return

        # Perform atomic file replacement
        try:
            os.chmod(temp_file, 0o755)
            # os.replace is atomic and works even if target is actively running on Linux
            os.replace(temp_file, target)
            os.chmod(target, 0o755)
            
            with self.lock:
                self.state = self.STATE_SUCCESS
                self.current_version = self.remote_version
        except Exception as e:
            with self.lock:
                self.state = self.STATE_ERROR
                self.error_message = f"Failed to apply update: {e}"

    def restart_game(self):
        """Relaunch the updated executable and exit cleanly."""
        target = self.get_target_appimage_path()
        if os.path.isfile(target) and os.access(target, os.X_OK):
            try:
                clean_env = os.environ.copy()
                for var in ["APPIMAGE", "APPDIR", "ARGV0", "OWD"]:
                    clean_env.pop(var, None)
                if "LD_LIBRARY_PATH" in clean_env:
                    clean_ld = [p for p in clean_env["LD_LIBRARY_PATH"].split(":") if not p.startswith("/tmp/.mount_")]
                    if clean_ld:
                        clean_env["LD_LIBRARY_PATH"] = ":".join(clean_ld)
                    else:
                        clean_env.pop("LD_LIBRARY_PATH", None)
                if "PATH" in clean_env:
                    clean_path = [p for p in clean_env["PATH"].split(":") if not p.startswith("/tmp/.mount_")]
                    clean_env["PATH"] = ":".join(clean_path)

                subprocess.Popen([target], env=clean_env, start_new_session=True)
                pygame.quit()
                sys.exit(0)
            except Exception as e:
                print(f"Restart failed: {e}")

