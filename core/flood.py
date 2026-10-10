"""
Bizz V3 — flood engine
Self-loop flood ke IP publik sendiri (prank mode).
"""

import threading
import time
import requests

from core.utils import get_public_ip


class SelfFlood:
    def __init__(self, target_url, threads=200, timeout=3):
        self.target_url = target_url
        self.threads = threads
        self.timeout = timeout
        self.stop_flag = threading.Event()
        self.counter = {"req": 0, "err": 0}
        self.lock = threading.Lock()
        self.self_ip = None
        self._threads = []

    def _worker(self):
        while not self.stop_flag.is_set():
            try:
                url = f"http://{self.self_ip}/?x={time.time()}"
                requests.get(url, timeout=self.timeout)
                with self.lock:
                    self.counter["req"] += 1
            except Exception:
                with self.lock:
                    self.counter["err"] += 1
                time.sleep(0.005)

    def start(self, duration=60):
        self.self_ip = get_public_ip()
        if not self.self_ip:
            print("\033[91m[!] Gagal ambil IP publik.\033[0m")
            return

        print(f"\033[93m[*]\033[0m Self IP   : \033[96m{self.self_ip}\033[0m")
        print(f"\033[93m[*]\033[0m Target    : \033[96m{self.target_url}\033[0m")
        print(f"\033[93m[*]\033[0m Threads   : \033[96m{self.threads}\033[0m")
        print(f"\033[93m[*]\033[0m Duration  : \033[96m{duration}s\033[0m\n")

        self.stop_flag.clear()
        self.counter = {"req": 0, "err": 0}
        self._threads = [
            threading.Thread(target=self._worker, daemon=True)
            for _ in range(self.threads)
        ]
        for t in self._threads:
            t.start()

        start = time.time()
        try:
            while time.time() - start < duration and not self.stop_flag.is_set():
                time.sleep(1)
                elapsed = int(time.time() - start)
                print(
                    f"\r\033[95m[~]\033[0m {elapsed:>3}s | "
                    f"Req: {self.counter['req']:>6} | "
                    f"Err: {self.counter['err']:>6}",
                    end="",
                )
        except KeyboardInterrupt:
            print()
        finally:
            self.stop_flag.set()
            for t in self._threads:
                t.join(timeout=1)

        print()
        print(f"\033[92m[+]\033[0m Total Req : {self.counter['req']}")
        print(f"\033[92m[+]\033[0m Total Err : {self.counter['err']}")

    def restore(self):
        self.stop_flag.set()
        print("\033[93m[*]\033[0m Restoring koneksi...")
        time.sleep(2)
        print("\033[92m[+]\033[0m Done.")
