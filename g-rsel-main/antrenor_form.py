# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QPainter
from custom_widgets import CustomTitleBar
from db_baglanti import sorgu_calistir  # Projenin gerçek DB modülü

class AntrenorForm(QDialog):
    def __init__(self, antrenor_id=None, parent=None):
        super().__init__(parent)
        self.antrenor_id = antrenor_id
        
        # BEYAZ WINDOWS BARINI SİLME VE SİBERPUNK TRANSPARANLIK AYARI
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(500, 480)
        
        self._ui_olustur()
        
        if self.antrenor_id:
            self._bilgileri_getir()

    def _ui_olustur(self):
        ana_layout = QVBoxLayout(self)
        ana_layout.setContentsMargins(0, 0, 0, 0)
        ana_layout.setSpacing(0)

        # Siberpunk Özel Başlık Çubuğu
        self.baslik_cubugu = CustomTitleBar(self)
        baslik_metni = "➕  YENİ ANTRENÖR EKLE" if not self.antrenor_id else "✏️  ANTRENÖR DÜZENLE"
        self.baslik_cubugu.title_label.setText(baslik_metni)
        ana_layout.addWidget(self.baslik_cubugu)

        # Koyu Neon Panel Yapısı (Üye Formundaki Stil)
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
            f.setStyleSheet("""
                QLineEdit {
                    background-color: #141438;
                    border: 1px solid #1E1E4A;
                    border-radius: 6px;
                    color: #E8E8FF;
                    padding-left: 10px;
                }
                QLineEdit:focus {
                    border: 1px solid #6C63FF;
                }
            """)
            return f

        # Form İnput Elemanları
        grid.addWidget(label("AD"), 0, 0)
        self.ad_input = field("Ad")
        grid.addWidget(self.ad_input, 0, 1)

        grid.addWidget(label("SOYAD"), 1, 0)
        self.soyad_input = field("Soyad")
        grid.addWidget(self.soyad_input, 1, 1)

        grid.addWidget(label("UZMANLIK"), 2, 0)
        self.uzmanlik_input = field("Örn: Fitness, Yoga, Boks")
        grid.addWidget(self.uzmanlik_input, 2, 1)

        # TELEFON (05XX... Şablonu ve Rakam Kısıtlaması)
        grid.addWidget(label("TELEFON"), 3, 0)
        self.tel_input = field("05XX...")
        self.tel_input.setMaxLength(11)
        self.tel_input.setValidator(QRegExpValidator(QRegExp(r"^\d+$"), self))
        grid.addWidget(self.tel_input, 3, 1)

        grid.addWidget(label("E-POSTA"), 4, 0)
        self.email_input = field("ornek@email.com")
        grid.addWidget(self.email_input, 4, 1)

        grid.addWidget(label("MAAŞ (₺)"), 5, 0)
        self.maas_input = field("Maaş miktarı")
        grid.addWidget(self.maas_input, 5, 1)

        # SİSTEM HATASINI ÇÖZEN GİZLİ INPUT (Admin panelin çökmesini önler)
        self.sifre_input = QLineEdit()
        self.sifre_input.setVisible(False)

        icerik_layout.addLayout(grid)
        icerik_layout.addStretch()

        # Siberpunk Buton Grubu
        btn_lay = QHBoxLayout()
        btn_lay.setSpacing(10)
        
        iptal_btn = QPushButton("İptal")
        iptal_btn.setFixedHeight(40)
        iptal_btn.setCursor(Qt.PointingHandCursor)
        iptal_btn.setStyleSheet("background-color: #141438; color: #7B7BAA; border: 1px solid #1E1E4A; border-radius: 6px; font-weight:700;")
        iptal_btn.clicked.connect(self.reject)
        
        kaydet_btn = QPushButton("  Kaydet  →")
        kaydet_btn.setFixedHeight(40)
        kaydet_btn.setCursor(Qt.PointingHandCursor)
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

    def _bilgileri_getir(self):
        # Sorguda %s yerine ? kullanıldı
        res = sorgu_calistir("SELECT ad, soyad, uzmanlik, telefon, email, maas FROM antrenorler WHERE antrenor_id=?", (self.antrenor_id,))
        
        # sorgu_calistir metodunuzun döndürdüğü yapıya göre (genellikle bir liste döner)
        if res:
            # Eğer res bir liste dönüyorsa ve ilk elemanı satırsa:
            veriler = res[0] 
            self.ad_input.setText(str(veriler[0]))
            self.soyad_input.setText(str(veriler[1]))
            self.uzmanlik_input.setText(str(veriler[2]))
            self.tel_input.setText(str(veriler[3]))
            self.email_input.setText(str(veriler[4]))
            self.maas_input.setText(str(veriler[5]))

    def _kaydet(self):
        # 1. Verileri topla
        veriler = (
            self.ad_input.text(), 
            self.soyad_input.text(), 
            self.uzmanlik_input.text(), 
            self.tel_input.text(), 
            self.email_input.text(), 
            self.maas_input.text()
        )
        
        if self.antrenor_id:
            # GÜNCELLEME: %s yerine ? kullanıldı
            # Sıralamaya dikkat: veriler + id
            sorgu_calistir(
                "UPDATE antrenorler SET ad=?, soyad=?, uzmanlik=?, telefon=?, email=?, maas=? WHERE antrenor_id=?", 
                veriler + (self.antrenor_id,)
            )
        else:
            # EKLEME: %s yerine ? kullanıldı
            sorgu_calistir(
                "INSERT INTO antrenorler (ad, soyad, uzmanlik, telefon, email, maas) VALUES (?, ?, ?, ?, ?, ?)", 
                veriler
            )
        self.accept()