#!/usr/bin/env python3
"""
Bizz V3 — Hacker Screen Self-Flood
Visual hacker full screen, request beneran ke IP sendiri.
"""

import os
import random
import socket
import string
import sys
import threading
import time

import requests


G  = "\033[92m"
DG = "\033[32m"
R  = "\033[91m"
Y  = "\033[93m"
C  = "\033[96m"
W  = "\033[97m"
M  = "\033[95m"
RESET = "\033[0m"
BOLD  = "\033[1m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


BANNER = r"""
  ____  _____ _______ ______
 |  _ \|_   _|__   __|___  /
 | |_) | | |    | |     / /
 |  _ <  | |    | |    / /
 | |_) |_| |_   | |   / /__
 |____/|_____|  |_|  /_____/

        >>  B I Z Z   V 3  <<
        >> hacker screen edition <<
"""


LOGS = [
    "Sending packet to {ip}:{port} ... OK",
    "TCP handshake {ip}:443 ... ESTABLISHED",
    "Injecting payload #{n} ... DONE",
    "Bypassing WAF rule #{n} ... OK",
    "GET /?x={rnd} HTTP/1.1 200 OK",
    "POST /api/{rnd} HTTP/1.1 200 OK",
    "Flooding {ip} with {n} conns/sec",
    "Bypassing Cloudflare ... OK",
    "SYN flood {ip}:80 ... OK",
    "HTTP/2 rapid reset ... SENT",
    "Opening socket #{n} ... OK",
    "Sending {n} bytes to {ip}",
    "Spoofing X-Forwarded-For: {rnd}",
    "Rotating user-agent: {rnd}",
    "Thread #{n} spawned ... OK",
    "Connection #{n} alive",
    "Response from {ip}: 200 OK ({rnd}ms)",
    "Retrying {ip} ... OK",
    "SYN-ACK received from {ip}",
    "Payload #{n} delivered",
    "Bypassing rate-limit ... OK",
    "Fragmented packet #{n} sent",
    "Redirect chained {ip} -> {rnd}",
    "SSL handshake {ip}:443 ... OK",
    "Keep-alive #{n} ... OK",
    "Chunked body #{n} sent",
    "TLS 1.3 negotiate ... OK",
    "DNS amplification {n}x ... OK",
    "Slowloris thread #{n} ... OK",
    "Header injection #{n} ... OK",
    "Payload 8KB -> {ip} ... SENT",
    "Bypassing IPS ... OK",
    "Sniffing response #{n} ... OK",
    "Persistent conn #{n} ... OK",
]


def rnd_str(n=8):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def rnd_log(ip):
    return random.choice(LOGS).format(
        ip=ip,
        port=random.choice([80, 443, 8080, 8443]),
        n=random.randint(100, 99999),
        rnd=rnd_str(random.randint(6, 12)),
    )


