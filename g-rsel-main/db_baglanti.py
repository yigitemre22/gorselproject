# -*- coding: utf-8 -*-
# MySQL Veritabanı Bağlantı Modülü

import mysql.connector
from mysql.connector import Error

# ── Bağlantı Ayarları ────────────────────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",   # Sunucu adresi
    "port":     3306,          # Port (varsayılan: 3306)
    "user":     "root",            # Kullanıcı adı
    "password": "1234",            # Şifre
    "database": "spor_salonu",            # Veritabanı adı
    "charset":  "utf8mb4",
    "use_pure": True,              # PyQt5 DLL çakışmalarını (SSL) önlemek için saf Python kullan
}
# ─────────────────────────────────────────────────────────────────────────────


def baglan():
    """
    MySQL'e bağlanır ve bağlantı nesnesini döndürür.
    Hata durumunda None döner.
    """
    try:
        baglanti = mysql.connector.connect(**DB_CONFIG)
        if baglanti.is_connected():
            return baglanti
    except Error as e:
        print(f"[DB HATA] Bağlantı kurulamadı: {e}")
        return None


def baglanti_kapat(baglanti, cursor=None):
    """
    Cursor ve bağlantıyı güvenli şekilde kapatır.
    """
    try:
        if cursor:
            cursor.close()
        if baglanti and baglanti.is_connected():
            baglanti.close()
    except Error as e:
        print(f"[DB HATA] Kapatma hatası: {e}")


def baglanti_test():
    """
    Bağlantıyı test eder ve sonucu yazdırır.
    """
    baglanti = baglan()
    if baglanti:
        print(f"[DB OK] '{DB_CONFIG['database']}' veritabanına başarıyla bağlanıldı.")
        baglanti_kapat(baglanti)
    else:
        print("[DB HATA] Bağlantı başarısız. Ayarları kontrol edin.")


def sorgu_calistir(sorgu, parametreler=None):
    """
    Veritabanında SELECT, INSERT, UPDATE, DELETE sorgularını çalıştırır.
    SELECT sorgularında veriyi liste olarak döner.
    Diğer sorgularda etkilenen satır sayısını döner.
    """
    baglanti = baglan()
    if not baglanti:
        return None
    
    cursor = None
    sonuc = None
    try:
        # dictionary=False kalsın ki tuple (veri listesi) dönsün, senin tablolarınla uyumlu olsun
        cursor = baglanti.cursor(dictionary=False) 
        
        if parametreler:
            cursor.execute(sorgu, parametreler)
        else:
            cursor.execute(sorgu)
            
        # Eğer sorgu bir SELECT sorgusu ise verileri çek
        if cursor.description:
            sonuc = cursor.fetchall()
        else:
            # INSERT, UPDATE, DELETE ise değişiklikleri kaydet
            baglanti.commit()
            sonuc = cursor.rowcount # Etkilenen satır sayısı
            
    except Error as e:
        print(f"[DB SORGUN HATASI]: {e}")
        if baglanti:
            baglanti.rollback() # Hata durumunda işlemi geri al
        sonuc = None
    finally:
        baglanti_kapat(baglanti, cursor)
        
    return sonuc