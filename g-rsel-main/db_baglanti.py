# -*- coding: utf-8 -*-
# SQLite Veritabanı Bağlantı Modülü

import sqlite3
import os

# ── Veritabanı Dosyası ───────────────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "gorsel.db")
# ─────────────────────────────────────────────────────────────────────────────


def baglan():
    """
    SQLite'a bağlanır ve bağlantı nesnesini döndürür.
    Hata durumunda None döner.
    """
    try:
        baglanti = sqlite3.connect(DB_PATH)
        return baglanti
    except sqlite3.Error as e:
        print(f"[DB HATA] Bağlantı kurulamadı: {e}")
        return None


def baglanti_kapat(baglanti, cursor=None):
    """
    Cursor ve bağlantıyı güvenli şekilde kapatır.
    """
    try:
        if cursor:
            cursor.close()
        if baglanti:
            baglanti.close()
    except sqlite3.Error as e:
        print(f"[DB HATA] Kapatma hatası: {e}")


def baglanti_test():
    """
    Bağlantıyı test eder ve sonucu yazdırır.
    """
    baglanti = baglan()
    if baglanti:
        print("[DB OK] 'gorsel.db' veritabanına başarıyla bağlanıldı.")
        baglanti_kapat(baglanti)
    else:
        print("[DB HATA] Bağlantı başarısız.")


def sorgu_calistir(sorgu, parametreler=None):
    """
    SELECT / INSERT / UPDATE / DELETE sorgularını çalıştırır.
    SELECT → veri döner
    diğerleri → etkilenen satır sayısı
    """
    baglanti = baglan()
    if not baglanti:
        return None

    cursor = None
    sonuc = None

    try:
        cursor = baglanti.cursor()

        if parametreler:
            cursor.execute(sorgu, parametreler)
        else:
            cursor.execute(sorgu)

        # SELECT kontrolü
        if sorgu.strip().lower().startswith("select"):
            sonuc = cursor.fetchall()
        else:
            baglanti.commit()
            sonuc = cursor.rowcount

    except sqlite3.Error as e:
        print(f"[DB SORGU HATASI]: {e}")
        baglanti.rollback()
        sonuc = None

    finally:
        baglanti_kapat(baglanti, cursor)

    return sonuc