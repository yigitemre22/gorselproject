# -*- coding: utf-8 -*-
# TitanFit Gym – Ödeme Formu 

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QDateEdit, QMessageBox, QGridLayout
)
from PyQt5.QtCore import Qt, QDate
from tema import uygula_tema
import db_baglanti


class OdemeForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tahsilat Al")
        self.setFixedSize(420, 390)
        uygula_tema(self)
        self.setStyleSheet(self.styleSheet() + """
            QDialog { background-color: #0A0A22; border: 1px solid #1E1E4A; border-radius: 10px; }
        """)
        self.uyeler   = self._getir("SELECT uye_id, ad, soyad FROM uyeler WHERE durum='aktif'")
        self.yontemler = self._getir("SELECT odeme_yontem_id, yontem_adi FROM odeme_yontemleri")
        self._ui_olustur()

    def _getir(self, sql):
        try:
            bag = db_baglanti.baglan()
            if not bag: return []
            cur = bag.cursor(dictionary=True)
            cur.execute(sql)
            veri = cur.fetchall()
            db_baglanti.baglanti_kapat(bag, cur)
            return veri
        except Exception as e:
            print(e); return []

    def _ui_olustur(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(18)

        baslik = QLabel("💰  Tahsilat Al")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("""
            font-size: 17px; font-weight: 800; color: #93C5FD;
            letter-spacing: 1px; padding-bottom: 6px;
            border-bottom: 1px solid #1E1E4A; background: transparent;
        """)
        layout.addWidget(baslik)

        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(1, 1)

        def label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-size:11px; color:#7B7BAA; font-weight:700; letter-spacing:1px; background:transparent; border:none;")
            return lbl

        # Üye
        grid.addWidget(label("ÜYE"), 0, 0)
        self.uye_input = QComboBox()
        self.uye_input.setFixedHeight(38)
        for u in self.uyeler:
            self.uye_input.addItem(f"{u['ad']} {u['soyad']}", u['uye_id'])
        grid.addWidget(self.uye_input, 0, 1)

        # Tutar
        grid.addWidget(label("TUTAR (₺)"), 1, 0)
        self.tutar_input = QLineEdit()
        self.tutar_input.setFixedHeight(38)
        self.tutar_input.setPlaceholderText("0.00")
        grid.addWidget(self.tutar_input, 1, 1)

        # Yöntem
        grid.addWidget(label("YÖNTEM"), 2, 0)
        self.yontem_input = QComboBox()
        self.yontem_input.setFixedHeight(38)
        for y in self.yontemler:
            self.yontem_input.addItem(y['yontem_adi'], y['odeme_yontem_id'])
        grid.addWidget(self.yontem_input, 2, 1)

        # Tarih
        grid.addWidget(label("TARİH"), 3, 0)
        self.tarih_input = QDateEdit()
        self.tarih_input.setFixedHeight(38)
        self.tarih_input.setCalendarPopup(True)
        self.tarih_input.setDate(QDate.currentDate())
        grid.addWidget(self.tarih_input, 3, 1)

        # Açıklama
        grid.addWidget(label("AÇIKLAMA"), 4, 0)
        self.aciklama_input = QLineEdit()
        self.aciklama_input.setFixedHeight(38)
        self.aciklama_input.setPlaceholderText("İsteğe bağlı")
        grid.addWidget(self.aciklama_input, 4, 1)

        layout.addLayout(grid)
        layout.addStretch()

        btn_lay = QHBoxLayout()
        btn_lay.setSpacing(10)
        iptal_btn = QPushButton("İptal")
        iptal_btn.setFixedHeight(40)
        iptal_btn.setCursor(Qt.PointingHandCursor)
        iptal_btn.clicked.connect(self.reject)
        kaydet_btn = QPushButton("  Kaydet  →")
        kaydet_btn.setObjectName("loginButton")
        kaydet_btn.setFixedHeight(40)
        kaydet_btn.setCursor(Qt.PointingHandCursor)
        kaydet_btn.clicked.connect(self._kaydet)
        btn_lay.addWidget(iptal_btn)
        btn_lay.addWidget(kaydet_btn)
        layout.addLayout(btn_lay)

    def _kaydet(self):
        uye_id   = self.uye_input.currentData()
        tutar    = self.tutar_input.text().strip()
        yontem   = self.yontem_input.currentData()
        tarih    = self.tarih_input.date().toString("yyyy-MM-dd")
        aciklama = self.aciklama_input.text().strip()

        if not tutar:
            QMessageBox.warning(self, "Uyarı", "Lütfen tutar giriniz."); return
        try:
            float(tutar)
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Tutar sadece rakamlardan oluşmalıdır."); return

        try:
            bag = db_baglanti.baglan()
            cur = bag.cursor()
            cur.execute(
                "INSERT INTO odemeler (uye_id,tutar,odeme_tarihi,odeme_yontem_id,aciklama) VALUES (%s,%s,%s,%s,%s)",
                (uye_id, tutar, tarih, yontem, aciklama)
            )
            bag.commit()
            db_baglanti.baglanti_kapat(bag, cur)
            QMessageBox.information(self, "Başarılı", "Tahsilat başarıyla kaydedildi.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt işlemi başarısız:\n{e}")