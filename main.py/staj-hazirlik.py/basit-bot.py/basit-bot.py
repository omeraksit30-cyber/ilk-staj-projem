import time # Zaman kütüphanesini ekledik (bekletmek için)

def bot_cevap_ver(mesaj):
    # Gelen mesaja göre cevap uyduralım (Bu kısım ilerde Yapay Zeka olacak)
    mesaj = mesaj.lower() # Hepsini küçük harfe çevir
    
    if "merhaba" in mesaj:
        return "Merhaba! Tavuk Dünyası asistanına hoşgeldin."
    elif "fiyat" in mesaj:
        return "Menülerimiz ortalama 280-300 TL arasındadır."
    elif "öneri" in mesaj:
        return "Benim favorim Kekiklim! Denemelisin."
    else:
        return "Bunu anlayamadım, ama yakında öğreneceğim!"

# ANA DÖNGÜ (Sonsuzluk)
print("Bot başlatılıyor... (Çıkmak için 'q' yaz)")

while True:
    kullanici_girdisi = input("Sen: ")
    
    if kullanici_girdisi == "q":
        print("Bot: Görüşürüz!")
        break # Döngüyü kırar ve çıkar
    
    # Sanki yapay zeka düşünüyormuş gibi 1 saniye bekletelim
    time.sleep(1)
    
    cevap = bot_cevap_ver(kullanici_girdisi)
    print("Bot: " + cevap)