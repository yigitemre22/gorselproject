# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QComboBox, QDateEdit, QPushButton, QHBoxLayout, QLabel
)
from PyQt5.QtCore import Qt, QDate
import db_baglanti
from custom_widgets import siber_mesaj

class EkipmanForm(QDialog):
    def __init__(self, ekipman_id=None, parent=None):
        super().__init__(parent)
        self.ekipman_id = ekipman_id
        self.setWindowTitle("Ekipman İşlemleri")
        self.setFixedSize(400, 450)
        self.setStyleSheet("background: #08081E; color: #E8E8FF;")
        
        self._ui_olustur()
        if self.ekipman_id:
            self._verileri_yukle()

    def _ui_olustur(self):
        lay = QVBoxLayout(self)
        form = QFormLayout()
        
        self.txt_ad = QLineEdit()
        self.combo_tur = QComboBox()
        self.txt_adet = QLineEdit()
        self.combo_durum = QComboBox()
        self.date_alim = QDateEdit(calendarPopup=True)
        self.date_alim.setDate(QDate.currentDate())
        
        # Stil
        for widget in [self.txt_ad, self.combo_tur, self.txt_adet, self.combo_durum, self.date_alim]:
            widget.setStyleSheet("padding: 8px; border: 1px solid #1E1E4A; border-radius: 4px; background: #0F0F35;")
        
        # Hatalı olan satırı bulup şu şekilde değiştirin:
        self.combo_durum.addItems(["aktif", "bakimda", "arizali"])
        
        # Türleri DB'den çek
        turler = db_baglanti.sorgu_calistir("SELECT ekipman_tur_id, tur_adi FROM ekipman_turleri")
        self.tur_map = {t[1]: t[0] for t in turler}
        self.combo_tur.addItems(self.tur_map.keys())

        form.addRow("Ekipman Adı:", self.txt_ad)
        form.addRow("Türü:", self.combo_tur)
        form.addRow("Adet:", self.txt_adet)
        form.addRow("Durum:", self.combo_durum)
        form.addRow("Alım Tarihi:", self.date_alim)
        
        lay.addLayout(form)
        
        btn_layout = QHBoxLayout()
        self.btn_kaydet = QPushButton("Kaydet")
        self.btn_kaydet.setStyleSheet("background: #6C63FF; color: white; padding: 10px; border-radius: 6px;")
        self.btn_kaydet.clicked.connect(self._kaydet)
        btn_layout.addWidget(self.btn_kaydet)
        
        lay.addLayout(btn_layout)

    def _verileri_yukle(self):
        row = db_baglanti.sorgu_calistir("SELECT ekipman_adi, ekipman_tur_id, adet, durum, alim_tarihi FROM ekipmanlar WHERE ekipman_id = ?", (self.ekipman_id,))
        if row:
            ad, tur_id, adet, durum, tarih = row[0]
            self.txt_ad.setText(ad)
            self.txt_adet.setText(str(adet))
            self.combo_durum.setCurrentText(durum)
            # Tarih setleme mantığı (DB formatına göre düzenlenmeli)
            self.date_alim.setDate(QDate.fromString(tarih, "yyyy-MM-dd"))

    def _kaydet(self):
        ad = self.txt_ad.text()
        tur_id = self.tur_map[self.combo_tur.currentText()]
        adet = self.txt_adet.text()
        durum = self.combo_durum.currentText()
        tarih = self.date_alim.date().toString("yyyy-MM-dd")

        bag = db_baglanti.baglan()
        cur = bag.cursor()
        
        if self.ekipman_id:
            cur.execute("UPDATE ekipmanlar SET ekipman_adi=?, ekipman_tur_id=?, adet=?, durum=?, alim_tarihi=? WHERE ekipman_id=?", 
                        (ad, tur_id, adet, durum, tarih, self.ekipman_id))
        else:
            cur.execute("INSERT INTO ekipmanlar (ekipman_adi, ekipman_tur_id, adet, durum, alim_tarihi) VALUES (?,?,?,?,?)", 
                        (ad, tur_id, adet, durum, tarih))
        
        bag.commit()
        db_baglanti.baglanti_kapat(bag, cur)
        self.accept()