def resolve_ip(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    host = url.split("//", 1)[1].split("/", 1)[0]
    try:
        return host, socket.gethostbyname(host)
    except socket.gaierror:
        return host, None


def get_my_ip():
    for url in ["https://api.ipify.org", "https://ifconfig.me/ip", "https://icanhazip.com"]:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200 and r.text.strip():
                return r.text.strip()
        except Exception:
            continue
    return None


# ============================================================
# FLOOD BENERAN ke IP sendiri (threads banyak)
# ============================================================
class SelfFlood:
    def __init__(self, threads=400, timeout=2):
        self.threads = threads
        self.timeout = timeout
        self.stop_flag = threading.Event()
        self.counter = 0
        self.err = 0
        self.lock = threading.Lock()
        self.active_workers = 0

    def _worker(self, my_ip):
        with self.lock:
            self.active_workers += 1
        while not self.stop_flag.is_set():
            try:
                requests.get(
                    f"http://{my_ip}/?x={time.time()}&r={rnd_str()}",
                    timeout=self.timeout,
                    headers={"User-Agent": f"BizzV3/{rnd_str(6)}"},
                )
                with self.lock:
                    self.counter += 1
            except Exception:
                with self.lock:
                    self.err += 1

    def start(self, my_ip):
        for _ in range(self.threads):
            threading.Thread(
                target=self._worker, args=(my_ip,), daemon=True
            ).start()

    def stop(self):
        self.stop_flag.set()


# ============================================================
# HEADER DASHBOARD (redraw pakai cursor ke atas)
# ============================================================
def draw_dashboard(target_host, target_ip, my_ip, counter, err, elapsed, duration, lines_drawn):
    # naikin cursor sebanyak lines_drawn biar nimpa
    if lines_drawn > 0:
        print(f"\033[{lines_drawn}A", end="")

    prog = min(1.0, elapsed / duration)
    bar_len = 42
    filled = int(bar_len * prog)
    bar = "█" * filled + "░" * (bar_len - filled)

    hr = G + BOLD + "─" * 60 + RESET

    out = []
    out.append(G + BOLD + "┌" + "─" * 58 + "┐" + RESET)
    out.append(G + BOLD + "│" + RESET + f" {Y}TARGET    : {C}{target_host:<40}" + G + BOLD + "│" + RESET)
    out.append(G + BOLD + "│" + RESET + f" {Y}TARGET IP : {C}{target_ip:<40}" + G + BOLD + "│" + RESET)
    out.append(G + BOLD + "│" + RESET + f" {Y}MY IP     : {C}{my_ip:<40}" + G + BOLD + "│" + RESET)
    out.append(G + BOLD + "│" + RESET + f" {Y}REQUESTS  : {G}{counter:<40}" + G + BOLD + "│" + RESET)
    out.append(G + BOLD + "│" + RESET + f" {Y}ERRORS    : {R}{err:<40}" + G + BOLD + "│" + RESET)
    out.append(G + BOLD + "│" + RESET + f" {Y}TIME      : {G}{elapsed}/{duration}s{'':<33}" + G + BOLD + "│" + RESET)
    out.append(G + BOLD + "│" + RESET + f" {G}{bar}" + G + BOLD + "│" + RESET)
    out.append(G + BOLD + "└" + "─" * 58 + "┘" + RESET)

    for line in out:
        # clear line dulu biar rapi
        print("\033[2K" + line)

    return len(out)


# ============================================================
# LOOP VISUAL HACKER
# ============================================================
def hacker_screen(target_host, target_ip, my_ip, duration):
    flood = SelfFlood(threads=400, timeout=2)
    flood.start(my_ip)

    os.system("clear")
    print(HIDE_CURSOR, end="")

    # print header dulu 1x
    dash_lines = draw_dashboard(
        target_host, target_ip, my_ip, 0, 0, 0, duration, 0
    )
    print()
    print(G + BOLD + " " + "═" * 58 + RESET)
    print()

    log_buffer = []
    start = time.time()
    last_dash = time.time()

    try:
        while time.time() - start < duration:
            elapsed = int(time.time() - start)

            # tambah 1 log baru tiap iterasi
            log_buffer.append(rnd_log(target_ip))
            if len(log_buffer) > 30:
                log_buffer.pop(0)

            # full redraw tiap 0.05s
            os.system("clear")
            print(HIDE_CURSOR, end="")

            draw_dashboard(
                target_host, target_ip, my_ip,
                flood.counter, flood.err,
                elapsed, duration, 0,
            )
            print()
            print(G + BOLD + " " + "═" * 58 + RESET)
            print()

            for line in log_buffer:
                print(f"{DG}[{elapsed:>3}s]{RESET} {G}{line}{RESET}")

            time.sleep(0.05)

    except KeyboardInterrupt:
        print(SHOW_CURSOR, end="")
        print()
        print(R + "\n[!] STOPPED BY USER" + RESET)
    finally:
        flood.stop()
        print(SHOW_CURSOR, end="")

    print()
    print(G + "=" * 60 + RESET)
    print(G + BOLD + f"[+] TOTAL REQUEST : {flood.counter}" + RESET)
    print(G + BOLD + f"[+] TOTAL ERRORS  : {flood.err}" + RESET)
    print(G + BOLD + f"[+] TARGET        : {target_host} ({target_ip})" + RESET)
    print(G + BOLD + f"[+] STATUS        : COMPLETE" + RESET)
    print(G + "=" * 60 + RESET)
    print()
    print(Y + "[i] Semua request dikirim ke IP kamu sendiri." + RESET)
    print(Y + "    Koneksi HP jenuh -> web target lambat di HP kamu." + RESET)
    print(Y + "    Orang lain tetap normal. 6767." + RESET)


def main():
    os.system("clear")
    print(G + BOLD + BANNER + RESET)
    print(G + "#" * 60 + RESET)
    print(G + "< " + W + "[+] Author : " + C + "Bizz" + G + " >" + RESET)
    print(G + "< " + W + "[+] Tools  : " + C + "Bizz V3" + G + " >" + RESET)
    print(G + "< " + W + "[+] Mode   : " + C + "Hacker Screen" + G + " >" + RESET)
    print(G + "#" * 60 + RESET)
    print()

    target = input(f"{C}[?]{RESET} URL web target: ").strip()
    if not target:
        print(R + "[!] URL kosong." + RESET)
        return

    host, ip = resolve_ip(target)
    if not ip:
        print(R + "[!] Gagal resolve IP target." + RESET)
        return

    print(f"{G}[+]{RESET} Hostname : {C}{host}{RESET}")
    print(f"{G}[+]{RESET} Target IP: {C}{ip}{RESET}")

    my_ip = get_my_ip()
    if not my_ip:
        print(R + "[!] Gagal ambil IP publik sendiri." + RESET)
        return
    print(f"{G}[+]{RESET} Your IP  : {C}{my_ip}{RESET}")

    dur = input(f"\n{C}[?]{RESET} Duration detik (default 60): ").strip() or "60"

    print()
    print(Y + "[*] Memulai dalam 3 detik..." + RESET)
    time.sleep(3)

    hacker_screen(host, ip, my_ip, int(dur))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Y}[!]{RESET} Interrupted.")
