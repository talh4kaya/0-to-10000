class Kisi:

    def __init__(self,isim,yas,kalanOmur,bulunduguUzayAraci):
        self.isim=isim
        self.yas=yas
        self.kalanOmur=kalanOmur
        self.bulunduguUzayAraci=bulunduguUzayAraci
        self.durumu = "canlı"
    

    def kisiGuncelle(self):
        if self.durumu=="canlı":
            self.kalanOmur -= 1
        if self.kalanOmur <= 0:
            self.durumu = "ölü"
        