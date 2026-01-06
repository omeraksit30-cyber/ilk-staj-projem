import sqlite3
import os
from openai import OpenAI

# --- AYARLAR ---
# Buraya yine kendi API Key'ini (veya stajda verileni) gireceksin.
api_sifresi = "BURAYA-API-KEY-GELECEK"

# --- ADIM 1: Veritabanı Fonksiyonu (Hafıza) ---
def bayiyi_bul(telefon_no):
    # Veritabanına bağlan
    baglanti = sqlite3.connect("tavuk_sistemi.db")
    garson = baglanti.cursor()
    
    # Telefon numarasını sor
    garson.execute("SELECT bayi_adi, sifre FROM bayiler WHERE telefon = ?", (telefon_no,))
    sonuc = garson.fetchone()
    
    baglanti.close()
    return sonuc # Eğer bulursa (İsim, Şifre) döner, bulamazsa None döner.

# --- ADIM 2: Yapay Zeka Başlatma ---
if "BURAYA" in api_sifresi:
    print("⚠️ UYARI: API Key girilmedi. Bot cevap veremez ama veritabanı çalışır.")
    client = None
else:
    client = OpenAI(api_key=api_sifresi)

# --- ADIM 3: Simülasyon (WhatsApp Gibi Davranma) ---
print("--- TAVUK DÜNYASI DESTEK HATTI ---")

# Sanki WhatsApp'tan mesaj gelmiş gibi önce telefon soruyoruz
gelen_telefon = input("Lütfen Telefon Numaranızı Girin (Örn: 5321112233): ")

# Bot önce hafızasına bakıyor...
bayi_bilgisi = bayiyi_bul(gelen_telefon)

if bayi_bilgisi is None:
    print("❌ HATA: Bu numara sistemde kayıtlı değil. Yetkisiz giriş!")
    exit() # Programı durdur

# Bayi bulunduysa bilgilerini alalım
bayi_adi = bayi_bilgisi[0] # Örn: Kadıköy Şubesi
bayi_sifresi = bayi_bilgisi[1] # Örn: 1234

print(f"✅ Giriş Başarılı! Hoşgeldin {bayi_adi}. Bot seni tanıdı.")
print("------------------------------------------------")

# --- ADIM 4: Sohbet Döngüsü ---
# Buradaki SİHİR şu: System mesajına veritabanı bilgisini GÖMÜYORUZ.
sistem_talimati = f"""
Sen Tavuk Dünyası'nın akıllı asistanısın.
Şu an konuştuğun kişi: {bayi_adi}.
Bu bayinin sistemdeki şifresi: {bayi_sifresi}.

Eğer kullanıcı "Şifrem ne?" veya "Şifremi unuttum" derse, ona yukarıdaki şifreyi söyle.
Başka konularda (Lojistik vb.) kibarca yardımcı ol.
"""

while True:
    soru = input(f"{bayi_adi}: ")
    
    if soru == "q":
        break

    if client:
        # Mesajı OpenAI'a gönderiyoruz
        cevap = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": sistem_talimati}, # <--- Sır Burada!
                {"role": "user", "content": soru}
            ]
        )
        print("Bot:", cevap.choices[0].message.content)
    else:
        # API Key yoksa test amaçlı manuel cevap verelim
        if "şifre" in soru.lower():
            print(f"Bot (Demo): Şifreniz veritabanında {bayi_sifresi} olarak görünüyor.")
        else:
            print("Bot (Demo): Mesajınız alındı (API Key olmadığı için AI cevap veremiyor).")