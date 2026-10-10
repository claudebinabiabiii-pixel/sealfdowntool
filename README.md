# Bizz V3

### Tools self-loop flood dengan tampilan ala Dos-WIFI

Tools ini dibuat buat **prank / fun** — bikin website keliatan down
**cuma di HP kamu**, sementara user lain tetap bisa akses normal.

---

## Warning!!

- Tool ini support **Termux (Android)**, Ubuntu, Kali Linux, Parrot Security
- Butuh koneksi internet aktif
- Pakai **WiFi**, jangan data seluler

---

## Cara Penggunaan Tools

```bash
git clone https://github.com/claudebinabilii-pixel/sealfdowntool.git
cd sealfdowntool
pip install -r requirements.txt
python main.py
```

Lalu:
- Pilih interface WiFi
- Pilih menu `[1]` buat start flood
- `[2]` buat restore koneksi
- `[0]` buat keluar

---

## Screenshot Tools

```
  ____  _____ _______ ______
 |  _ \|_   _|__   __|___  /
 | |_) | | |    | |     / /
 |  _ <  | |    | |    / /
 | |_) |_| |_   | |   / /__
 |____/|_____|  |_|  /_____/

        >>  B I Z Z   V 3  <<

############################################################
< [+] Author  : Bizz >
< [+] Tools   : Bizz V3 >
< [+] Version : 3.0 >
< [+] GitHub  : Bizz >
############################################################

[*] Mendeteksi interface WiFi...

[0] - wlan1
[1] - wlan0

[?] Pilih interface (angka): _
```

---

## Konsep

1. HP kamu punya 1 IP publik dari ISP
2. Semua request keluar lewat IP itu
3. IP itu di-flood dari dalam → NAT/queue HP jenuh
4. Website target timeout **di HP kamu**
5. User lain (IP beda) tetap normal

Bukan DDoS. Cuma "self-sabotage" koneksi lokal. Fun.

---

## Disclaimer

Ini buat **fun / prank** doang. Nggak ngerusak website orang.
Yang kena cuma koneksi HP kamu sendiri, sementara.
