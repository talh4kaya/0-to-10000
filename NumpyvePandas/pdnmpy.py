import pandas as pd
import numpy as np

#1.kısım csv yi okudum ve tarihleri tarih formatına çevirdim ve boş varmı diye konrol ettim
df = pd.read_csv("satislar.csv")

print(df)      
print(df.isnull().sum())
df["Tarih"] = pd.to_datetime(df["Tarih"])
print()
print(df)


#2.kısım toplam diye sutun ekledim ve ortalama fiyatı buldum ve aylık satisi buldum
print()
df['Toplam']=df['Adet'] * df['Fiyat']
print(df)
print()
print(df['Toplam'].sum())

en_cok_satis=df.loc[df['Toplam'].idxmax(), 'Urun']
print("en cok satis yapan urun: ",en_cok_satis,"\n")

en_pahali_urun = df.loc[df['Fiyat'].idxmax(), 'Urun']
print("En pahalı ürün:", en_pahali_urun)

en_cok_satis_yapilan_sehir = df.groupby('Sehir')['Toplam'].sum().idxmax()
print("en çok satış yapılan şehir:",en_cok_satis_yapilan_sehir)

df['YılAy'] = df['Tarih'].dt.to_period('M')
df['YılAy'] = df['Tarih'].dt.strftime('%Y-%m')

aylik_toplam_satis = df.groupby('YılAy')['Toplam'].sum()
print(aylik_toplam_satis)

df['kategoriToplami'] = df.groupby('Kategori')['Toplam'].transform('sum')
df['ortFiyat'] = df.groupby('Kategori')['Fiyat'].transform('mean')
print(df)
print()

en_cok_satis_yapilan_gun=df.loc[df['Toplam'].idxmax(),'Tarih']
print("en .ok satis yapilan gun: ",en_cok_satis_yapilan_gun)


kategori_ozet = df.groupby('Kategori').agg(
    toplam_satis=('Toplam', 'sum'),
    ortalama_fiyat=('Fiyat', 'mean')
)
print(kategori_ozet)