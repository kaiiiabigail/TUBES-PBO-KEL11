class Dagangan:
    jumlah_barang = 0
    list_barang = []

    def __init__(self, nama, stok, harga):
        self.__nama = nama
        self.__stok = stok
        self.__harga = harga

        Dagangan.jumlah_barang += 1
        Dagangan.list_barang.append((self.__nama, self.__stok, self.__harga))

    def lihat_barang(self):
        print("Jumlah barang dagangan pada toko:", self.jumlah_barang, "buah")
        for idx, barang in enumerate(self.list_barang, start=1):
            nama, stok, harga = barang
            print(f"{idx}. {nama} seharga Rp {harga} (stok: {stok})")

    def __del__(self):
        Dagangan.jumlah_barang -= 1
        for barang in Dagangan.list_barang:
            if self.__nama in barang:
                Dagangan.list_barang.remove(barang)
                print(f"{self.__nama} dihapus dari toko!")
                break


# Contoh penggunaannya
Dagangan1 = Dagangan("Galon Aqua 19L", 32, 17000)
Dagangan2 = Dagangan("Gas LPG 5 kg", 22, 88000)
Dagangan3 = Dagangan("Beras Ramos 5 kg", 13, 68000)
Dagangan1.lihat_barang()

del Dagangan1
Dagangan2.lihat_barang()
