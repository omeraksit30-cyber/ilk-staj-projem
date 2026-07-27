import sqlite3  # <--- YENİ EKLENDİ
import time
import logging
import schedule
from datetime import datetime
import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# API KEY BURAYA GELECEK (Pazartesi alacağın şifre)
os.environ["OPENAI_API_KEY"] = "BURAYA-SK-ILE-BASLAYAN-SIFRE-GELECEK"

# --- 1. AYARLAR & LOGLAMA ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler("sistem_gunlugu.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

# --- 2. YAPAY ZEKA MODÜLÜ ---
# --- RAG SİSTEMİNİ HAZIRLA (Sadece bir kere çalışır) ---
print("🧠 Yapay Zeka Kuralları Okuyor...")
try:
    loader = TextLoader("kurallar.txt")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    # Veriyi Sayısallaştır (Embedding)
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, embeddings)
    
    # Karar Mekanizması (Zincir)
    qa_zinciri = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo"), 
        chain_type="stuff", 
        retriever=db.as_retriever()
    )
    print("🧠 Beyin Yüklendi! Hazır.")
except Exception as e:
    print(f"⚠️ UYARI: API Key olmadığı için beyin yüklenemedi. ({e})")
    qa_zinciri = None

# --- YENİ AKILLI KARAR FONKSİYONU ---
def ai_karar_ver(talep):
    logger.info(f"🤖 AI Düşünüyor: '{talep}' talebi analiz ediliyor...")
    
    if qa_zinciri is None:
        return "HATA - API Key Yok"
    
    try:
        # Yapay zekaya soruyu soruyoruz
        soru = f"Şu talebi kurallara göre değerlendir: '{talep}'. Cevabın sadece ONAY veya RET ile başlasın."
        cevap = qa_zinciri.run(soru)
        return cevap
    except Exception as e:
        logger.error(f"AI Hatası: {e}")
        return "RET - Sistem Hatası"

# --- 3. VERİTABANI İŞLERİ (JOB GÖREVİ) ---
def veritabani_kontrol_job():
    logger.info("🕵️‍♂️ JOB BAŞLADI: Gerçek veritabanı kontrol ediliyor...")
    
    # Veritabanına Bağlan
    try:
        baglanti = sqlite3.connect("tavuk_sistemi.db")
        cursor = baglanti.cursor()
        
        # Bekleyenleri Çek
        cursor.execute("SELECT id, calisan_adi, talep_metni FROM izin_talepleri WHERE durum='BEKLIYOR'")
        talepler = cursor.fetchall()
        
        if talepler:
            logger.info(f"📝 {len(talepler)} adet yeni talep bulundu!")
            
            for talep in talepler:
                talep_id = talep[0]
                isim = talep[1]
                metin = talep[2]
                
                logger.info(f"--- İşleniyor: {isim} -> {metin}")
                
                # AI Kararı
                karar = ai_karar_ver(metin)
                
                # Veritabanını Güncelle
                cursor.execute("UPDATE izin_talepleri SET durum=? WHERE id=?", (karar, talep_id))
                logger.info(f"✅ {isim} için karar ({karar}) veritabanına işlendi.")
                
            baglanti.commit()
        else:
            logger.info("💤 Bekleyen talep yok.")
            
        baglanti.close()
        
    except Exception as e:
        logger.error(f"Bir hata oluştu: {e}")

# --- 4. PLANLAMA (SCHEDULER) ---
schedule.every(10).seconds.do(veritabani_kontrol_job)

# --- 5. ANA DÖNGÜ ---
print("""
==============================================
   KURUMSAL OTOMASYON BOTU v2.0 (SQL BAĞLI)
   Hedef: Portekiz / Almanya / İtalya 🚀
==============================================
""")

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    logger.warning("🛑 Sistem kullanıcı tarafından durduruldu!")