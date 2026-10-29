#!/usr/bin/env python3
"""K-3 Sistem Operasi Kelas D - Algoritma Banker untuk checkout Toko Online UMKM.

Sumber daya (jenis):
  A = Lock tabel stok        (pool slot akses tabel produk, total 10)
  B = Lock transaksi bayar   (sesi verifikasi pembayaran, total 5)
  C = Slot kurir             (slot pengiriman, total 7)
Proses P0..P4 = lima transaksi checkout yang berjalan bersamaan.

CATATAN: matriks di bawah adalah CONTOH. Ganti ALLOCATION, MAX, dan TOTAL dengan
matriks khusus kelas dari dosen, lalu jalankan ulang:  python3 banker.py
"""
NAMA_R = ["A (stok)", "B (bayar)", "C (kurir)"]
PROSES = ["P0", "P1", "P2", "P3", "P4"]
ALLOCATION = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
MAX        = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
TOTAL      = [10, 5, 7]


def hitung_need(maks, alok):
    return [[m - a for m, a in zip(rm, ra)] for rm, ra in zip(maks, alok)]


def available(total, alok):
    return [t - sum(r[j] for r in alok) for j, t in enumerate(total)]


def kurang(a, b):  # a <= b ?
    return all(x <= y for x, y in zip(a, b))


def cek_safe(alok, need, avail, verbose=True):
    """Algoritma keamanan (safety). Mengembalikan (aman, urutan_aman)."""
    n = len(alok)
    work, finish, urutan = avail[:], [False] * n, []
    langkah = 1
    while len(urutan) < n:
        ditemukan = False
        for i in range(n):
            if not finish[i] and kurang(need[i], work):
                if verbose:
                    print(f"  Langkah {langkah}: {PROSES[i]} Need={need[i]} <= Work={work} -> bisa selesai")
                work = [w + a for w, a in zip(work, alok[i])]
                if verbose:
                    print(f"            {PROSES[i]} melepas {alok[i]} -> Work={work}")
                finish[i] = True
                urutan.append(PROSES[i])
                ditemukan = True
                langkah += 1
        if not ditemukan:
            break
    return len(urutan) == n, urutan


def minta(i, req, alok, need, avail):
    """Resource-request algorithm: apakah permintaan req dari proses i boleh dikabulkan?"""
    print(f"\n>> {PROSES[i]} meminta {req}")
    if not kurang(req, need[i]):
        print("   DITOLAK: melebihi Need (proses melanggar klaim maksimum)")
        return False
    if not kurang(req, avail):
        print(f"   DITUNDA: Request {req} > Available {avail} (sumber daya belum tersedia)")
        return False
    a2 = [r[:] for r in alok]; n2 = [r[:] for r in need]
    av2 = [x - y for x, y in zip(avail, req)]
    a2[i] = [x + y for x, y in zip(a2[i], req)]
    n2[i] = [x - y for x, y in zip(n2[i], req)]
    print(f"   Simulasi alokasi -> Available={av2}, Need {PROSES[i]}={n2[i]}")
    aman, urut = cek_safe(a2, n2, av2)
    if aman:
        print(f"   DIKABULKAN: state tetap aman, urutan {' -> '.join(urut)}")
    else:
        print("   DITOLAK: state hasil alokasi TIDAK aman (berpotensi deadlock)")
    return aman


def tabel(judul, m):
    print(f"\n{judul}")
    print("      " + "  ".join(f"{h:<9}" for h in NAMA_R))
    for p, r in zip(PROSES, m):
        print(f"  {p}  " + "  ".join(f"{x:<9}" for x in r))


if __name__ == "__main__":
    need = hitung_need(MAX, ALLOCATION)
    avail = available(TOTAL, ALLOCATION)
    print("=== ALGORITMA BANKER - CHECKOUT TOKO UMKM ===")
    print("Total sumber daya:", dict(zip(NAMA_R, TOTAL)))
    tabel("Allocation", ALLOCATION); tabel("Max", MAX); tabel("Need = Max - Allocation", need)
    print("\nAvailable = Total - sum(Allocation) =", avail)
    print("\n--- Algoritma keamanan (safety) ---")
    aman, urut = cek_safe(ALLOCATION, need, avail)
    print(f"\nHASIL: state {'AMAN' if aman else 'TIDAK AMAN'}", ("| urutan aman: " + " -> ".join(urut)) if aman else "")
    print("\n--- Uji permintaan baru (resource-request) ---")
    minta(1, [1, 0, 2], ALLOCATION, need, avail)
    minta(4, [3, 3, 0], ALLOCATION, need, avail)
    minta(0, [0, 2, 0], ALLOCATION, need, avail)