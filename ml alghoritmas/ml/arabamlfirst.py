# --- GEREKLİ KÜTÜPHANELER ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Programın tamamını hata yönetimi için try-except bloğuna alalım
try:
    # --- VERİ SETİNİ YÜKLEME ---
    # CSV dosyasını latin-1 kodlaması ile okuyoruz. Dosya adının doğru olduğundan emin olun.
    df = pd.read_csv("araba.csv", encoding='latin-1')
    print("Veri seti başarıyla yüklendi.")
    print("-" * 50)

    # --- ADIM A: KOLON İSİMLERİNİ DÜZELTME ---
    print("\n--- Adım A: Kolon İsimleri Düzeltiliyor ---")
    # DataFrame'de 11 kolon olduğu için 11 tane yeni ve anlaşılır isim veriyoruz.
    df.columns = [
        'marka', 'model', 'motor_tipi_ham', 'motor_hacmi_ham', 'beygir_gucu', 'maks_hiz',
        'hizlanma_0_100', 'fiyat', 'yakit_turu', 'koltuk_sayisi', 'tork'
    ]
    print("Yeni kolon isimleri:", df.columns.to_list())
    print("-" * 50)

    # --- ADIM B: SAYISAL PERFORMANS KOLONLARINI TEMİZLEME ---
    print("\n--- Adım B: Performans Kolonları Temizleniyor ---")
    
    # Bu fonksiyon, metin içeren sayısal değerleri temizler ve aralıkları ortalamaya çevirir.
    def ortalama_hesapla_ve_temizle(deger, birim):
        # Önce birim ifadelerini (hp, Nm, km/h, sec vb.) temizle
        deger = str(deger).replace(birim, '').strip()
        # Aralık varsa ('100-120' gibi) ortalamasını al
        if '-' in deger:
            parcalar = deger.split('-')
            # Parçaların sayısal olup olmadığını kontrol et
            if parcalar[0].strip().replace('.', '', 1).isdigit() and parcalar[1].strip().replace('.', '', 1).isdigit():
                return (float(parcalar[0].strip()) + float(parcalar[1].strip())) / 2
            else:
                return np.nan # Aralıkta sayısal olmayan değer varsa NaN ata
        # Değerin sayısal olup olmadığını kontrol et
        if deger.replace('.', '', 1).isdigit():
            return float(deger)
        return np.nan # Hiçbiri değilse NaN ata

    # Fonksiyonları ilgili kolonlara uygula
    df['beygir_gucu'] = df['beygir_gucu'].apply(lambda x: ortalama_hesapla_ve_temizle(x, 'hp'))
    df['maks_hiz'] = df['maks_hiz'].apply(lambda x: ortalama_hesapla_ve_temizle(x, 'km/h'))
    df['hizlanma_0_100'] = df['hizlanma_0_100'].apply(lambda x: ortalama_hesapla_ve_temizle(x, 'sec'))
    df['tork'] = df['tork'].apply(lambda x: ortalama_hesapla_ve_temizle(x, 'Nm'))
    print("Performans kolonları (Beygir, Hız, Hızlanma, Tork) başarıyla sayısal hale getirildi.")
    print("-" * 50)
    
    # --- ADIM C: FİYAT KOLONUNU TEMİZLEME ---
    print("\n--- Adım C: Fiyat Kolonu Temizleniyor ---")
    # Fiyat kolonundaki '$' ve ',' işaretlerini kaldır ve sayısal formata çevir.
    df['fiyat'] = df['fiyat'].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
    df['fiyat'] = df['fiyat'].apply(lambda x: ortalama_hesapla_ve_temizle(x, ''))
    print("Fiyat kolonu başarıyla sayısal hale getirildi.")
    print("-" * 50)

    # --- ADIM D: MOTOR BİLGİSİ KOLONLARINI DÜZENLEME ---
    print("\n--- Adım D: Motor Bilgisi Kolonları Düzenleniyor ---")
    
    # 'motor_hacmi_ham' kolonundaki 'cc' ifadesini kaldırıp sayıya çeviriyoruz.
    df['motor_hacmi_cc'] = df['motor_hacmi_ham'].str.replace('cc', '', regex=False).str.strip()
    # Sayıya çevirirken hata oluşursa (örn: boş değer), o değeri NaN olarak ata
    df['motor_hacmi_cc'] = pd.to_numeric(df['motor_hacmi_cc'], errors='coerce')

    # 'motor_tipi_ham' kolonunun adını 'motor_tipi' olarak değiştiriyoruz.
    df['motor_tipi'] = df['motor_tipi_ham'].str.strip()
    
    # Artık gereksiz olan ham (raw) kolonları siliyoruz.
    df.drop(['motor_tipi_ham', 'motor_hacmi_ham'], axis=1, inplace=True)
    print("Motor bilgisi kolonları son haline getirildi.")
    print("-" * 50)
    
     # --- ADIM D-EK: ÖZEL DEĞERLERİ DÜZENLEME (YENİ EKLENEN BÖLÜM) ---
    print("\n--- Adım D-Ek: Özel Değerler Düzenleniyor ---")
    
    # 'koltuk_sayisi' kolonundaki '2+2' gibi metinleri sayısal anlama gelecek şekilde değiştiriyoruz.
    # .replace() metodu ile '2+2' gördüğümüz yeri '4' ile değiştiriyoruz.
    if 'koltuk_sayisi' in df.columns:
        original_dtype = df['koltuk_sayisi'].dtype
        print(f"'koltuk_sayisi' kolonu '2+2' değerleri için kontrol ediliyor...")
        df['koltuk_sayisi'] = df['koltuk_sayisi'].astype(str).replace('2+2', '4')
        
        # Değişiklik sonrası tüm kolonu sayısal tipe çeviriyoruz.
        # Bu işlem, modelleme ve analiz için çok önemlidir.
        df['koltuk_sayisi'] = pd.to_numeric(df['koltuk_sayisi'], errors='coerce')
        print("-> 'koltuk_sayisi' kolonundaki '2+2' değerleri '4' olarak değiştirildi.")
        print("-> 'koltuk_sayisi' kolonu sayısal (numeric) tipe dönüştürüldü.")
    print("-" * 60)
    
    # --- TEMİZLEME SONRASI VERİ SETİNİN SON HALİ ---
    print("\n\n--- TÜM TEMİZLEME İŞLEMLERİ SONRASI VERİ SETİ ---")
    # Kolonların sırasını daha mantıklı bir hale getiriyoruz
    son_kolon_sirasi = [
        'marka', 'model', 'motor_tipi', 'motor_hacmi_cc', 'beygir_gucu', 
        'tork', 'hizlanma_0_100', 'maks_hiz', 'koltuk_sayisi', 
        'yakit_turu', 'fiyat'
    ]
    df = df[son_kolon_sirasi]
    
    print("\nVeri Setinin İlk 5 Satırı (Temizlenmiş Hali):\n")
    print(df.head())
    
    print("\nVeri Tiplerinin Son Durumu (info):\n")
    df.info()
    print("-" * 50)

    # --- ADIM E: FİYAT İLE DİĞER ÖZELLİKLERİN İLİŞKİSİNİ ANALİZ ETME ---
    print("\n--- Adım E: Fiyatı Etkileyen Faktörler Analiz Ediliyor ---")

    # 1. Sadece sayısal kolonları seçerek korelasyon matrisi oluşturma
    sayisal_df = df.select_dtypes(include=np.number)
    korelasyon_matrisi = sayisal_df.corr()

    # 2. Fiyat ile olan korelasyonları büyükten küçüğe sıralayarak yazdırma
    fiyat_korelasyonlari = korelasyon_matrisi['fiyat'].sort_values(ascending=False)
    print("\nFiyat ile Diğer Özelliklerin Korelasyonu (İlişki Gücü):\n")
    print(fiyat_korelasyonlari)

    # 3. Korelasyon matrisini bir ısı haritası (heatmap) ile görselleştirme
    print("\nKorelasyon ısı haritası oluşturuluyor...")
    plt.figure(figsize=(12, 10))
    sns.heatmap(korelasyon_matrisi, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    plt.title('Özelliklerin Birbiriyle Korelasyon Isı Haritası', fontsize=15)
    plt.show()

    # 4. Fiyatı en çok etkileyen ilk 3 pozitif faktör için saçılım grafiği (scatter plot) çizdirme
    print("\nFiyatı en çok etkileyen faktörler için saçılım grafikleri oluşturuluyor...")
    # 'fiyat' kendisiyle olan korelasyonu 1 olacağı için onu atlayarak başlıyoruz (index 1'den).
    # NaN olmayan korelasyonları alarak devam ediyoruz
    for kolon in fiyat_korelasyonlari.dropna().index[1:4]:
        plt.figure(figsize=(8, 5))
        sns.scatterplot(data=df, x=kolon, y='fiyat', alpha=0.6)
        # Grafik başlığını ve eksen etiketlerini daha okunaklı hale getiriyoruz
        baslik = f'Fiyat - {kolon.replace("_", " ").title()}'
        plt.title(baslik, fontsize=14)
        plt.xlabel(f'{kolon.replace("_", " ").title()}')
        plt.ylabel('Fiyat ($)')
        plt.grid(True)
        plt.show()

      # --- ADIM F: FİYAT TAHMİNİ İÇİN MODELLERİ EĞİTME VE KIYASLAMA (DÜZENLENMİŞ HALİ) ---
    print("\n--- Adım F: Fiyat Tahmini için Modeller Eğitiliyor ve Kıyaslanıyor ---")

    # 1. Model için veri setini hazırlama
    df_model = df.copy()
    df_model.dropna(subset=['fiyat'], inplace=True)
    
    kategorik_ozellikler = ['marka', 'motor_tipi', 'yakit_turu']
    df_model = pd.get_dummies(df_model, columns=kategorik_ozellikler, drop_first=True)

    y = df_model['fiyat']
    X = df_model.drop('fiyat', axis=1)

    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X)
    X = pd.DataFrame(X_imputed, columns=X.columns)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X = pd.DataFrame(X_scaled, columns=X.columns)
    
    print(f"Model için hazırlanan veri seti {X.shape[0]} satır ve {X.shape[1]} özellik içeriyor.")
    print("-" * 60)

    # 2. Modelleri ve cross-validation'ı tanımlama
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    results = []

    # 3. Modelleri eğitme ve değerlendirme
    print("\nModeller çapraz doğrulama ile değerlendiriliyor...\n")
    for name, model in models.items():
        r2_scores = cross_val_score(model, X, y, cv=kfold, scoring='r2')
        mae_scores = -1 * cross_val_score(model, X, y, cv=kfold, scoring='neg_mean_absolute_error')
        mse_scores = -1 * cross_val_score(model, X, y, cv=kfold, scoring='neg_mean_squared_error')
        results.append({
            'Model': name,
            'R2 Ortalama': r2_scores.mean(),
            'MAE Ortalama': mae_scores.mean(),
            'MSE Ortalama': mse_scores.mean()
        })
        print(f"-> Model: {name:<20} | R²: {r2_scores.mean():.4f} | MAE: ${mae_scores.mean():,.2f}")

    # 4. Sonuçları tablo halinde karşılaştırma
    print("-" * 60)
    print("\n--- MODEL KARŞILAŞTIRMA TABLOSU ---")
    results_df = pd.DataFrame(results).sort_values(by='R2 Ortalama', ascending=False).reset_index(drop=True)
    print(results_df)
    print("-" * 60)

    # --- 5. SONUÇLARI GÖRSELLEŞTİRME VE YORUMLAMA (YENİ EKLENEN BÖLÜM) ---
    print("\n--- SONUÇLARIN GÖRSELLEŞTİRİLMESİ ---")

    # R-Kare (R²) Skorlarını Görselleştirme
    plt.figure(figsize=(10, 6))
    sns.barplot(x='R2 Ortalama', y='Model', data=results_df, palette='viridis', orient='h')
    plt.title('Modellerin R-Kare (R²) Skoru Karşılaştırması', fontsize=16)
    plt.xlabel('Ortalama R² Skoru (Yüksek Değer Daha İyi)', fontsize=12)
    plt.ylabel('Model', fontsize=12)
    plt.xlim(0, 1) # R-kare skoru 0 ile 1 arasındadır
    # Barların üzerine değerlerini yazma
    for index, value in enumerate(results_df['R2 Ortalama']):
        plt.text(value, index, f'{value:.3f}', va='center', ha='left', fontsize=11, color='white')
    plt.show()

    # Ortalama Mutlak Hata (MAE) Skorlarını Görselleştirme
    plt.figure(figsize=(10, 6))
    # MAE için en düşük hatayı en üstte göstermek için yeniden sıralıyoruz
    mae_sorted_df = results_df.sort_values(by='MAE Ortalama', ascending=True)
    sns.barplot(x='MAE Ortalama', y='Model', data=mae_sorted_df, palette='plasma', orient='h')
    plt.title('Modellerin Ortalama Mutlak Hata (MAE) Karşılaştırması', fontsize=16)
    plt.xlabel('Ortalama Hata (Düşük Değer Daha İyi)', fontsize=12)
    plt.ylabel('Model', fontsize=12)
    # Barların üzerine değerlerini yazma
    for index, row in mae_sorted_df.iterrows():
        plt.text(row['MAE Ortalama'], index, f"${row['MAE Ortalama']:,.0f}", va='center', ha='left', fontsize=11, color='white')
    plt.show()
    
    print("\n" + "="*60)
    print("--- SONUÇLARIN YORUMU ---")
    print("="*60)
    
    # En iyi modeli R² skoruna göre seçiyoruz
    best_model_stats = results_df.iloc[0]
    
    print(f"\n>> En Başarılı Model: '{best_model_stats['Model']}'\n")
    
    print(f"-> AÇIKLAMA GÜCÜ (R²):")
    print(f"   Bu modelin R-kare skoru yaklaşık {best_model_stats['R2 Ortalama']:.3f}. Bu, modelin araba fiyatlarındaki değişkenliğin")
    print(f"   yaklaşık %{best_model_stats['R2 Ortalama']*100:.1f}'ini başarıyla açıklayabildiği anlamına gelir. Bu oldukça yüksek bir başarı oranıdır.")
    
    print(f"\n-> HATA PAYI (MAE):")
    print(f"   Bu modelin Ortalama Mutlak Hatası (MAE) ise yaklaşık ${best_model_stats['MAE Ortalama']:,.0f}.")
    print(f"   Bu da demek oluyor ki, modelin yaptığı fiyat tahminleri gerçek fiyattan ortalama olarak bu kadar sapmaktadır.")
      
    print("\n>> ÖZET:")
    print("   Grafikler ve tabloya göre, bu veri setiyle fiyat tahmini yapmak için en iyi performansı")
    print(f"   '{best_model_stats['Model']}' modeli göstermektedir. Hem açıklama gücü en yüksek hem de hata payı en düşük modellerden biridir.")
    print("="*60)


except FileNotFoundError:
    print("HATA: 'araba.csv' dosyası bulunamadı. Lütfen dosyanın kod ile aynı klasörde olduğundan emin olun.")
except Exception as e:
    print(f"Beklenmedik bir hata oluştu: {e}")