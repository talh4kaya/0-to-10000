import pandas as pd
import numpy as np



df = pd.read_csv("musteri.csv")
print(df)
print()
print(df.isnull().sum())
df["AlisTarihi"] = pd.to_datetime(df["AlisTarihi"])

mapping = {'Erkek': 0, 'Kadın': 1}
#df['cinsiyet_kodu'] = df['Cinsiyet'].map(mapping)


# 1. Eksik değerleri doldur veya sil
df = df.dropna()  

# 3. Cinsiyeti sayısal değere çevir (Erkek=0, Kadın=1)
df['Cinsiyet_kodu'] = df['Cinsiyet'].map({'Erkek': 0, 'Kadın': 1})

# 4. Şehri kategorik kodlara dönüştür
df['Sehir_kodu'] = df['Sehir'].astype('category').cat.codes

X = df['AylikGelir']
Y = df['SatisAdedi']
x_mean = X.mean()
y_mean = Y.mean()

# Eğim (b1) ve kesişim (b0) hesapla
b1 = ((X - x_mean) * (Y - y_mean)).sum() / ((X - x_mean)**2).sum()
b0 = y_mean - b1 * x_mean

# Regresyon denklemi:
print(f"Regresyon denklemi: SatisAdedi = {b0:.2f} + {b1:.2f} * AylikGelir")

# Tahmin sütunu ekle
df['Tahmin'] = b0 + b1 * X

# İlk 5 satırı göster
print(df[['AylikGelir', 'SatisAdedi', 'Tahmin']].head())

print(df)



