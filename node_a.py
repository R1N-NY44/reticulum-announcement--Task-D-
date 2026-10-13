# ============================================================
# NODE A - Pengirim Announcement Reticulum
# ============================================================
# Script ini berfungsi sebagai node pengirim announcement
# ke Node B lewat jaringan Reticulum.
# Node A ini jalan sebagai TCP Client yang connect ke "node_b:4242".
# ============================================================

import os      # buat manipulasi path & environment variable
import time    # buat sleep / delay
import RNS     # library Reticulum Network Stack

# ------------------------------------------------------------
# Var GLOBAL
# ------------------------------------------------------------

# Nama aplikasi -> dipakai buat bikin destination
APP_NAME = "taskd"

# Aspek dari aplikasi -> digabung jadi "taskd.announcement"
ASPECT = "announcement"

# Pesan yang bakal dikirim lewat announcement
MESSAGE = "Hello from Node A!"

# Direktori config Reticulum
# Diambil dari env var RETICULUM_CONFIG, kalau gak ada default /reticulum
CONFIG_DIR = os.environ.get("RETICULUM_CONFIG", "/reticulum")


# ============================================================
# FUNGSI PREPARE_CONFIG
# ============================================================
# Fungsi ini nyiapin file config Reticulum buat Node A.
# Kalau file config belum ada -> dibuat baru.
# ============================================================

def prepare_config():

    # Bikin direktori config kalau belum ada
    # exist_ok=True -> gak error kalau direktori udah ada
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # Path file config Reticulum
    config_path = os.path.join(CONFIG_DIR, "config")

    # Kalau file config belum ada -> tulis config default
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as config:
            # Isi config:
            # [reticulum]
            #   enable_transport = No  -> node ini BUKAN transport node
            # [logging]
            #   loglevel = 4           -> level logging
            # [interfaces]
            #   TCPClientInterface     -> connect ke node_b:4242
            #   target_host = node_b   -> pakai nama container (docker DNS)
            #   target_port = 4242     -> port TCP Node B
            config.write(
                "[reticulum]\n"
                "enable_transport = No\n\n"
                "[logging]\n"
                "loglevel = 4\n\n"
                "[interfaces]\n"
                "  [[Docker TCP Client]]\n"
                "    type = TCPClientInterface\n"
                "    enabled = yes\n"
                "    target_host = node_b\n"
                "    target_port = 4242\n"
            )


# ============================================================
# FUNGSI MAIN
# ============================================================
# Fungsi utama buat setup config, init Reticulum, bikin identity,
# bikin destination, dan kirim announcement.
# ============================================================

def main():

    # Siapin file config dulu
    prepare_config()

    # Print status mulai
    print("[NODE A] Starting Reticulum...", flush=True)

    # Inisialisasi Reticulum pakai configdir yang udah disiapin
    # Setelah ini, TCP client interface bakal aktif connect ke Node B
    RNS.Reticulum(configdir=CONFIG_DIR)

    # Path file identity -> disimpen biar identity-nya konsisten
    # (destination hash Node A bakal sama tiap restart kalau identity-nya sama)
    identity_path = os.path.join(CONFIG_DIR, "identity")

    # Cek apakah file identity udah ada
    if os.path.exists(identity_path):
        # Load identity dari file
        identity = RNS.Identity.from_file(identity_path)

        # Kalau gagal load -> raise error
        if identity is None:
            raise RuntimeError("Could not load saved identity")
    else:
        # Bikin identity baru
        identity = RNS.Identity()

        # Simpen identity ke file
        # Kalau gagal simpen -> raise error
        if not identity.to_file(identity_path):
            raise RuntimeError("Could not save identity")

    # Bikin destination
    # Parameter:
    #   identity        -> identity Node A
    #   IN              -> arah destination (incoming, buat terima)
    #   SINGLE          -> tipe destination single (1 identity)
    #   APP_NAME        -> "taskd"
    #   ASPECT          -> "announcement"
    # Hasil akhirnya destination dengan aspek "taskd.announcement"
    destination = RNS.Destination(
        identity,
        RNS.Destination.IN,
        RNS.Destination.SINGLE,
        APP_NAME,
        ASPECT,
    )

    # Print status nunggu koneksi TCP ke Node B
    print("[NODE A] Waiting for TCP connection...", flush=True)

    # Kasih waktu 10 detik biar TCP client sempet konek ke Node B
    # (biar announcement-nya beneran nyampe, bukan dibuang duluan)
    time.sleep(10)

    # Print status mau ngirim announcement
    print("[NODE A] Sending announcement...", flush=True)

    # Kirim announcement
    # app_data diisi MESSAGE yang di-encode jadi bytes (utf-8)
    destination.announce(app_data=MESSAGE.encode("utf-8"))

    # Print status announcement udah disubmit
    print("[NODE A] Announcement submitted.", flush=True)

    # Tahan Reticulum instance sebentar biar packet-nya sempet kekirim
    # Ini cuma buat demo, jadi cuma 10 detik
    time.sleep(10)


# Entry point standar Python
# Cuma jalanin main() kalau script dieksekusi langsung (bukan di-import)
if __name__ == "__main__":
    main()