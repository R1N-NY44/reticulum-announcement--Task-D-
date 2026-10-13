# ============================================================
# NODE B - Penerima Announcement Reticulum
# ============================================================
# Script ini berfungsi sebagai node penerima announcement
# dari node lain di jaringan Reticulum.
# Node B ini jalan sebagai TCP Server yang listen di port 4242.
# ============================================================

import os      # buat manipulasi path & environment variable
import time    # buat sleep di loop utama
import RNS     # library Reticulum Network Stack

# ------------------------------------------------------------
# Var GLOBAL
# ------------------------------------------------------------

# Nama aplikasi yang dipakai buat filter announcement
APP_NAME = "taskd"

# Aspek dari aplikasi -> nanti digabung jadi "taskd.announcement"
ASPECT = "announcement"

# Direktori config Reticulum
# Diambil dari env var RETICULUM_CONFIG, kalau gak ada pakai /reticulum
CONFIG_DIR = os.environ.get("RETICULUM_CONFIG", "/reticulum")


# ============================================================
# CLASS HANDLER ANNOUNCEMENT
# ============================================================
# Class ini dipakai buat handle announcement yang masuk.
# RNS.Transport butuh object yang punya:
#   1. attribute  : aspect_filter
#   2. method     : received_announce(...)
# ============================================================

class AnnouncementHandler:

    # Filter aspek -> cuma announcement dengan aspek ini yang diproses
    # Hasil konkatenasi: "taskd.announcement"
    aspect_filter = APP_NAME + "." + ASPECT

    def received_announce(
        self,
        destination_hash,           # hash destination si pengirim (bytes)
        announced_identity,         # object identity si pengirim
        app_data,                   # payload data yang dikirim (bytes / None)
        announce_packet_hash=None,  # hash packet announce (optional)
        is_path_response=False,     # flag kalau ini path response (optional)
    ):
        # Method ini otomatis dipanggil tiap ada announcement masuk
        # yang cocok sama aspect_filter di atas.

        # Print header penanda announcement diterima
        # flush=True -> biar langsung keluar di stdout, gak ketahan buffer
        print("\n[ANNOUNCEMENT RECEIVED]", flush=True)

        # Tampilkan destination hash dalam bentuk hex string
        print("Destination:", destination_hash.hex(), flush=True)

        # Cek apakah ada payload data
        if app_data:
            # Decode bytes -> string
            # Kalau ada byte invalid, ganti pakai karakter replacement
            print(
                "Message:",
                app_data.decode("utf-8", errors="replace"),
                flush=True,
            )
        else:
            # Kalau gak ada data sama sekali, kasih keterangan
            print("Message: (no application data)", flush=True)


# ============================================================
# FUNGSI MAIN
# ============================================================
# Fungsi utama buat setup config, init Reticulum, dan jalanin loop.
# ============================================================

def main():

    # Bikin direktori config kalau belum ada
    # exist_ok=True -> gak error kalau direktori udah ada
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # Path file config Reticulum
    config_path = os.path.join(CONFIG_DIR, "config")

    # Kalau file config belum ada -> bikin baru pakai config default
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as config:
            # Isi config:
            # [reticulum]
            #   enable_transport = No  -> node ini BUKAN transport node
            # [logging]
            #   loglevel = 4           -> level logging (0-7, makin gede makin verbose)
            # [interfaces]
            #   TCPServerInterface     -> listen TCP di 0.0.0.0:4242
            config.write(
                "[reticulum]\n"
                "enable_transport = No\n\n"
                "[logging]\n"
                "loglevel = 4\n\n"
                "[interfaces]\n"
                "  [[Docker TCP Server]]\n"
                "    type = TCPServerInterface\n"
                "    enabled = yes\n"
                "    listen_ip = 0.0.0.0\n"
                "    listen_port = 4242\n"
            )

    # Print status mulai
    print("[NODE B] Starting Reticulum...", flush=True)

    # Inisialisasi Reticulum pakai configdir yang udah disiapin
    # Setelah ini, interface TCP server bakal aktif
    RNS.Reticulum(configdir=CONFIG_DIR)

    # Bikin instance handler announcement
    handler = AnnouncementHandler()

    # Daftarin handler ke Transport Reticulum
    # Setelah ini, tiap announcement masuk yang cocok filter
    # bakal otomatis diteruskan ke handler.received_announce()
    RNS.Transport.register_announce_handler(handler)

    # Print status listening
    print("[NODE B] Listening on TCP port 4242...", flush=True)

    try:
        # Loop utama: cuma sleep 1 detik terus-menerus
        # Program tetap hidup -> thread internal RNS yang handle network I/O
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Handle Ctrl+C biar keluar dengan rapi
        print("[NODE B] Stopped.", flush=True)


# Entry point standar Python
# Cuma jalanin main() kalau script dieksekusi langsung (bukan di-import)
if __name__ == "__main__":
    main()