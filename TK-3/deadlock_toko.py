#!/usr/bin/env python3
"""K-3 Sistem Operasi Kelas D - Simulasi deadlock checkout Toko Online UMKM.

Meniru pola api.py (STOK_LOCK di /api/checkout) dengan dua lock tambahan:
  LOCK_STOK   : lock tabel stok              (cek_stok / potong stok)
  LOCK_BAYAR  : lock transaksi pembayaran    (verifikasi pembayaran)
  LOCK_KURIR  : slot kurir                   (jadwal pengiriman)

Tiga alur memegang lock dengan urutan berbeda -> menunggu melingkar (deadlock):
  T1 checkout     : stok  -> bayar
  T2 pembayaran   : bayar -> kurir
  T3 jadwal kurir : kurir -> stok

Pemakaian:
  python3 deadlock_toko.py macet     # tanpa pencegahan (dideteksi lewat timeout)
  python3 deadlock_toko.py aman      # dengan lock ordering stok -> bayar -> kurir
  python3 deadlock_toko.py trylock   # dengan acquire timeout + rollback + retry
"""
import sys
import threading
import time

LOCK_STOK, LOCK_BAYAR, LOCK_KURIR = threading.Lock(), threading.Lock(), threading.Lock()
NAMA = {id(LOCK_STOK): "stok", id(LOCK_BAYAR): "bayar", id(LOCK_KURIR): "kurir"}
ALUR = {"T1-checkout": (LOCK_STOK, LOCK_BAYAR),
        "T2-pembayaran": (LOCK_BAYAR, LOCK_KURIR),
        "T3-jadwal-kurir": (LOCK_KURIR, LOCK_STOK)}
sudah_pegang = threading.Barrier(3)
sudah_timeout = threading.Barrier(3)
hasil = {}
t0 = time.time()


def log(nama, pesan):
    print(f"[{time.time() - t0:5.2f}s] {nama:<16} {pesan}", flush=True)


def alur_macet(nama, pertama, kedua):
    pertama.acquire(); log(nama, f"memegang lock {NAMA[id(pertama)]}")
    sudah_pegang.wait()
    log(nama, f"menunggu lock {NAMA[id(kedua)]} ...")
    if kedua.acquire(timeout=2):              # timeout hanya untuk deteksi bukan pencegahan
        log(nama, "berhasil (tidak deadlock)"); hasil[nama] = "selesai"; kedua.release()
    else:
        log(nama, f"TIMEOUT 2 detik -> terindikasi DEADLOCK (menunggu {NAMA[id(kedua)]})"); hasil[nama] = "DEADLOCK"
    sudah_timeout.wait()                      # tahanlock pertama sampai ketiganya selesai menunggu
    pertama.release()


def alur_urut(nama, pertama, kedua):
    a, b = sorted((pertama, kedua), key=lambda l: [LOCK_STOK, LOCK_BAYAR, LOCK_KURIR].index(l))
    with a:
        log(nama, f"memegang lock {NAMA[id(a)]}"); time.sleep(0.2)
        with b:
            log(nama, f"memegang lock {NAMA[id(b)]} -> proses selesai"); hasil[nama] = "selesai"


def alur_trylock(nama, pertama, kedua):
    for percobaan in range(1, 6):
        pertama.acquire()
        log(nama, f"percobaan {percobaan}: memegang {NAMA[id(pertama)]}"); time.sleep(0.2)
        if kedua.acquire(timeout=0.5):
            log(nama, f"memegang {NAMA[id(kedua)]} -> selesai"); hasil[nama] = f"selesai (percobaan {percobaan})"
            kedua.release(); pertama.release(); return
        log(nama, f"gagal dapat {NAMA[id(kedua)]} -> lepas {NAMA[id(pertama)]} (rollback), coba lagi")
        pertama.release()
        time.sleep(0.1 * (hash(nama) % 7 + 1))  #backoff acak agar tidak bentrok
    hasil[nama] = "menyerah"


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "macet"
    fungsi = {"macet": alur_macet, "aman": alur_urut, "trylock": alur_trylock}[mode]
    print(f"=== Mode: {mode} ===")
    ts = [threading.Thread(target=fungsi, args=(n, *k), name=n) for n, k in ALUR.items()]
    [t.start() for t in ts]; [t.join() for t in ts]
    print("\nRingkasan:", hasil)