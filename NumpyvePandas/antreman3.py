import pandas as pd

df = pd.read_csv("antreman3.csv")

print(df)

print()
print(df.isnull().sum())
df_unique_date = df.drop_duplicates(subset=['Tarih'])
df.dropna()

df["Tarih"] = pd.to_datetime(df["Tarih"])
print(df)

print()
df["BolgeKoduM"]= df["Bolge"].map({'Kuzey':1,'guney':0})
print(df)

print()
df["BolgeKoduC"]= df["Bolge"].astype('category').cat.codes
print(df)

df['Urun Basi Kar'] = (df['Gelir'] - df['Reklam_Harcamasi']) / df['Satilan_Urun_Adedi']
print()
print(df)

ortalamaUrun = df['Satilan_Urun_Adedi'].mean()
maxmimumSatis = df.loc[df['Gelir'].idxmax(),'Tarih']
minimumSatis = df.loc[df['Gelir'].idxmin(),'Tarih']
medyan_degeri = df['Gelir'].median()
ortalmaSatis = df['Gelir'].mean()

print(f"Ortalama Ürün Adedi: {ortalamaUrun}\nMaksimum Satış Tarihi: {maxmimumSatis}\nMinimum Satış Tarihi: {minimumSatis}\nMedyan Gelir: {medyan_degeri}\nOrtalama Gelir: {ortalmaSatis}")


korelasyon = df['Reklam_Harcamasi'].corr(df['Gelir'])
print()
print(f"kroelasyon degeri: {korelasyon}")

#burda yapılan şu tarihlerden 2 tane var mesela hangi tarihde daha fazla satış yapılmış onu buluyor topluyor o tarihdekileri 
print()
en_cok_satis_yapilan_tarih = df.groupby('Tarih')['Satilan_Urun_Adedi'].sum().idxmax()
print("en çok satış yapılan tarih:",en_cok_satis_yapilan_tarih)

en_satis_yapilan_ay = df_unique_date.loc[df_unique_date['Satilan_Urun_Adedi'].idxmax(),'Tarih']
print()
print(f"en çok satış yapılan ay: {en_satis_yapilan_ay}")


X = df['Reklam_Harcamasi']
Y = df['Satilan_Urun_Adedi']
x_mean = X.mean()
y_mean = Y.mean()

# Eğim (b1) ve kesişim (b0) hesapla
b1 = ((X - x_mean) * (Y - y_mean)).sum() / ((X - x_mean)**2).sum()
b0 = y_mean - b1 * x_mean

df['Tahmin'] = b0 + b1 * X

print()
print(df)