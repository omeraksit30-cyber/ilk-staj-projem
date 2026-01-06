import sqlite3

# 1. ADIM: Mutfak Kapısını Aç (Bağlantı Kur)
# Eğer bu isimde bir dosya yoksa, Python onu senin için oluşturur.
baglanti = sqlite3.connect("tavuk_sistemi.db")

# Bu "imleç" (cursor), veritabanına emir veren garsondur.
garson = baglanti.cursor()

# 2. ADIM: Masaları Kur (Tablo Oluştur)
# Bayilerin bilgilerini tutacak bir tablo yapıyoruz.
# SQL dili şuna benzer: "CREATE TABLE IF NOT EXISTS..."
komut = """
CREATE TABLE IF NOT EXISTS bayiler (
    id INTEGER PRIMARY KEY,
    bayi_adi TEXT,
    telefon TEXT,
    sifre TEXT
)
"""
garson.execute(komut)

# 3. ADIM: Müşterileri Oturt (Veri Ekle)
# Önce tablo boş mu diye kontrol edelim, yoksa her çalıştığında aynı veriyi ekler.
garson.execute("SELECT count(*) FROM bayiler")
kisi_sayisi = garson.fetchone()[0]

if kisi_sayisi == 0:
    print("Tablo boş, bayiler ekleniyor...")
    # Veri ekleme komutu: "INSERT INTO..."
    bayi_listesi = [
        ("Kadıköy Şubesi", "5321112233", "1234"),
        ("Beşiktaş Şubesi", "5334445566", "9999"),
        ("İzmir Alsancak", "5556667788", "abcd")
    ]
    
    # Hepsini tek tek ekleyelim
    garson.executemany("INSERT INTO bayiler (bayi_adi, telefon, sifre) VALUES (?,?,?)", bayi_listesi)
    
    # KAYDETMEK ÖNEMLİDİR! (Commit)
    baglanti.commit() 
    print("✅ Bayiler başarıyla kaydedildi!")
else:
    print("ℹ️ Bayiler zaten kayıtlı.")

# 4. ADIM: Sorgulama (Botun yapacağı iş)
print("\n--- SORGULAMA TESTİ ---")
aranan_telefon = "5321112233" # Diyelim ki WhatsApp'tan bu numara yazdı

# SQL'e soruyoruz: "Telefonu bu olan bayinin adını ve şifresini getir"
garson.execute("SELECT bayi_adi, sifre FROM bayiler WHERE telefon = ?", (aranan_telefon,))
sonuc = garson.fetchone()

if sonuc:
    print(f"Buldum! Arayan Bayi: {sonuc[0]}")
    print(f"Mevcut Şifresi: {sonuc[1]}")
else:
    print("Bu numara sistemde kayıtlı değil.")

# 5. ADIM: Kapıyı Kapat
baglanti.close()