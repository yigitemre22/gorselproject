# -*- coding: utf-8 -*-
# TitanFit Gym – Gider Formu 

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QDateEdit, QMessageBox, QGridLayout, QFrame
)
from PyQt5.QtCore import Qt, QDate
from tema import uygula_tema
import db_baglanti


class GiderForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gider Kaydı Ekle")
        self.setFixedSize(420, 340)
        uygula_tema(self)
        self.setStyleSheet(self.styleSheet() + """
            QDialog { background-color: #0A0A22; border: 1px solid #1E1E4A; border-radius: 10px; }
        """)
        self._ui_olustur()

    def _ui_olustur(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(18)

        # Başlık
        baslik = QLabel("📉  Yeni Gider Kaydı")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("""
            font-size: 17px;
            font-weight: 800;
            color: #A78BFA;
            letter-spacing: 1px;
            padding-bottom: 6px;
            border-bottom: 1px solid #1E1E4A;
            background: transparent;
        """)
        layout.addWidget(baslik)

        # Form Alanları
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setColumnStretch(1, 1)

        def label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-size:11px; color:#7B7BAA; font-weight:700; letter-spacing:1px; background:transparent; border:none;")
            return lbl

        # Gider Türü
        grid.addWidget(label("GİDER TÜRÜ"), 0, 0)
        self.tur_input = QComboBox()
        self.tur_input.setFixedHeight(38)
        self.tur_input.addItems(["Elektrik","Su","Doğalgaz","Personel Maaşı",
                                  "Ekipman Bakımı","Temizlik","Kira","Diğer"])
        self.tur_input.setEditable(True)
        grid.addWidget(self.tur_input, 0, 1)

        # Tutar
        grid.addWidget(label("TUTAR (₺)"), 1, 0)
        self.tutar_input = QLineEdit()
        self.tutar_input.setFixedHeight(38)
        self.tutar_input.setPlaceholderText("0.00")
        grid.addWidget(self.tutar_input, 1, 1)

        # Tarih
        grid.addWidget(label("TARİH"), 2, 0)
        self.tarih_input = QDateEdit()
        self.tarih_input.setFixedHeight(38)
        self.tarih_input.setCalendarPopup(True)
        self.tarih_input.setDate(QDate.currentDate())
        grid.addWidget(self.tarih_input, 2, 1)

        # Açıklama
        grid.addWidget(label("AÇIKLAMA"), 3, 0)
        self.aciklama_input = QLineEdit()
        self.aciklama_input.setFixedHeight(38)
        self.aciklama_input.setPlaceholderText("İsteğe bağlı")
        grid.addWidget(self.aciklama_input, 3, 1)

        layout.addLayout(grid)
        layout.addStretch()

        # Butonlar
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
        tur = self.tur_input.currentText().strip()
        tutar = self.tutar_input.text().strip()
        tarih = self.tarih_input.date().toString("yyyy-MM-dd")
        aciklama = self.aciklama_input.text().strip()

        if not tutar or not tur:
            QMessageBox.warning(self, "Uyarı", "Tutar ve Gider Türü alanları zorunludur.")
            return
        try:
            float(tutar)
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Tutar sadece rakamlardan oluşmalıdır.")
            return

        try:
            bag = db_baglanti.baglan()
            cur = bag.cursor()
            cur.execute(
                "INSERT INTO giderler (gider_turu, tutar, gider_tarihi, aciklama) VALUES (%s,%s,%s,%s)",
                (tur, tutar, tarih, aciklama)
            )
            bag.commit()
            db_baglanti.baglanti_kapat(bag, cur)
            QMessageBox.information(self, "Başarılı", "Gider başarıyla kaydedildi.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Kayıt işlemi başarısız:\n{e}")