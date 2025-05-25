class UzayAraci:

    def __init__(self, uzayAraciAdi, cikisGezegeni, varisGezegeni, cikisTarihi, mesafeSaatOlarak):
        self.uzayAraciAdi = uzayAraciAdi
        self.cikisGezegeni = cikisGezegeni
        self.varisGezegeni = varisGezegeni
        self.cikisTarihi = cikisTarihi
        self.mesafeSaatOlarak = mesafeSaatOlarak
        self.vardiMi="BEKLİYOR"
        self.varisGunu=0
        self.varisAyi=0
        self.varisYili=0
        self.nufus=0

    @staticmethod
    def uzayAraciGuncelle(arac, gezegenler):
        cikisGezegenibulunan = next((g for g in gezegenler if g.gezegenAdi == arac.cikisGezegeni), None)

        cgun, cay, cyil = map(int, arac.cikisTarihi.split("."))
        geGun = cikisGezegenibulunan.vakit.gun
        geAy = cikisGezegenibulunan.vakit.ay
        geYil = cikisGezegenibulunan.vakit.yil

  
        if (cgun == geGun and cay == geAy and cyil == geYil) or arac.vardiMi == "YOLDA":
            arac.vardiMi = "YOLDA"
            arac.mesafeSaatOlarak -= 1


        if arac.mesafeSaatOlarak == 0 and arac.vardiMi == "YOLDA":
            arac.varisGezegeni = ""
            arac.vardiMi = "VARDI"
    
    @staticmethod
    def varisTarihiHesaplayici(arac, gezegenler):
        
        cikisGezegeni = next((g for g in gezegenler if g.gezegenAdi == arac.cikisGezegeni), None)
        varisGezegeni = next((g for g in gezegenler if g.gezegenAdi == arac.varisGezegeni), None)
      
        cgun, cay, cyil = map(int, arac.cikisTarihi.split("."))
  
        suAnGun = cikisGezegeni.vakit.gun
        suAnAy = cikisGezegeni.vakit.ay
        suAnYil = cikisGezegeni.vakit.yil

        if(cyil, cay, cgun) < (suAnYil, suAnAy, suAnGun):
                arac.varisGunu = ""
                arac.varisAyi = ""
                arac.varisYili = ""
                
        else:  
                farkGun = (cgun - suAnGun) + (cay - suAnAy) * 30 + (cyil - suAnYil) * 360
                beklemeSaat = farkGun * cikisGezegeni.vakit.gununKacSaatOldugu

            
                toplamSaat = beklemeSaat + arac.mesafeSaatOlarak

            
                gunlukSaat = varisGezegeni.vakit.gununKacSaatOldugu
                toplamGun = toplamSaat // gunlukSaat
                eklenecekSaat = toplamSaat % gunlukSaat

                toplamAy = toplamGun // 30
                eklenecekGun = toplamGun % 30

                toplamYil = toplamAy // 12
                eklenecekAy = toplamAy % 12

                varisGunu = varisGezegeni.vakit.gun + eklenecekGun
                varisAyi = varisGezegeni.vakit.ay + eklenecekAy
                varisYili = varisGezegeni.vakit.yil + toplamYil

            
                if varisGunu > 30:
                    varisGunu -= 30
                    varisAyi += 1
                if varisAyi > 12:
                    varisAyi -= 12
                    varisYili += 1

                arac.varisGunu = varisGunu
                arac.varisAyi = varisAyi
                arac.varisYili = varisYili

    def nufusKontrolu(self, araclar, kisiler, gezegenler):
        # Her tur başında tüm araç ve gezegen nüfuslarını sıfırla
        for arac in araclar:
            arac.nufus = 0
        for gezegen in gezegenler:
            gezegen.nufus = 0

        # 1. Her kişiyi yalnızca bulunduğu uzay aracına say
        for insan in kisiler:
            bagli_arac = next((a for a in araclar if a.uzayAraciAdi == insan.bulunduguUzayAraci), None)
            if bagli_arac and insan.durumu=="canlı":
                bagli_arac.nufus += 1

        # 2. Araç hangi durumdaysa ona göre gezegenin nüfusunu artır
        for arac in araclar:
            if arac.vardiMi == "BEKLİYOR":
                # Hâlâ çıkış gezegenindeyse, çıkış gezegenine bu aracı ve içindekileri say
                cikisGezegeni = next((g for g in gezegenler if g.gezegenAdi == arac.cikisGezegeni), None)
                if cikisGezegeni:
                    cikisGezegeni.nufus += arac.nufus

            elif arac.vardiMi == "VARDI":
                # Vardıysa varış gezegenine bu aracın içindekileri say
                varisGezegeni = next((g for g in gezegenler if g.gezegenAdi == arac.varisGezegeni), None)
                if varisGezegeni:
                    varisGezegeni.nufus += arac.nufus
            
            elif arac.vardiMi == "YOLDA":
                # Vardıysa varış gezegenine bu aracın içindekileri say
                varisGezegeni = next((g for g in gezegenler if g.gezegenAdi == arac.varisGezegeni), None)
                if varisGezegeni:
                    varisGezegeni.nufus -= arac.nufus


           

                
