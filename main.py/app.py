import streamlit as st
import time

# Sayfa Başlığı ve İkonu
st.set_page_config(page_title="Tavuk Dünyası AI", page_icon="🐔")

st.title("🐔 Tavuk Dünyası Asistanı")
st.write("Merhaba Ömer! Ben senin ilk görsel yapay zeka projeme hoşgeldin.")

# Yan Menü (Sidebar)
with st.sidebar:
    st.header("Ayarlar")
    st.write("Burası menü kısmı.")
    seviye = st.slider("Acı Seviyesi", 0, 10, 5)

# Ana Ekran
isim = st.text_input("Adınız nedir?", "Misafir")
soru = st.text_area("Yapay Zekaya Sorunuz:", "Hangi menüyü önerirsin?")

if st.button("Yapay Zekaya Gönder 🚀"):
    with st.spinner("Yapay zeka düşünüyor..."):
        time.sleep(2) # Sanki düşünüyormuş gibi bekletelim
        st.success(f"Sayın {isim}, '{soru}' sorunuz alındı!")
        st.info(f"Seçtiğiniz acı seviyesi: {seviye}/10. Buna göre 'Kekiklim' öneriyorum!")
        st.balloons() # Ekranda balonlar uçurur! 🎉