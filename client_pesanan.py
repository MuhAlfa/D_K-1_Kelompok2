import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

kode_produk = "P999"
jumlah_pesan = 5

print(f"[Client Pesanan] Memeriksa stok untuk {kode_produk}...")
stok_awal = proxy.cek_stok(kode_produk)
print(f"[Client Pesanan] Stok tersedia: {stok_awal}")

if stok_awal >= jumlah_pesan:
    berhasil, sisa_stok = proxy.potong_stok(kode_produk, jumlah_pesan)
    if berhasil:
        print(f"[Client Pesanan] Berhasil memesan {jumlah_pesan} unit {kode_produk}!")
        print(f"[Client Pesanan] Sisa stok di server sekarang: {sisa_stok}")
else:
    print(f"[Client Pesanan] Gagal: Stok {kode_produk} tidak mencukupi.")