import sqlite3

# Veritabanına bağlan (Dosya yoksa oluşturur)
baglanti = sqlite3.connect("tavuk_sistemi.db")
cursor = baglanti.cursor()

# 1. Eski tabloyu sil (Varsa temizle)
cursor.execute("DROP TABLE IF EXISTS izin_talepleri")

# 2. Yeni tabloyu SIFIRDAN kur
cursor.execute("""
CREATE TABLE izin_talepleri (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    calisan_adi TEXT,
    talep_metni TEXT,
    durum TEXT DEFAULT 'BEKLIYOR'
)
""")

# 3. Örnek verileri ekle
cursor.execute("INSERT INTO izin_talepleri (calisan_adi, talep_metni, durum) VALUES ('Mehmet', 'Yarın doktora gideceğim, izin lazım.', 'BEKLIYOR')")
cursor.execute("INSERT INTO izin_talepleri (calisan_adi, talep_metni, durum) VALUES ('Ayşe', 'Yıllık izin kullanmak istiyorum.', 'BEKLIYOR')")

baglanti.commit()
print("✅ TABLO KURULDU! Artık main_system.py çalışabilir.")
baglanti.close()