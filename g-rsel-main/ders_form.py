# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from custom_widgets import CustomTitleBar
from db_baglanti import sorgu_calistir  # Projenin gerçek DB modülü

class DersForm(QDialog):
    def __init__(self, ders_id=None, parent=None):
        super().__init__(parent)
        self.ders_id = ders_id
        
        # BEYAZ WINDOWS BARINI SİLME VE SİBERPUNK TRANSPARANLIK AYARI
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(500, 440)
        
        self._ui_olustur()
        self._antrenorleri_yukle()
        
        if self.ders_id:
            self._bilgileri_getir()

    def _ui_olustur(self):
        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(0, 0, 0, 0)
        ana_layout.setSpacing(0)

        # Siberpunk Başlık Barı
        self.baslik_cubugu = CustomTitleBar(self)
        baslik_metni = "➕  YENİ DERS EKLE" if not self.ders_id else "✏️  DERS DÜZENLE"
        self.baslik_cubugu.title_label.setText(baslik_metni)
        ana_layout.addWidget(self.baslik_cubugu)

        # Form Koyu Arka Plan Paneli
        self.form_panel = QWidget()
        self.form_panel.setObjectName("FormPanel")
        self.form_panel.setStyleSheet("""
            QWidget#FormPanel {
                background-color: #0A0A22;
                border-left: 2px solid #6C63FF;
                border-right: 2px solid #6C63FF;
                border-bottom: 2px solid #6C63FF;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
            }
        """)
        
        icerik_layout = QVBoxLayout(self.form_panel)
        icerik_layout.setContentsMargins(24, 20, 24, 20)
        icerik_layout.setSpacing(14)

        grid = QGridLayout()
        grid.setSpacing(12)

        def label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-size:11px; color:#7B7BAA; font-weight:700; letter-spacing:1px; background:transparent;")
            return lbl

        def field(placeholder=None):
            f = QLineEdit()
            if placeholder: f.setPlaceholderText(placeholder)
            f.setFixedHeight(36)
            f.setStyleSheet("background-color: #141438; border: 1px solid #1E1E4A; border-radius: 6px; color: #E8E8FF; padding-left: 10px;")
            return f

        grid.addWidget(label("DERS ADI"), 0, 0)
        self.ders_adi_input = field("Dersin Adı")
        grid.addWidget(self.ders_adi_input, 0, 1)

        grid.addWidget(label("ANTRENÖR"), 1, 0)
        self.antrenor_combo = QComboBox()
        self.antrenor_combo.setFixedHeight(36)
        self.antrenor_combo.setStyleSheet("""
            QComboBox {
                background-color: #141438;
                border: 1px solid #1E1E4A;
                border-radius: 6px;
                color: #E8E8FF;
                padding-left: 10px;
            }
            QComboBox::drop-down { border: none; }
        """)
        grid.addWidget(self.antrenor_combo, 1, 1)

        grid.addWidget(label("DERS SAATİ"), 2, 0)
        self.ders_saati_input = field("SS:DD (Örn: 14:30)")
        grid.addWidget(self.ders_saati_input, 2, 1)

        grid.addWidget(label("KAPASİTE"), 3, 0)
        self.kapasite_input = field("Maksimum kontenjan")
        grid.addWidget(self.kapasite_input, 3, 1)

        grid.addWidget(label("SALON NO"), 4, 0)
        self.salon_input = field("Örn: Salon 1")
        grid.addWidget(self.salon_input, 4, 1)

        icerik_layout.addLayout(grid)
        icerik_layout.addStretch()

        # Alt Butonlar
        btn_lay = QHBoxLayout()
        iptal_btn = QPushButton("İptal")
        iptal_btn.setFixedHeight(40)
        iptal_btn.setStyleSheet("background-color: #141438; color: #7B7BAA; border: 1px solid #1E1E4A; border-radius: 6px; font-weight:700;")
        iptal_btn.clicked.connect(self.reject)
        
        kaydet_btn = QPushButton("  Kaydet  →")
        kaydet_btn.setFixedHeight(40)
        kaydet_btn.setStyleSheet("background-color: #6C63FF; color: white; border: none; border-radius: 6px; font-weight:700;")
        kaydet_btn.clicked.connect(self._kaydet)
        
        btn_lay.addWidget(iptal_btn)
        btn_lay.addWidget(kaydet_btn)
        icerik_layout.addLayout(btn_lay)

        ana_layout.addWidget(self.form_panel)

    def paintEvent(self, event):
        from PyQt5.QtWidgets import QStyle, QStyleOption
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    def _antrenorleri_yukle(self):
        rows = sorgu_calistir("SELECT antrenor_id, CONCAT(ad, ' ', soyad) FROM antrenorler")
        if rows and isinstance(rows, list):
            for r in rows:
                self.antrenor_combo.addItem(str(r[1]), r[0])

    def _bilgileri_getir(self):
        res = sorgu_calistir("SELECT ders_adi, antrenor_id, ders_saati, kapasite, salon FROM dersler WHERE ders_id=%s", (self.ders_id,))
        if res and isinstance(res, list):
            v = res[0]
            self.ders_adi_input.setText(str(v[0]))
            idx = self.antrenor_combo.findData(v[1])
            if idx != -1: self.antrenor_combo.setCurrentIndex(idx)
            self.ders_saati_input.setText(str(v[2]))
            self.kapasite_input.setText(str(v[3]))
            self.salon_input.setText(str(v[4]))

    def _kaydet(self):
        veriler = (self.ders_adi_input.text(), self.antrenor_combo.currentData(), self.ders_saati_input.text(), self.kapasite_input.text(), self.salon_input.text())
        if self.ders_id:
            sorgu_calistir("UPDATE dersler SET ders_adi=%s, antrenor_id=%s, ders_saati=%s, kapasite=%s, salon=%s WHERE ders_id=%s", veriler + (self.ders_id,))
        else:
            sorgu_calistir("INSERT INTO dersler (ders_adi, antrenor_id, ders_saati, kapasite, salon) VALUES (%s, %s, %s, %s, %s)", veriler)
        self.accept()