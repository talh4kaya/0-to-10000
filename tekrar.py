import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import datetime

# --- 1. VERİTABANI BAĞLANTI BİLGİLERİ ---
db_kullanici_adi = "postgres"
db_sifre = "13145313Sa"  # Kendi şifreniz
db_host = "localhost"
db_port = "5432"
db_adi = "projecalisma"  # Kendi veritabanı adınız

# Bağlantı metnini oluştur
connection_string = f"postgresql://{db_kullanici_adi}:{db_sifre}@{db_host}:{db_port}/{db_adi}"
print(f"Oluşturulan Bağlantı Adresi: postgresql://{db_kullanici_adi}:***@{db_host}:{db_port}/{db_adi}")

try:
    # SQLAlchemy motorunu oluştur
    engine = create_engine(connection_string)

    # --- ADIM 1: VERİYİ VERİTABANINDAN OKUMA ---
    print("\n--- Adım 1: PostgreSQL'den Veri Çekme ---")
    
    sql_query = "SELECT * FROM calisanlar;"
    df = pd.read_sql(sql_query, engine, index_col='id')
    
    print("✅ Veritabanı bağlantısı ve veri okuma BAŞARILI!")
    print("\nİşlemden Önceki Orijinal DataFrame:")
    print(df)
    print("\n" * 2)

    # --- ADIM 2: PANDAS İLE VERİ TEMİZLEME VE HAZIRLAMA ---
    print("--- Adım 2: Pandas ile Veri Temizleme ve Hazırlama ---")

    # Eksik verileri yönetme (FutureWarning vermeyen yöntem)
    df['isim'] = df['isim'].fillna('Bilinmeyen')
    median_maas = df['maas'].median()
    df['maas'] = df['maas'].fillna(median_maas)
    df['ise_giris_tarihi'] = pd.to_datetime(df['ise_giris_tarihi'])

    print("Temizlenmiş DataFrame:")
    print(df.head())
    print("\n" * 2)

    # --- ADIM 3: NUMPY İLE MATEMATİKSEL VE İSTATİSTİKSEL İŞLEMLER ---
    print("--- Adım 3: NumPy ile Matematiksel ve İstatistiksel İşlemler ---")

    maaslar_np = df['maas'].to_numpy()
    skorlar_np = df['performans_skoru'].to_numpy()

    print(f"Maaş Ortalaması (NumPy): {np.mean(maaslar_np):.2f}")
    print(f"En Yüksek Performans Skoru (NumPy): {np.max(skorlar_np)}")

    df['maas'] = maaslar_np * 1.10

    min_skor, max_skor = np.min(skorlar_np), np.max(skorlar_np)
    if (max_skor - min_skor) != 0:
        df['normalize_performans_skoru'] = (skorlar_np - min_skor) / (max_skor - min_skor)
    else:
        df['normalize_performans_skoru'] = 0

    print("\nMaaşlara zam yapıldıktan ve skorlar normalize edildikten sonra DataFrame:")
    print(df.head())
    print("\n" * 2)

    # --- ADIM 4: PANDAS İLE İLERİ SEVİYE ANALİZ VE MANİPÜLASYON ---
    print("--- Adım 4: Pandas ile İleri Seviye Analiz ve Manipülasyon ---")

    # Yeni Sütunlar Ekleme
    current_date = pd.to_datetime(datetime.date.today())
    
    # !!! HATA BURADAYDI, DÜZELTİLDİ !!!
    df['calisma_suresi_yil'] = ((current_date - df['ise_giris_tarihi']).dt.days / 365.25).round(2)
    
    df['maas_kategorisi'] = df['maas'].apply(lambda x: 'Yüksek' if x > 10000 else ('Orta' if x > 8500 else 'Düşük'))
    
    print("Yeni sütunlar (calisma_suresi_yil, maas_kategorisi) eklendi.")
    
    departman_analizi = df.groupby('departman').agg(
        ortalama_maas=('maas', 'mean'),
        ortalama_performans=('performans_skoru', 'mean'),
        calisan_sayisi=('isim', 'count')
    ).round(2)
    print("\nDepartman Bazında Analiz:")
    print(departman_analizi)

    df_for_update = df[['isim', 'departman', 'ise_giris_tarihi', 'maas', 'performans_skoru']].copy()
    print("\nVeritabanına güncellenecek son hali:")
    print(df_for_update)
    print("\n" * 2)

    # --- ADIM 5: VERİYİ VERİTABANINDA GÜNCELLEME ---
    print("--- Adım 5: DataFrame'deki Güncellemeleri PostgreSQL'e Geri Yazma ---")

    with engine.connect() as connection:
        for index, row in df_for_update.iterrows():
            update_query = text("""
                UPDATE calisanlar
                SET 
                    isim = :isim,
                    departman = :departman,
                    maas = :maas,
                    performans_skoru = :performans
                WHERE id = :id;
            """)
            params = {'isim': row['isim'], 'departman': row['departman'], 'maas': row['maas'], 'performans': row['performans_skoru'], 'id': index}
            connection.execute(update_query, params)
        # SQLAlchemy 2.0+ için with bloğu sonunda commit otomatik yapılır.
        
    print("✅ Veritabanındaki 'calisanlar' tablosu başarıyla güncellendi.")
    print("\n" * 2)


    # --- ADIM 6: GÜNCELLENMİŞ VERİYİ KONTROL ETME ---
    print("--- Adım 6: Veritabanındaki Güncellenmiş Veriyi Kontrol Etme ---")
    
    df_guncel = pd.read_sql("SELECT * FROM calisanlar ORDER BY id;", engine, index_col='id')
    print("Veritabanından çekilen güncellenmiş DataFrame:")
    print(df_guncel)

except Exception as e:
    print(f"\n❌ BİR HATA OLUŞTU! Karşılaşılan Hata: {e}")
    print("\n--- Hata Kontrol Listesi ---")
    print("1. Şifrenizin doğru olduğundan emin misiniz?")
    print("2. 'host', 'port', 'db_adi' bilgilerinin doğru olduğunu kontrol ettiniz mi?")
    print("3. 'calisanlar' tablosu veritabanınızda mevcut mu ve sütun adları doğru mu?")
    print("4. PostgreSQL sunucunuzun çalıştığından emin misiniz?")