# 1. TABAN: Python yüklü bir Linux bilgisayar istiyoruz
FROM python:3.9-slim

# 2. ÇALIŞMA MASASI: Kodları /app klasörüne koyacağız
WORKDIR /app

# 3. MALZEMELER: Önce kütüphane listesini kopyala
# (Bunun için requirements.txt dosyası oluşturacağız)
COPY requirements.txt .

# 4. HAZIRLIK: Kütüphaneleri kur
RUN pip install --no-cache-dir -r requirements.txt

# 5. YEMEK: Tüm kodlarımızı içeri at
COPY . .

# 6. SERVİS: Konteynır çalışınca bu komutu başlat
CMD ["python", "rag_bot.py"]