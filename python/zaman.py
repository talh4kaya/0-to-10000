class Zaman:
    def __init__(self, gun, ay, yil, saat, gununKacSaatOldugu):
        self.gun = gun
        self.ay = ay
        self.yil = yil
        self.saat = saat
        self.gununKacSaatOldugu= gununKacSaatOldugu

    def saatIlerlet(self):
         self.saat += 1
         if self.saat >= self.gununKacSaatOldugu:
             self.saat = 0
             self.gun += 1
             if self.gun > 30: 
                    self.gun = 1
                    self.ay += 1
                    if self.ay > 12: 
                        self.ay = 1
                        self.yil += 1
