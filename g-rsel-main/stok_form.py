# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
import db_baglanti
from custom_widgets import siber_mesaj

class StokForm(QDialog):
    def __init__(self, urun_id=None, parent=None):
        super().__init__(parent)
        self.urun_id = urun_id
        self.setWindowTitle("Stok İşlemleri")
        self.setFixedSize(350, 300)
        self.setStyleSheet("background: #08081E; color: #E8E8FF;")
        
        self._ui_olustur()
        if self.urun_id:
            self._verileri_yukle()

    def _ui_olustur(self):
        lay = QVBoxLayout(self)
        form = QFormLayout()
        
        self.txt_ad = QLineEdit()
        self.txt_miktar = QLineEdit()
        self.txt_birim = QLineEdit()
        
        for widget in [self.txt_ad, self.txt_miktar, self.txt_birim]:
            widget.setStyleSheet("padding: 8px; border: 1px solid #1E1E4A; border-radius: 4px; background: #0F0F35;")
        
        form.addRow("Ürün Adı:", self.txt_ad)
        form.addRow("Miktar:", self.txt_miktar)
        form.addRow("Birim (kg/adet/lt):", self.txt_birim)
        
        lay.addLayout(form)
        
        btn_layout = QHBoxLayout()
        self.btn_kaydet = QPushButton("Kaydet")
        self.btn_kaydet.setStyleSheet("background: #6C63FF; color: white; padding: 10px; border-radius: 6px;")
        self.btn_kaydet.clicked.connect(self._kaydet)
        btn_layout.addWidget(self.btn_kaydet)
        lay.addLayout(btn_layout)

    def _verileri_yukle(self):
        # Sorguda 'stok_id' kullanarak veriyi çekiyoruz
        row = db_baglanti.sorgu_calistir("SELECT urun_adi, miktar, birim FROM stoklar WHERE stok_id = ?", (self.urun_id,))
        if row and len(row) > 0:
            self.txt_ad.setText(str(row[0][0]))
            self.txt_miktar.setText(str(row[0][1]))
            self.txt_birim.setText(str(row[0][2]))

    def _kaydet(self):
        ad = self.txt_ad.text()
        miktar = self.txt_miktar.text()
        birim = self.txt_birim.text()

        bag = db_baglanti.baglan()
        cur = bag.cursor()
        
        if self.urun_id:
            # Güncelleme kısmında 'WHERE stok_id = ?' kullanıyoruz
            cur.execute("UPDATE stoklar SET urun_adi=?, miktar=?, birim=?, son_guncelleme=CURRENT_TIMESTAMP WHERE stok_id=?", 
                        (ad, miktar, birim, self.urun_id))
        else:
            cur.execute("INSERT INTO stoklar (urun_adi, miktar, birim, son_guncelleme) VALUES (?,?,?,CURRENT_TIMESTAMP)", 
                        (ad, miktar, birim))
        
      
        bag.commit()
        db_baglanti.baglanti_kapat(bag, cur)
        self.accept()