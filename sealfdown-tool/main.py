#!/usr/bin/env python3
"""
Bizz V3 — Self-Loop Flood Prank Tool
Desain ala Dos-WIFI, jalan di Termux.
"""

import json
import os
import sys
from pathlib import Path

from core.utils import (
    show_banner,
    show_linux_watermark,
    detect_interfaces,
    show_interface_menu,
    prompt_interface,
    show_main_menu,
)
from core.flood import SelfFlood


CONFIG_PATH = Path(__file__).parent / "config.json"


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def main():
    clear()
    show_banner()

    interfaces = detect_interfaces()
    show_interface_menu(interfaces)
    chosen = prompt_interface(interfaces)

    print()
    print(f"\033[92m[+]\033[0m Interface dipilih: \033[96m{chosen}\033[0m")
    print()
    input("\033[93m[?]\033[0m Tekan ENTER buat lanjut ke menu utama...")
    clear()

    show_banner()
    show_linux_watermark()

    cfg = load_config()
    flood = SelfFlood(
        target_url=cfg["target_url"],
        threads=int(cfg["threads"]),
        timeout=int(cfg["timeout"]),
    )

    while True:
        show_main_menu()
        try:
            choice = input("\033[96m[?]\033[0m Pilih menu: ").strip()
        except KeyboardInterrupt:
            print("\n\033[93m[!]\033[0m Keluar...")
            sys.exit(0)

        if choice == "1":
            print()
            flood.start(duration=int(cfg["duration"]))
        elif choice == "2":
            flood.restore()
        elif choice == "3":
            print("\n\033[93m[*]\033[0m Edit manual: nano config.json\033[0m")
        elif choice == "0":
            print("\033[93m[!]\033[0m Sampai jumpa, gng. 6767.\033[0m")
            sys.exit(0)
        else:
            print("\033[91m[!]\033[0m Pilihan tidak valid.\033[0m")

        print()
        input("\033[93m[?]\033[0m ENTER buat lanjut...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[93m[!]\033[0m Interrupted.\033[0m")
