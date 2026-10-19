from xmlrpc.server import SimpleXMLRPCServer

stok_db = {
    "P001": 50,
    "P002": 30,
    "P999": 20
}

def cek_stok(kode_produk):
    return stok_db.get(kode_produk, 0)

def potong_stok(kode_produk, jumlah):
    stok_ada = stok_db.get(kode_produk, 0)
    if stok_ada >= jumlah:
        stok_db[kode_produk] -= jumlah
        return True, stok_db[kode_produk]
    return False, stok_ada

server = SimpleXMLRPCServer(("localhost", 8000))
print("[RPC Server] Layanan Stok siap berjalan di port 8000...")
server.register_function(cek_stok, "cek_stok")
server.register_function(potong_stok, "potong_stok")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n[RPC Server] Layanan dihentikan.")