import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

# --- API KEY AYARI ---
# Buraya API Key'ini girmen lazım
os.environ["OPENAI_API_KEY"] = "BURAYA-API-KEY-GELECEK"

print("🔄 Menü yükleniyor ve öğreniliyor...")

# 1. ADIM: Dosyayı Yükle
loader = TextLoader("menu.txt")
belgeler = loader.load()

# 2. ADIM: Veriyi Matematiksel Format'a (Vektör) Çevir
# Bu işlem metni, yapay zekanın anlayacağı sayılara dönüştürür.
embeddings = OpenAIEmbeddings()
vektor_veritabani = FAISS.from_documents(belgeler, embeddings)

# 3. ADIM: Arama Motorunu Kur
# "RetrievalQA" zinciri, bizim yerimize dosyada arama yapıp cevabı üretir.
qa_zinciri = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-3.5-turbo"),
    chain_type="stuff",
    retriever=vektor_veritabani.as_retriever()
)

print("✅ Hazır! Tavuk Dünyası'nın GİZLİ bilgilerini sorabilirsin.")
print("---------------------------------------------------------")

while True:
    soru = input("Sorunuz (Çıkış için 'q'): ")
    
    if soru == "q":
        break
    
    # LangChain burada devreye giriyor:
    # Soruyu al -> Dosyada cevabı bul -> GPT ile cümle kur -> Cevap ver
    try:
        cevap = qa_zinciri.invoke(soru)
        # LangChain bazen cevabı 'result' içinde döndürür
        print(f"Bot: {cevap['result']}")
    except Exception as e:
        print(f"Hata: {e}")