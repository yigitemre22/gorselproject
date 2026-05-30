# -*- coding: utf-8 -*-
# TitanFit Gym – Antrenör Paneli 

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QStackedWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QGridLayout, QApplication,
    QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor

from tema import uygula_tema
import db_baglanti
from custom_widgets import CustomTitleBar, HudCard

from tema import uygula_tema, RENKLER

class SidebarBtn(QPushButton):
    def __init__(self, ikon, metin):
        super().__init__(f"  {ikon}   {metin}")
        self.setCheckable(True)
        self.setFixedHeight(46)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding-left: 12px;
                font-size: 13px;
                font-weight: 500;
                color: #555580;
            }
            QPushButton:hover {
                background: rgba(59,130,246,0.12);
                color: #93C5FD;
            }
            QPushButton:checked {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 rgba(59,130,246,0.30), stop:1 rgba(107,99,255,0.15));
                color: #BAE6FD;
                font-weight: 700;
                border-left: 3px solid #3B82F6;
            }
        """)


def tablo_olustur(sutunlar):
    t = QTableWidget()
    t.setColumnCount(len(sutunlar))
    t.setHorizontalHeaderLabels(sutunlar)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.setEditTriggers(QTableWidget.NoEditTriggers)
    t.setSelectionBehavior(QTableWidget.SelectRows)
    t.setAlternatingRowColors(True)
    t.verticalHeader().setVisible(False)
    t.setShowGrid(False)
    return t


def tabloyu_doldur(tablo, satirlar):
    tablo.setRowCount(len(satirlar))
    for i, satir in enumerate(satirlar):
        for j, deger in enumerate(satir):
            item = QTableWidgetItem(str(deger) if deger is not None else "—")
            item.setTextAlignment(Qt.AlignCenter)
            tablo.setItem(i, j, item)


def sorgu_calistir(sql, params=None):
    try:
        bag = db_baglanti.baglan()
        if not bag:
            return []
        cur = bag.cursor()
        cur.execute(sql, params or ())
        sonuc = cur.fetchall()
        db_baglanti.baglanti_kapat(bag, cur)
        return sonuc
    except Exception as e:
        print(f"[DB] {e}")
        return []


class AntrenorPanel(QWidget):
    def __init__(self, antrenor):
        super().__init__()
        self.antrenor = antrenor
        self.antrenor_id = antrenor.get("antrenor_id")
        self.aktif_btn = None

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("TitanFit Gym – Antrenör Paneli")
        self.setMinimumSize(1300, 820)

        uygula_tema(self)
        self._ui_olustur()

    def _ui_olustur(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 14, 14)

        bg = QFrame()
        bg.setObjectName("bg_frame")
        bg.setStyleSheet("""
            QFrame#bg_frame {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #07071A, stop:0.5 #0A0A22, stop:1 #07071A);
                border: 1px solid #3B82F6;
                border-radius: 14px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(59, 130, 246, 130))
        shadow.setOffset(0, 0)
        bg.setGraphicsEffect(shadow)

        bg_lay = QVBoxLayout(bg)
        bg_lay.setContentsMargins(0, 0, 0, 0)
        bg_lay.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        bg_lay.addWidget(self.title_bar)

        main = QHBoxLayout()
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # SIDEBAR
        sidebar = QFrame()
        sidebar.setFixedWidth(230)
        sidebar.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 #0A0A22, stop:1 #07071A);
                border-right: 1px solid #1E1E4A;
                border-bottom-left-radius: 14px;
            }
        """)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(12, 22, 12, 20)
        sb.setSpacing(3)

        logo_frame = QFrame()
        logo_frame.setStyleSheet("""
            QFrame {
                background: rgba(59,130,246,0.08);
                border: 1px solid rgba(59,130,246,0.20);
                border-radius: 10px;
            }
        """)
        lf_lay = QVBoxLayout(logo_frame)
        lf_lay.setContentsMargins(10, 14, 10, 14)
        lf_lay.setSpacing(4)

        logo = QLabel("⬡")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size:34px; color:#3B82F6; background:transparent; border:none;")
        gym_lbl = QLabel("TitanFit Gym")
        gym_lbl.setAlignment(Qt.AlignCenter)
        gym_lbl.setStyleSheet("font-size:13px; font-weight:800; color:#93C5FD; background:transparent; border:none; letter-spacing:1px;")
        user_lbl = QLabel(f"👤  {self.antrenor.get('ad','')} {self.antrenor.get('soyad','')}")
        user_lbl.setAlignment(Qt.AlignCenter)
        user_lbl.setStyleSheet("font-size:11px; color:#555580; background:transparent; border:none;")
        rol_lbl = QLabel("Antrenör")
        rol_lbl.setAlignment(Qt.AlignCenter)
        rol_lbl.setStyleSheet("font-size:10px; color:#3B82F6; font-weight:700; letter-spacing:2px; background:transparent; border:none;")

        lf_lay.addWidget(logo)
        lf_lay.addWidget(gym_lbl)
        lf_lay.addWidget(user_lbl)
        lf_lay.addWidget(rol_lbl)
        sb.addWidget(logo_frame)
        sb.addSpacing(18)

        menu_lbl = QLabel("MENÜ")
        menu_lbl.setStyleSheet("font-size:10px; color:#2E2E5E; font-weight:700; letter-spacing:2px; padding-left:8px; background:transparent; border:none;")
        sb.addWidget(menu_lbl)
        sb.addSpacing(6)

        self.menu_btnleri = []
        menuler = [
            ("📊", "Dashboard",      0),
            ("📅", "Derslerim",      1),
            ("👥", "Üyelerim",       2),
            ("📈", "Gelişim Takibi", 3),
            ("🚪", "Giriş/Çıkış",    4),
        ]
        for ikon, metin, idx in menuler:
            btn = SidebarBtn(ikon, metin)
            btn.clicked.connect(lambda _, i=idx, b=btn: self._sayfa(i, b))
            sb.addWidget(btn)
            self.menu_btnleri.append(btn)

        sb.addStretch()

        cikis = QPushButton("  🚪   Çıkış Yap")
        cikis.setFixedHeight(42)
        cikis.setCursor(Qt.PointingHandCursor)
        cikis.setStyleSheet("""
            QPushButton {
                background: rgba(239,68,68,0.10);
                border: 1px solid rgba(239,68,68,0.35);
                border-radius: 8px;
                color: #EF4444;
                font-size: 13px;
                font-weight: 700;
                text-align: left;
                padding-left: 16px;
            }
            QPushButton:hover {
                background: rgba(239,68,68,0.22);
                border-color: #EF4444;
            }
        """)
        cikis.clicked.connect(self._cikis)
        sb.addWidget(cikis)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: #08081E;")

        for fn in [self._dashboard, self._derslerim,
                   self._uyelerim, self._gelisim, self._giris_cikis]:
            self.stack.addWidget(fn())

        main.addWidget(sidebar)
        main.addWidget(self.stack)
        self._sayfa(0, self.menu_btnleri[0])

        bg_lay.addLayout(main)
        outer.addWidget(bg)

    def _sayfa(self, idx, btn):
        if self.aktif_btn:
            self.aktif_btn.setChecked(False)
        btn.setChecked(True)
        self.aktif_btn = btn
        self.stack.setCurrentIndex(idx)

    def _cikis(self):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Çıkış")
        msg.setText("Çıkmak istiyor musunuz?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        msg.setWindowFlags(msg.windowFlags() | Qt.FramelessWindowHint)
        msg.setStyleSheet(f"""
            QMessageBox {{ background-color: {RENKLER['bg_panel']}; border: 2px solid {RENKLER['border_focus']}; border-radius: 12px; }}
            QMessageBox QLabel {{ color: {RENKLER['metin_ana']}; background: transparent; padding-top: 10px; }}
            QMessageBox QPushButton {{ background: transparent; border: 1.5px solid {RENKLER['mor_parlak']}; border-radius: 6px; padding: 8px 22px; font-weight: 700; color: {RENKLER['mor_acik']}; min-width: 80px; }}
            QMessageBox QPushButton:hover {{ background: {RENKLER['grad_buton']}; color: white; border-color: transparent; }}
        """)

        sonuc = msg.exec_()
        if sonuc == QMessageBox.Yes:
            try:
                # 1. Giriş ekranının olduğu python dosyasını buraya import et
                # NOT: Dosya adın 'login.py' ve sınıfın 'GirisEkrani' ise ona göre düzenle:
                from giris import LoginWindow 
                
                # 2. Yeni bir giriş ekranı nesnesi oluştur ve göster
                self.giris_penceresi = LoginWindow()
                self.giris_penceresi.show()
                
                # 3. Mevcut admin panelini Kapat (Uygulamayı değil, sadece bu pencereyi)
                self.close()
                
            except Exception as e:
                # Eğer import veya sınıf adında hata yaparsan terminale yazması için:
                print(f"Giriş ekranına dönerken hata oluştu: {e}")

    def _sayfa_widget(self, baslik):
        w = QWidget()
        w.setStyleSheet("background: #08081E;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(16)
        title = QLabel(baslik)
        title.setObjectName("title")
        title.setStyleSheet("""
            font-size: 22px; font-weight: 900; color: #93C5FD;
            letter-spacing: 1px; padding-bottom: 6px;
            border-bottom: 1px solid #1E1E4A;
            background: transparent;
        """)
        lay.addWidget(title)
        return w, lay

    # DASHBOARD
    def _dashboard(self):
        w, lay = self._sayfa_widget("📊  Dashboard")

        ders_say = sorgu_calistir(
            "SELECT COUNT(*) FROM dersler WHERE antrenor_id=%s", (self.antrenor_id,))
        uye_say = sorgu_calistir(
            "SELECT COUNT(*) FROM uye_Antrenor WHERE antrenor_id=%s", (self.antrenor_id,))
        d = ders_say[0][0] if ders_say else 0
        u = uye_say[0][0] if uye_say else 0

        kl = QHBoxLayout(); kl.setSpacing(14)
        kl.addWidget(HudCard("DERSLERİM", d, "📅", "#6C63FF"))
        kl.addWidget(HudCard("ÜYELERİM",  u, "👥", "#3B82F6"))
        kl.addStretch()
        lay.addLayout(kl)

        prog_lbl = QLabel("📅  Ders Programım")
        prog_lbl.setObjectName("panelText")
        prog_lbl.setStyleSheet("font-size:15px; font-weight:bold; color:#93C5FD; background:transparent; border:none;")
        lay.addWidget(prog_lbl)

        t = tablo_olustur(["Ders Adı","Saat","Kapasite","Salon"])
        rows = sorgu_calistir(
            "SELECT ders_adi,ders_saati,kapasite,salon FROM dersler WHERE antrenor_id=%s",
            (self.antrenor_id,))
        tabloyu_doldur(t, rows)
        lay.addWidget(t)
        return w

    # DERSLERİM
    def _derslerim(self):
        w, lay = self._sayfa_widget("📅  Derslerim")
        t = tablo_olustur(["Ders ID","Ders Adı","Saat","Kapasite","Salon"])
        rows = sorgu_calistir(
            "SELECT ders_id,ders_adi,ders_saati,kapasite,salon FROM dersler WHERE antrenor_id=%s",
            (self.antrenor_id,))
        tabloyu_doldur(t, rows)
        lay.addWidget(t)

        kayitli_lbl = QLabel("👥  Derslerime Kayıtlı Üyeler")
        kayitli_lbl.setStyleSheet("font-size:15px; font-weight:bold; color:#93C5FD; background:transparent; border:none; margin-top:8px;")
        lay.addWidget(kayitli_lbl)

        t2 = tablo_olustur(["Üye Adı","Üye Soyadı","Ders Adı","Kayıt Tarihi"])
        rows2 = sorgu_calistir("""
            SELECT uy.ad, uy.soyad, d.ders_adi, ud.kayit_tarihi
            FROM uyeDers ud
            JOIN uyeler uy ON ud.uye_id=uy.uye_id
            JOIN dersler d  ON ud.ders_id=d.ders_id
            WHERE d.antrenor_id=%s
            ORDER BY ud.kayit_tarihi DESC
        """, (self.antrenor_id,))
        tabloyu_doldur(t2, rows2)
        lay.addWidget(t2)
        return w

    # ÜYELERİM
    def _uyelerim(self):
        w, lay = self._sayfa_widget("👥  Üyelerim")
        t = tablo_olustur(["Ad","Soyad","Telefon","E-posta","Üyelik Tipi","Bitiş","Durum"])
        rows = sorgu_calistir("""
            SELECT uy.ad, uy.soyad, uy.telefon, uy.email,
                   ut.tip_adi, uy.uyelik_bitis, uy.durum
            FROM uye_Antrenor ua
            JOIN uyeler uy ON ua.uye_id=uy.uye_id
            LEFT JOIN uyelik_tipleri ut ON uy.uyelik_tip_id=ut.uyelik_tip_id
            WHERE ua.antrenor_id=%s
        """, (self.antrenor_id,))
        tabloyu_doldur(t, rows)
        lay.addWidget(t)
        return w

    # GELİŞİM TAKİBİ
    def _gelisim(self):
        w, lay = self._sayfa_widget("📈  Üye Gelişim Takibi")
        t = tablo_olustur(["Ad","Soyad","Kilo (kg)","Boy (cm)","Yağ Oranı (%)","Tarih"])
        rows = sorgu_calistir("""
            SELECT uy.ad, uy.soyad, g.kilo, g.boy, g.yag_orani, g.kayit_tarihi
            FROM gelisim g
            JOIN uyeler uy ON g.uye_id=uy.uye_id
            JOIN uye_Antrenor ua ON uy.uye_id=ua.uye_id
            WHERE ua.antrenor_id=%s
            ORDER BY g.kayit_tarihi DESC
        """, (self.antrenor_id,))
        tabloyu_doldur(t, rows)
        lay.addWidget(t)
        return w

    # GİRİŞ / ÇIKIŞ
    def _giris_cikis(self):
        w, lay = self._sayfa_widget("🚪  Üye Giriş/Çıkış Kayıtları")
        t = tablo_olustur(["Ad","Soyad","Giriş Saati","Çıkış Saati"])
        rows = sorgu_calistir("""
            SELECT uy.ad, uy.soyad, gck.giris_saati, gck.cikis_saati
            FROM girisCikisKayitlari gck
            JOIN uyeler uy ON gck.uye_id=uy.uye_id
            JOIN uye_Antrenor ua ON uy.uye_id=ua.uye_id
            WHERE ua.antrenor_id=%s
            ORDER BY gck.giris_saati DESC
        """, (self.antrenor_id,))
        tabloyu_doldur(t, rows)
        lay.addWidget(t)
        return w