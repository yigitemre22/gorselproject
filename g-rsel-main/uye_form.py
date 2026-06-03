# -*- coding: utf-8 -*-
# TitanFit Gym – Üye Formu 

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QDateEdit, QTextEdit, QMessageBox, QGridLayout, QWidget
)

from PyQt5.QtCore import Qt, QDate, QRegExp
from PyQt5.QtGui import QRegExpValidator
from tema import uygula_tema
import db_baglanti

# Çerçevesiz penceremize ekleyeceğimiz başlık barını çağırıyoruz
from custom_widgets import CustomTitleBar

class UyeForm(QDialog):
    def __init__(self, uye_id=None, parent=None):
        super().__init__(parent)
        self.uye_id = uye_id
        
        # 1. Stil ve çerçeve ayarları
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(540, 620)
        uygula_tema(self)
        self.setStyleSheet(self.styleSheet() + """
            QDialog { background-color: #0A0A22; border: 2px solid #6C63FF; border-radius: 12px; }
        """)
        
        # 2. ÖNCE Arayüzü oluştur
        self.uyelik_tipleri = self._uyelik_tiplerini_getir()
        self._ui_olustur()
        
        # 3. SONRA verileri doldur (İki metodu tek bir yerde birleştirmelisin)
       
        if self.uye_id:
            self._verileri_getir()
        # 4. İlk açılışta bitiş tarihini otomatik tetikle
        self.bitis_tarihi_hesapla()

    def _uyelik_tiplerini_getir(self):
        try:
            bag = db_baglanti.baglan()
            if not bag: return []
            cur = bag.cursor()
            cur.execute("SELECT uyelik_tip_id, tip_adi, sure_ay FROM uyelik_tipleri")
            tipler = cur.fetchall()
            db_baglanti.baglanti_kapat(bag, cur)
            return tipler
        except Exception as e:
            print(e); return []

    def _ui_olustur(self):
        # 1. Ana pencere düzeni (Sıfıra sıfır margins)
        self.ana_layout = QVBoxLayout(self)
        self.ana_layout.setContentsMargins(0, 0, 0, 0)
        self.ana_layout.setSpacing(0)

        # 2. Üst Siberpunk Başlık Çubuğu
        self.baslik_cubugu = CustomTitleBar(self)
        baslik_metni = "➕  YENİ ÜYE EKLE" if not self.uye_id else "✏️  ÜYE DÜZENLE"
        self.baslik_cubugu.title_label.setText(baslik_metni)
        self.ana_layout.addWidget(self.baslik_cubugu)

        # 3. İÇERİK PANELİ: Arka planın opak olmasını sağlayan ana taşıyıcı widget
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
        
        # İçerik layout'unu DOĞRUDAN form_panel'in içerisine kuruyoruz
        icerik_layout = QVBoxLayout(self.form_panel)
        icerik_layout.setContentsMargins(24, 20, 24, 20)
        icerik_layout.setSpacing(16)

        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)

        def label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-size:11px; color:#7B7BAA; font-weight:700; letter-spacing:1px; background:transparent; border:none;")
            return lbl

        def field(placeholder, h=36):
            f = QLineEdit()
            f.setPlaceholderText(placeholder)
            f.setFixedHeight(h)
            return f

        # Ad / Soyad
        grid.addWidget(label("AD"), 0, 0)
        self.ad_input = field("Ad")
        grid.addWidget(self.ad_input, 0, 1)
        grid.addWidget(label("SOYAD"), 0, 2)
        self.soyad_input = field("Soyad")
        grid.addWidget(self.soyad_input, 0, 3)

        # TC / Telefon
        grid.addWidget(label("TC KİMLİK"), 1, 0)
        self.tc_input = field("11 haneli TC No")
        self.tc_input.setMaxLength(11)
        self.tc_input.setValidator(QRegExpValidator(QRegExp(r"^\d+$"), self))
        grid.addWidget(self.tc_input, 1, 1)
        
        grid.addWidget(label("TELEFON"), 1, 2)
        self.tel_input = field("05XX...")
        self.tel_input.setMaxLength(11)
        self.tel_input.setValidator(QRegExpValidator(QRegExp(r"^\d+$"), self))
        grid.addWidget(self.tel_input, 1, 3)

        # E-posta
        grid.addWidget(label("E-POSTA"), 2, 0)
        self.email_input = field("ornek@email.com")
        grid.addWidget(self.email_input, 2, 1, 1, 3)

        # Doğum Tarihi / Cinsiyet
        grid.addWidget(label("DOĞUM TARİHİ"), 3, 0)
        self.dt_input = QDateEdit()
        self.dt_input.setCalendarPopup(True)
        self.dt_input.setDate(QDate.currentDate().addYears(-20))
        self.dt_input.setFixedHeight(36)
        grid.addWidget(self.dt_input, 3, 1)
        grid.addWidget(label("CİNSİYET"), 3, 2)
        self.cinsiyet_input = QComboBox()
        self.cinsiyet_input.setFixedHeight(36)
        self.cinsiyet_input.addItems(["Erkek","Kadın"])
        grid.addWidget(self.cinsiyet_input, 3, 3)

        # Adres
        grid.addWidget(label("ADRES (OPSİYONEL)"), 4, 0)
        self.adres_input = QTextEdit()
        self.adres_input.setPlaceholderText("Adres belirtmek zorunlu değildir...")
        self.adres_input.setFixedHeight(56)
        grid.addWidget(self.adres_input, 4, 1, 1, 3)

        # Üyelik Tipi
        grid.addWidget(label("ÜYELİK TİPİ"), 5, 0)
        self.uyelik_tip_input = QComboBox()
        self.uyelik_tip_input.setFixedHeight(36)
        for tip in self.uyelik_tipleri:
            self.uyelik_tip_input.addItem(f"{tip[1]} ({tip[2]} Ay)", [tip[0], tip[2]])
        
        self.uyelik_tip_input.currentIndexChanged.connect(self.bitis_tarihi_hesapla)
        grid.addWidget(self.uyelik_tip_input, 5, 1, 1, 3)

        # Başlangıç / Bitiş
        grid.addWidget(label("BAŞLANGIÇ"), 6, 0)
        self.baslangic_input = QDateEdit()
        self.baslangic_input.setCalendarPopup(True)
        self.baslangic_input.setDate(QDate.currentDate())
        self.baslangic_input.setFixedHeight(36)
        self.baslangic_input.dateChanged.connect(self.bitis_tarihi_hesapla)
        grid.addWidget(self.baslangic_input, 6, 1)
        
        grid.addWidget(label("BİTİŞ"), 6, 2)
        self.bitis_input = QDateEdit()
        self.bitis_input.setCalendarPopup(True)
        self.bitis_input.setFixedHeight(36)
        self.bitis_input.setEnabled(False) 
        self.bitis_input.setStyleSheet("QDateEdit { background-color: #141438; color: #8B5CF6; }")
        grid.addWidget(self.bitis_input, 6, 3)

        icerik_layout.addLayout(grid)
        icerik_layout.addStretch()

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
        icerik_layout.addLayout(btn_lay)
        
        # 4. Bütün paneli ana dikey düzene gömüyoruz
        self.ana_layout.addWidget(self.form_panel)

    # Frameless QDialog'larda stil atamasının arka planı ezmesini engelleyen kritik metot
    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter
        from PyQt5.QtWidgets import QStyle, QStyleOption
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)

    # 5. OTOMATİK BİTİŞ TARİHİ HESAPLAMA METODU
    def bitis_tarihi_hesapla(self):
        if self.uyelik_tip_input.currentIndex() == -1:
            return
        
        # ComboBox'a sakladığımız [id, sure_ay] verisini çekiyoruz
        data = self.uyelik_tip_input.currentData()
        if data and isinstance(data, list):
            sure_ay = data[1] # Veritabanından gelen ay süresi (1, 3, 6, 12 vb.)
            baslangic_tarihi = self.baslangic_input.date()
            # Başlangıç tarihine ay süresini ekleyip bitiş tarihini buluyoruz
            bitis_tarihi = baslangic_tarihi.addMonths(sure_ay)
            self.bitis_input.setDate(bitis_tarihi)

    def _verileri_doldur(self):
        try:
            bag = db_baglanti.baglan()
            cur = bag.cursor()
            cur.execute("SELECT * FROM uyeler WHERE uye_id=%s", (self.uye_id,))
            uye = cur.fetchone()
            db_baglanti.baglanti_kapat(bag, cur)
            if uye:
                self.ad_input.setText(uye.get("ad",""))
                self.soyad_input.setText(uye.get("soyad",""))
                self.tc_input.setText(uye.get("tc_no",""))
                self.tel_input.setText(uye.get("telefon",""))
                self.email_input.setText(uye.get("email",""))
                self.cinsiyet_input.setCurrentText(uye.get("cinsiyet","Erkek"))
                self.adres_input.setPlainText(uye.get("adres",""))
                if uye.get("dogum_tarihi"):   self.dt_input.setDate(uye["dogum_tarihi"])
                if uye.get("uyelik_baslangic"): self.baslangic_input.setDate(uye["uyelik_baslangic"])
                
                # ComboBox datasına göre doğru üyelik tipini seçelim
                for i in range(self.uyelik_tip_input.count()):
                    combo_data = self.uyelik_tip_input.itemData(i)
                    if combo_data and combo_data[0] == uye.get("uyelik_tip_id"):
                        self.uyelik_tip_input.setCurrentIndex(i)
                        break
                
                # Bitiş tarihini otomatik hesaplama metodumuz zaten dolduracaktır.
                self.bitis_tarihi_hesapla()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Üye bilgileri alınamadı: {e}")
    def _verileri_getir(self):
        if self.uye_id: # Eğer uye_id varsa düzenleme modundayız
            try:
                bag = db_baglanti.baglan()
                cur = bag.cursor()
                # uyeler tablosundaki tüm sütunları çekiyoruz
                cur.execute("SELECT * FROM uyeler WHERE uye_id=?", (self.uye_id,))
                uye = cur.fetchone()
                
                if uye:
                    # uye[0] = id, uye[1] = ad, uye[2] = soyad vb.
                    # Kendi tablonuzdaki sıra farklıysa buradaki indeksleri güncelleyin
                    self.ad_input.setText(str(uye[1]))
                    self.soyad_input.setText(str(uye[2]))
                    self.tc_input.setText(str(uye[3]))
                    self.tel_input.setText(str(uye[4]))
                    self.email_input.setText(str(uye[5]))
                    # Tarihleri QDate'e çevirip setDate yapıyoruz
                    # self.dt_input.setDate(QDate.fromString(uye[6], "yyyy-MM-dd"))
                    
                    self.adres_input.setPlainText(str(uye[8]))
                    
                    # Cinsiyet gibi ComboBoxlar için:
                    index = self.cinsiyet_input.findText(uye[7])
                    if index != -1: self.cinsiyet_input.setCurrentIndex(index)
                    
                db_baglanti.baglanti_kapat(bag, cur)
            except Exception as e:
                print(f"Veri çekme hatası: {e}")
    def _kaydet(self):
        ad    = self.ad_input.text().strip()
        soyad = self.soyad_input.text().strip()
        tc    = self.tc_input.text().strip()
        tel   = self.tel_input.text().strip()
        email = self.email_input.text().strip()
        adres = self.adres_input.toPlainText().strip()

        # Eksik kontrolü
        if not ad or not soyad or not tc or not tel:
            QMessageBox.warning(self, "Eksik Bilgi", "Ad, Soyad, TC ve Telefon alanları zorunludur.")
            return

        # ComboBox verisi
        secili_data = self.uyelik_tip_input.currentData()
        uyelik_tip_id = secili_data[0] if secili_data else None

        dt        = self.dt_input.date().toString("yyyy-MM-dd")
        baslangic = self.baslangic_input.date().toString("yyyy-MM-dd")
        bitis     = self.bitis_input.date().toString("yyyy-MM-dd")
        cins      = self.cinsiyet_input.currentText()

        try:
            bag = db_baglanti.baglan()
            cur = bag.cursor()
            
            if self.uye_id:
                # GÜNCELLEME (UPDATE)
                cur.execute("""
                    UPDATE uyeler SET ad=?, soyad=?, tc_no=?, telefon=?, email=?,
                    dogum_tarihi=?, cinsiyet=?, adres=?, uyelik_tip_id=?,
                    uyelik_baslangic=?, uyelik_bitis=? WHERE uye_id=?
                """, (ad, soyad, tc, tel, email, dt, cins, adres, uyelik_tip_id, baslangic, bitis, self.uye_id))
            else:
                # EKLEME (INSERT) - 'durum' sütunu kaldırıldı
                cur.execute("""
                    INSERT INTO uyeler (ad, soyad, tc_no, telefon, email, dogum_tarihi,
                    cinsiyet, adres, uyelik_tip_id, uyelik_baslangic, uyelik_bitis)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (ad, soyad, tc, tel, email, dt, cins, adres, uyelik_tip_id, baslangic, bitis))
            
            bag.commit()
            QMessageBox.information(self, "Başarılı", "İşlem başarıyla kaydedildi.")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Hata detayı: {e}")
        finally:
            if 'bag' in locals() and bag:
                bag.close()