class Hewan:
    def __init__(self, nama, jenis_kelamin):
        self.nama = nama
        self.jenis_kelamin = jenis_kelamin

    def bersuara(self):
        print(f"{self.__class__.__name__} {self.nama} bersuara: " + self.suara)

    def makan(self):
        print(f"{self.__class__.__name__} {self.nama} sedang makan: " + self.makanan)

    def minum(self):
        print(f"{self.__class__.__name__} {self.nama} sedang minum: " + self.minuman)

class Kucing(Hewan):
    suara = "Meong!"
    makanan = "tulang"
    minuman = "susu"

class Anjing(Hewan):
    suara = "Guk Guk!"
    makanan = "tulang"
    minuman = "air"

hewan1 = Kucing("Mero", "Jantan")
hewan2 = Anjing("Ochi", "Betina")
print(hewan1.nama) 
print(hewan2.nama) 
hewan1.bersuara() 
hewan1.makan() 
hewan2.bersuara() 
hewan2.makan() 