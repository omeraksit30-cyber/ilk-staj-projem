import time
import logging

# --- 1. LOG AYARLARI (Kara Kutu) ---
# Olayları 'sistem_kayitlari.log' dosyasına yaz diyoruz.
logging.basicConfig(
    filename='sistem_kayitlari.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s', # Tarih - Mesaj formatı
    datefmt='%H:%M:%S'
)

print("Sistem başlatıldı... (Durdurmak için Ctrl+C)")

# --- 2. JOB FONKSİYONU (İşçi) ---
def periyodik_kontrol():
    # Burada normalde SQL'e gidip "Yeni izin var mı?" diye soracağız.
    # Şimdilik mış gibi yapıyoruz.
    print("👷 JOB: Veritabanı kontrol ediliyor...")
    
    # Log dosyasına not düşelim
    logging.info("Job çalıştı: Veritabanı kontrolü yapıldı. Yeni kayıt yok.")

# --- 3. ZAMANLAYICI DÖNGÜSÜ (Bekçi) ---
try:
    while True:
        periyodik_kontrol()
        
        # 5 Saniye uyu (Bekle)
        time.sleep(5) 
        
except KeyboardInterrupt:
    print("\nSistem kapatılıyor...")
    logging.warning("Sistem kullanıcı tarafından kapatıldı!")