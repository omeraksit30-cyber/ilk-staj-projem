# Bu bir Python SÖZLÜĞÜDÜR (Dictionary).
# API'den veri işte böyle gelir.
gelen_veri = {
    "restoran": "Tavuk Dünyası",
    "sube": "Kadıköy",
    "menuler": [
        {"isim": "Kekiklim", "fiyat": 280, "aci_mi": False},
        {"isim": "Şefin Tavası", "fiyat": 290, "aci_mi": True},
        {"isim": "Barbekü", "fiyat": 285, "aci_mi": False}
    ]
}

# Şimdi bu veriyi okuyalım (Simülasyon)
print("Hoşgeldiniz: " + gelen_veri["restoran"])
print("Şube: " + gelen_veri["sube"])

print("--- MENÜ ---")

# Döngü (Loop) ile menüleri gezelim
for yemek in gelen_veri["menuler"]:
    print(f"Yemek: {yemek['isim']} - Fiyat: {yemek['fiyat']} TL")
    
    if yemek["aci_mi"] == True:
        print("DIKKAT: Bu yemek acılıdır! 🌶️")
    print("----------------")