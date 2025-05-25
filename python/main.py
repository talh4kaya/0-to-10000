import dosyaOkuma as do
import zaman as z
import kisi as k
import time


def simulasyon():
    gezegenler = do.gezegen_dosyasi_oku("gezegenler.txt")
    araclar = do.uzayAraci_dosyasi_oku("araclar.txt")
    kisiler = do.kisi_dosyasi_oku("kisiler.txt")
    

    for arac in araclar:
        arac.varisTarihiHesaplayici(arac,gezegenler)
       
    while True:

        do.ekranaYazdirici(araclar, kisiler, gezegenler)

        for gezegen in gezegenler:
            gezegen.vakit.saatIlerlet()

        for kisi in kisiler:
            kisi.kisiGuncelle()  

        for arac in araclar:
            arac.uzayAraciGuncelle(arac,gezegenler)  
            arac.nufusKontrolu(araclar,kisiler,gezegenler)

           

        
        
        time.sleep(1)
      
simulasyon()
