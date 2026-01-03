import os
from openai import OpenAI

# ------------------------------------------------------------------
# DİKKAT: Burası Stajdaki En Önemli Kısım!
# Patronun sana "API Key" (uzun bir şifre) verecek.
# O şifreyi buradaki tırnakların içine yazacaksın.
# Şimdilik boş bırakıyoruz, çünkü paralı bir şifredir.
# ------------------------------------------------------------------
api_sifresi = "BURAYA-PATRONUN-VERDIGI-UZUN-SIFRE-GELECEK"

# Eğer şifre yoksa uyarı verelim (Hata almamak için)
if "BURAYA" in api_sifresi:
    print("⚠️ UYARI: API Key girilmediği için yapay zeka cevap veremez.")
    print("Lütfen stajda verilen key'i koda ekleyin.")
else:
    # Yapay Zeka Bağlantısını Başlatıyoruz
    client = OpenAI(api_key=api_sifresi)

    def yapay_zekaya_sor(soru):
        print("🤖 Yapay zeka düşünüyor...")
        
        try:
            cevap = client.chat.completions.create(
                model="gpt-3.5-turbo", # Kullanılan beyin modeli
                messages=[
                    # Sisteme rolünü öğretiyoruz (Bu RAG mimarisinin temelidir)
                    {"role": "system", "content": "Sen Tavuk Dünyası'nın yardımsever asistanısın. Müşterilere kibar davran."},
                    # Kullanıcının sorusunu iletiyoruz
                    {"role": "user", "content": soru}
                ]
            )
            # Gelen cevabı alıp geri gönderiyoruz
            return cevap.choices[0].message.content
        except Exception as hata:
            return f"Bir hata oluştu: {hata}"

    # --- TEST ALANI ---
    while True:
        soru = input("Sen: ")
        if soru == "q":
            break
        
        # Fonksiyonu çağır ve cevabı yazdır
        gelen_cevap = yapay_zekaya_sor(soru)
        print("Bot:", gelen_cevap)