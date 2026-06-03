import sqlite3
import random
from datetime import datetime

# Veritabanına bağlan
conn = sqlite3.connect(r'C:\Users\yigit\OneDrive\Masaüstü\gorsel\aray-z\g-rsel-main\gorsel.db')
cursor = conn.cursor()

# Hedef oranlar
# 18-25 (%30), 26-35 (%42), 36+ (%28)
yas_gruplari = ['18-25', '26-35', '36+']
agirliklar = [0.30, 0.42, 0.28]

# 1000 adet yaş aralığı seçimi (ağırlıklı)
secilen_gruplar = random.choices(yas_gruplari, weights=agirliklar, k=1000)

# Veritabanındaki her bir üye için doğum tarihi üret
for i in range(1, 1001):
    grup = secilen_gruplar[i-1]
    
    if grup == '18-25':
        yil = random.randint(2001, 2008)
    elif grup == '26-35':
        yil = random.randint(1991, 2000)
    else: # 36+
        yil = random.randint(1960, 1990)
    
    tarih = f"{yil}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    
    # Mevcut veriyi güncelle
    cursor.execute("UPDATE uyeler SET dogum_tarihi = ? WHERE uye_id = ?", (tarih, i))

conn.commit()
conn.close()
print("Yaş dağılımı %30, %42, %28 oranlarına göre başarıyla güncellendi.")