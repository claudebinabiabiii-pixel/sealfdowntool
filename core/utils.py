"""
Bizz V3 — utils
Banner, watermark, deteksi interface, warna, get public IP.
"""

import subprocess
import requests


RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
RESET   = "\033[0m"
BOLD    = "\033[1m"


BANNER_ART = r"""
  ____  _____ _______ ______
 |  _ \|_   _|__   __|___  /
 | |_) | | |    | |     / /
 |  _ <  | |    | |    / /
 | |_) |_| |_   | |   / /__
 |____/|_____|  |_|  /_____/

        >>  B I Z Z   V 3  <<
"""


LINUX_WM = r"""
    ██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗
    ██║     ██║████╗  ██║██║   ██║╚██╗██╔╝
    ██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝
    ██║     ██║██║╚██╗██║██║   ██║ ██╔██╗
    ███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗
    ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝
"""


def show_banner():
    print(RED + BOLD + BANNER_ART + RESET)
    print(RED + "#" * 60 + RESET)
    print(RED + "< " + GREEN + "[+] " + WHITE + "Author  : " + CYAN + "Bizz"    + RED + " >" + RESET)
    print(RED + "< " + GREEN + "[+] " + WHITE + "Tools   : " + CYAN + "Bizz V3" + RED + " >" + RESET)
    print(RED + "< " + GREEN + "[+] " + WHITE + "Version : " + CYAN + "3.0"     + RED + " >" + RESET)
    print(RED + "< " + GREEN + "[+] " + WHITE + "GitHub  : " + CYAN + "Bizz"    + RED + " >" + RESET)
    print(RED + "#" * 60 + RESET)
    print()


def show_linux_watermark():
    print(RED + LINUX_WM + RESET)


def detect_interfaces():
    interfaces = []

    try:
        out = subprocess.check_output(
            ["iw", "dev"], stderr=subprocess.DEVNULL
        ).decode(errors="ignore")
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("Interface"):
                interfaces.append(line.split()[-1])
    except Exception:
        pass

    if not interfaces:
        try:
            out = subprocess.check_output(
                ["ip", "-o", "link", "show"], stderr=subprocess.DEVNULL
            ).decode(errors="ignore")
            for line in out.splitlines():
                parts = line.split(":")
                if len(parts) >= 2:
                    name = parts[1].strip()
                    if name.startswith(("wl", "wlan", "wlp", "wlo")):
                        interfaces.append(name)
        except Exception:
            pass

    if not interfaces:
        interfaces = ["wlan1", "wlan0"]

    return interfaces


def show_interface_menu(interfaces):
    print(YELLOW + "[*] " + WHITE + "Mendeteksi interface WiFi..." + RESET)
    print()
    for idx, iface in enumerate(interfaces):
        print(YELLOW + f"[{idx}] " + WHITE + f"- {iface}" + RESET)
    print()


def prompt_interface(interfaces):
    while True:
        try:
            choice = input(CYAN + "[?] " + WHITE + "Pilih interface (angka): " + RESET)
            idx = int(choice.strip())
            if 0 <= idx < len(interfaces):
                return interfaces[idx]
            print(RED + "[!] Pilihan tidak valid." + RESET)
        except (ValueError, KeyboardInterrupt):
            print(RED + "\n[!] Dibatalkan." + RESET)
            raise SystemExit(0)


def show_main_menu():
    print(CYAN + "=" * 60 + RESET)
    print(WHITE + BOLD + "         BIZZ V3 — MAIN MENU" + RESET)
    print(CYAN + "=" * 60 + RESET)
    print(GREEN + "[1]" + WHITE + " Start Self-Flood (prank mode)" + RESET)
    print(GREEN + "[2]" + WHITE + " Restore koneksi" + RESET)
    print(GREEN + "[3]" + WHITE + " Ubah config" + RESET)
    print(GREEN + "[0]" + WHITE + " Keluar" + RESET)
    print(CYAN + "=" * 60 + RESET)
    print()


def get_public_ip():
    endpoints = [
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
        "https://icanhazip.com",
    ]
    for url in endpoints:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200 and r.text.strip():
                return r.text.strip()
        except Exception:
            continue
    return None
