from zaman import Zaman
from gezegen import Gezegen
from kisi import Kisi
from uzayAraci import UzayAraci 
import os


def gezegen_dosyasi_oku(dosya_adi):
    gezegenler = []

    try:
        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            for satir in dosya:
                satir = satir.strip()
                if satir == "" or satir.startswith("#") or "Gezegen_Adi" in satir:
                    continue

                parcala = satir.split("#")
                if len(parcala) == 3:
                    adi, gununKacSaattenOlustugu, mevcutTarih = parcala

                    gununKacSaattenOlustugu=int(gununKacSaattenOlustugu)
                    gun, ay, yil = map(int, mevcutTarih.split("."))
                    saat = 0  
                    zaman = Zaman( gun=gun, ay=ay, yil=yil, saat=saat, gununKacSaatOldugu=gununKacSaattenOlustugu)

                    gezegen = Gezegen(adi, 0, vakit=zaman)
                    gezegenler.append(gezegen)

    except FileNotFoundError:
        print(f"Hata: {dosya_adi} bulunamadı!")

    return gezegenler

def uzayAraci_dosyasi_oku(dosya_adi):
    araclar = []

    try:
        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            for satir in dosya:
                satir = satir.strip()
                if satir == "" or satir.startswith("#"):
                    continue

                parcala = satir.split("#")
                if len(parcala) == 5:
                    adi,cikisGezegeni, varisGezegeni,cikisTarihi,mesefasiSaatOlarak = parcala

                    mesefasiSaatOlarak=int(mesefasiSaatOlarak)

                    arac=UzayAraci(uzayAraciAdi=adi, cikisGezegeni=cikisGezegeni, varisGezegeni=varisGezegeni, cikisTarihi=cikisTarihi,mesafeSaatOlarak=mesefasiSaatOlarak)
                    araclar.append(arac)

    except FileNotFoundError:
        print(f"Hata: {dosya_adi} bulunamadı!")

    return araclar

def kisi_dosyasi_oku(dosya_adi):
    kisiler = []

    try:
        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            for satir in dosya:
                satir = satir.strip()
                if satir == "" or satir.startswith("#"):
                    continue

                parcala = satir.split("#")
                if len(parcala) == 4:
                    adi,yas, kalanOmur,bulunduguUzayAraciAdi = parcala

                    yas=int(yas)
                    kalanOmur=int(kalanOmur)

                    kisi=Kisi(isim=adi,yas=yas,kalanOmur=kalanOmur,bulunduguUzayAraci=bulunduguUzayAraciAdi)
                    kisiler.append(kisi)

    except FileNotFoundError:
        print(f"Hata: {dosya_adi} bulunamadı!")

    return kisiler

def ekranaYazdirici(araclar, kisiler, gezegenler):
    import os
    os.system("cls" if os.name == "nt" else "clear")  

    print("Gezegenler:")

    for g in gezegenler:
        print(f"{g.gezegenAdi:22}", end="")  
    print()  


    for g in gezegenler:
        print(f"{g.vakit.gun}.{g.vakit.ay}.{g.vakit.yil:<17}", end="")
    print()


    for g in gezegenler:
        print(f"{g.nufus:<22}", end="")

    print("\n\nUzay Araçları:")
    print(f"{'Adı':<20} {'Durumu':<15} {'Nufusu':<15} {'Çıkış':<15} {'Varış':<15} {'Çıkış Tarihi':<20} {'Mesafe (saat)':<17} {'Varış Tarihi':<15}")
    for a in araclar:
           print(f"{a.uzayAraciAdi:<20} {a.vardiMi:<15} {a.nufus:<15} {a.cikisGezegeni:<15} {a.varisGezegeni:<15} {a.cikisTarihi:<20} {a.mesafeSaatOlarak:<17} {a.varisGunu}.{a.varisAyi}.{a.varisYili}")


    print("\nKişiler:")
    for k in kisiler:
        print(f"{k.isim:<10}  Yaş: {k.yas:<3}  Kalan Ömür: {k.kalanOmur:<5} Durumu: {k.durumu:<5} {k.bulunduguUzayAraci:<5}")
    print()
