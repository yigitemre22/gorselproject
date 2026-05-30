# -*- coding: utf-8 -*-
# TitanFit Gym – Admin Paneli 

import csv
import traceback
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from uye_form import UyeForm
from custom_widgets import siber_mesaj
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFrame, QStackedWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QGridLayout, QSizePolicy,
    QApplication, QGraphicsDropShadowEffect, QFileDialog,
    QGraphicsOpacityEffect, QAbstractItemView
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.QtGui import QColor

from tema import uygula_tema, RENKLER
import db_baglanti
from custom_widgets import CustomTitleBar, CircularProgress, HudCard, ToastNotification


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
                border-left: 3px solid transparent;
                border-radius: 8px;
                text-align: left;
                padding-left: 12px;
                font-size: 13px;
                font-weight: 700;
                color: #555580;
            }

            QPushButton:hover {
                background: rgba(107, 99, 255, 0.12);
                color: #A78BFA;
            }

            QPushButton:checked {
                background: qlineargradient(
                    x1:0,y1:0,x2:1,y2:0,
                    stop:0 rgba(107,99,255,0.30),
                    stop:1 rgba(59,130,246,0.15)
                );
                color: #C4B5FD;
                 border-left: 3px solid #8B5CF6;
            }
            """)
        
def uyelik_durumlarini_guncelle():
    try:
        bag = db_baglanti.baglan()
        cur = bag.cursor()
        cur.execute("""
            UPDATE uyeler 
            SET durum = 'pasif' 
            WHERE uyelik_bitis < CURDATE() 
            AND durum = 'aktif'
        """)
        bag.commit()
        db_baglanti.baglanti_kapat(bag, cur)
    except Exception as e:
        print(f"[HATA] Üyelik güncelleme: {e}")

def tablo_olustur(sutunlar):
    t = QTableWidget()
    t.setColumnCount(len(sutunlar))
    t.setHorizontalHeaderLabels(sutunlar)
    
    # Tüm satırı seçtir ve tekli seçimi aktif et
    t.setSelectionBehavior(QAbstractItemView.SelectRows)
    t.setSelectionMode(QAbstractItemView.SingleSelection)
    
    # Hücre odaklanma efektini tamamen kapat
    t.setFocusPolicy(Qt.NoFocus) 
    
    t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    t.setEditTriggers(QTableWidget.NoEditTriggers)
    t.setAlternatingRowColors(True)
    t.verticalHeader().setVisible(False)
    t.setShowGrid(False)
    
    # GÜNCELLENEN SİBERPUNK CSS (Hücre odağı ve sütun işaretleri kaldırıldı)
    t.setStyleSheet("""
        QTableWidget {
            background-color: #0F0F35;
            gridline-color: #1E1E4A;
            color: #E8E8FF;
            border: 1px solid #6C63FF;
            border-radius: 8px;
            outline: none; /* Genel odak çerçevesini kaldırır */
        }
        QTableWidget::item {
            padding: 5px;
        }
        /* Seçilen satırın tamamı tek kalıp halinde neon mor parlasın */
        QTableWidget::item:selected {
            background-color: rgba(108, 99, 255, 0.25) !important;
            color: #A78BFA !important;
            border-top: 1px solid #6C63FF;
            border-bottom: 1px solid #6C63FF;
        }
        /* Tıklanan hücrenin içindeki o sinir bozucu sütun/hücre seçilme işaretini yok eder */
        QTableWidget::item:focus {
            background-color: rgba(108, 99, 255, 0.25) !important;
            color: #A78BFA !important;
            border: none;
            outline: none;
        }
    """)
    
    return t

def tabloyu_doldur(tablo, satirlar, renkli_sutun=None):
    tablo.setRowCount(len(satirlar))
    for i, satir in enumerate(satirlar):
        for j, deger in enumerate(satir):
            item = QTableWidgetItem(str(deger) if deger is not None else "—")
            item.setTextAlignment(Qt.AlignCenter)
            if renkli_sutun and j == renkli_sutun:
                renk = "#10B981" if str(deger) == "aktif" else "#EF4444"
                item.setForeground(QColor(renk))
            tablo.setItem(i, j, item)


def sorgu_calistir(sql, params=None):
    try:
        bag = db_baglanti.baglan()
        if not bag:
            return []
        cur = bag.cursor()
        cur.execute(sql, params or ())
        
        # SELECT sorguları için fetchall, diğerleri için commit
        if sql.strip().upper().startswith("SELECT"):
            sonuc = cur.fetchall()
        else:
            bag.commit()  # ← BU SATIR EKSİKTİ
            sonuc = []
        
        db_baglanti.baglanti_kapat(bag, cur)
        return sonuc
    except Exception as e:
        print(f"[DB] {e}")
        return []


def aksiyon_bar_olustur(butonlar):
    """butonlar: list of (metin, obj_name, callback)"""
    frame = QFrame()
    frame.setFixedHeight(54)
    frame.setStyleSheet("""
        QFrame {
            background: rgba(9,9,32,0.60);
            border: 1px solid #1E1E4A;
            border-radius: 8px;
        }
    """)
    lay = QHBoxLayout(frame)
    lay.setContentsMargins(12, 8, 12, 8)
    lay.setSpacing(10)
    for metin, obj_name, callback in butonlar:
        btn = QPushButton(metin)
        if obj_name:
            btn.setObjectName(obj_name)
        btn.setFixedHeight(36)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.setMinimumWidth(btn.fontMetrics().horizontalAdvance(metin) + 44)
        if callback:
            btn.clicked.connect(callback)
        lay.addWidget(btn)
    lay.addStretch()
    return frame


class AdminPanel(QWidget):
    def __init__(self, kullanici):
        super().__init__()
        self.kullanici = kullanici
        self.aktif_btn = None
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("TitanFit Gym – Admin Paneli")
        self.setMinimumSize(1300, 820)
        uygula_tema(self)
        self._ui_olustur()

    def _ui_olustur(self):
        # Açılışta bitiş tarihi geçmiş üyeleri pasife al
        uyelik_durumlarini_guncelle()

# Her saat otomatik kontrol
        self.uyelik_timer = QTimer(self)
        self.uyelik_timer.timeout.connect(uyelik_durumlarini_guncelle)
        self.uyelik_timer.start(60 * 60 * 1000)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 14, 14, 14)

        bg = QFrame()
        bg.setObjectName("bg_frame")
        bg.setStyleSheet("""
            QFrame#bg_frame {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #07071A, stop:0.5 #0A0A22, stop:1 #07071A);
                border: 1px solid #6C63FF;
                border-radius: 14px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(108, 99, 255, 140))
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
                background: rgba(107,99,255,0.08);
                border: 1px solid rgba(107,99,255,0.20);
                border-radius: 10px;
            }
        """)
        lf_lay = QVBoxLayout(logo_frame)
        lf_lay.setContentsMargins(10, 14, 10, 14)
        lf_lay.setSpacing(4)

        logo = QLabel("⬡")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size: 34px; color: #6C63FF; background: transparent; border: none;")
        gym_lbl = QLabel("TitanFit Gym")
        gym_lbl.setAlignment(Qt.AlignCenter)
        gym_lbl.setStyleSheet("font-size: 13px; font-weight: 800; color: #A78BFA; background: transparent; border: none; letter-spacing: 1px;")
        user_lbl = QLabel(f"👤  {self.kullanici.get('ad','')} {self.kullanici.get('soyad','')}")
        user_lbl.setAlignment(Qt.AlignCenter)
        user_lbl.setStyleSheet("font-size: 11px; color: #555580; background: transparent; border: none;")

        lf_lay.addWidget(logo)
        lf_lay.addWidget(gym_lbl)
        lf_lay.addWidget(user_lbl)
        sb.addWidget(logo_frame)
        sb.addSpacing(18)

        menu_lbl = QLabel("MENÜ")
        menu_lbl.setStyleSheet("font-size: 10px; color: #2E2E5E; font-weight: 700; letter-spacing: 2px; padding-left: 8px; background: transparent; border: none;")
        sb.addWidget(menu_lbl)
        sb.addSpacing(6)

        self.menu_btnleri = []
        menuler = [
            ("📊", "Dashboard",       0),
            ("👥", "Üyeler",          1),
            ("🏋", "Antrenörler",     2),
            ("📅", "Dersler",         3),
            ("💰", "Ödemeler",        4),
            ("🔧", "Ekipmanlar",      5),
            ("📦", "Stoklar",         6),
            ("💼", "Kasa & Giderler", 7),
            ("📄", "Raporlar",        8),
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

        for fn in [self._dashboard, self._uyeler, self._antrenorler,
                   self._dersler, self._odemeler, self._ekipmanlar,
                   self._stoklar, self._kasa, self._raporlar]:
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

        # Efekti oluşturuyoruz
        self.fade_effect = QGraphicsOpacityEffect(self.stack)
        self.stack.setGraphicsEffect(self.fade_effect)
        
        self.anim = QPropertyAnimation(self.fade_effect, b"opacity")
        self.anim.setDuration(140)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)

        def _on_fade_out():
            self.stack.setCurrentIndex(idx)
            self.anim.disconnect()
            self.anim.setStartValue(0.0)
            self.anim.setEndValue(1.0)
            
            # ── İŞTE KRİTİK DÜZELTME ──
            # Sayfa görünür olduktan sonra efekti kapatıyoruz ki mouse koordinatları sapıtmasın
            self.anim.finished.connect(lambda: self.fade_effect.setEnabled(False))
            # ──────────────────────────
            
            self.anim.start()
            if idx == 0:
                self._dashboard_yenile()
            elif idx == 7:
                self._kasa_yenile()

        self.anim.finished.connect(_on_fade_out)
        self.anim.start()

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
            font-size: 22px; font-weight: 900; color: #A78BFA;
            letter-spacing: 1px; padding-bottom: 6px;
            border-bottom: 1px solid #1E1E4A;
            background: transparent;
        """)
        lay.addWidget(title)
        return w, lay

    # DASHBOARD
    # DASHBOARD
    # DASHBOARD
    # DASHBOARD
    def _dashboard(self):
        w, lay = self._sayfa_widget("📊  Dashboard")
        
        # Üst panel için ana yatay düzen
        hud = QHBoxLayout()
        hud.setSpacing(20)
        hud.setContentsMargins(0, 0, 0, 0)
        
        # 1. Daire Grafiği (Sol Taraf)
        self.cp = CircularProgress(0, "AKTİF ÜYELER", "#8B5CF6")
        # Hem minimum hem maksimumu eşitleyerek Qt'nin boyutla oynamasını tamamen engelliyoruz
        self.cp.setMinimumSize(160, 160)
        self.cp.setMaximumSize(160, 160)
        hud.addWidget(self.cp, alignment=Qt.AlignVCenter) # Dikeyde ortala
        
        # 2. Hud Kartları (Sağ Taraf)
        kg = QGridLayout()
        kg.setSpacing(14)
        kg.setContentsMargins(0, 0, 0, 0)
        
        self.dash_kart1 = HudCard("TOPLAM ÜYE",      0,   "👥", "#6C63FF")
        self.dash_kart2 = HudCard("BU AY GELİR (₺)", "0", "💰", "#3B82F6")
        self.dash_kart3 = HudCard("AKTİF ANTRENÖR",  0,   "🏋", "#A78BFA")
        
        # Kartların yüksekliklerini kesin olarak kilitliyoruz
        for kart in [self.dash_kart1, self.dash_kart2, self.dash_kart3]:
            kart.setMinimumHeight(130)
            kart.setMaximumHeight(130)
            kart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        kg.addWidget(self.dash_kart1, 0, 0)
        kg.addWidget(self.dash_kart2, 0, 1)
        kg.addWidget(self.dash_kart3, 0, 2)
        
        hud.addLayout(kg)
        lay.addLayout(hud)
        
        # Tablo başlığı
        son_lbl = QLabel("🕐  Son Kayıtlı Üyeler")
        son_lbl.setObjectName("panelText")
        son_lbl.setStyleSheet("font-size: 14px; font-weight: 700; color: #A78BFA; margin-top: 10px;")
        lay.addWidget(son_lbl)
        
        # 3. Tablo
        self.dash_tablo = tablo_olustur(["Ad", "Soyad", "Telefon", "Üyelik Tipi", "Başlangıç"])
        # Tabloya dikeyde büyüyebildiği kadar büyü diyoruz
        self.dash_tablo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        lay.addWidget(self.dash_tablo)
        
        self._dashboard_yenile()
        return w

    def _dashboard_yenile(self):
        rows = sorgu_calistir("""
            SELECT (SELECT COUNT(*) FROM uyeler),
                   (SELECT COUNT(*) FROM uyeler WHERE durum='aktif'),
                   (SELECT IFNULL(SUM(tutar),0) FROM odemeler
                    WHERE MONTH(odeme_tarihi)=MONTH(NOW()) AND YEAR(odeme_tarihi)=YEAR(NOW())),
                   (SELECT COUNT(*) FROM antrenorler)
        """)
        toplam, aktif, gelir, ant = rows[0] if rows else (0, 0, 0, 0)
        self.cp.guncelle(aktif)
        self.dash_kart1.guncelle(toplam)
        self.dash_kart2.guncelle(f"{float(gelir):,.0f}")
        self.dash_kart3.guncelle(ant)
        rows2 = sorgu_calistir("""
            SELECT u.ad, u.soyad, u.telefon, ut.tip_adi, u.uyelik_baslangic
            FROM uyeler u LEFT JOIN uyelik_tipleri ut ON u.uyelik_tip_id=ut.uyelik_tip_id
            ORDER BY u.kayit_tarihi DESC LIMIT 10
        """)
        tabloyu_doldur(self.dash_tablo, rows2)

    # ÜYELER
    def _uyeler_yenile(self):
        rows = sorgu_calistir("""
            SELECT u.uye_id, u.ad, u.soyad, u.telefon, u.email,
                   ut.tip_adi, u.uyelik_bitis, u.durum
            FROM uyeler u LEFT JOIN uyelik_tipleri ut ON u.uyelik_tip_id=ut.uyelik_tip_id
            ORDER BY u.uye_id DESC
        """)
        tabloyu_doldur(self.uye_tablo, rows, renkli_sutun=7)

    def _uye_ekle(self):
        from uye_form import UyeForm
        f = UyeForm(parent=self)
        if f.exec_(): self._uyeler_yenile()

    def _uye_duzenle(self):
        sel = self.uye_tablo.selectedItems()
        # KORUMA: Eğer tablodan hiçbir şeye tıklanmadıysa şık siberpunk uyarı ver ve dur!
        if not sel:
            siber_mesaj("Seçim Eksik", "Düzenleme yapabilmek için lütfen tablodan bir üye satırına tıklayın.", "uyari", self)
            return
            
        secili_satir = sel[0].row()
        uid = self.uye_tablo.item(secili_satir, 0).text()
        
        # Formu açma kodların...
        form = UyeForm(uye_id=uid, parent=self)
        if form.exec_():
            self._uyeler_yenile()

    def _uye_sil(self):
        sel = self.uye_tablo.selectedItems()
        if not sel:
            siber_mesaj("Seçim Eksik", "Silmek için lütfen tablodan bir üye seçin.", "uyari", self)
            return  # ← return if bloğunun İÇİNDE olmalı
        
        secili_satir = sel[0].row()
        uid = self.uye_tablo.item(secili_satir, 0).text()
        ad  = self.uye_tablo.item(secili_satir, 1).text()
        
        if siber_mesaj("Üye Silme Onayı", f"{ad} isimli üyeyi ve sistemdeki tüm kayıtlarını silmek istiyor musunuz?", "soru", self):
            try:
                bag = db_baglanti.baglan()
                cur = bag.cursor()
                cur.execute("SET FOREIGN_KEY_CHECKS = 0")
                cur.execute("DELETE FROM uyeler WHERE uye_id = %s", (uid,))
                cur.execute("SET FOREIGN_KEY_CHECKS = 1")
                bag.commit()
                db_baglanti.baglanti_kapat(bag, cur)
                self.uye_tablo.removeRow(secili_satir)
                ToastNotification(self, f"{ad} başarıyla silindi.", "basari").goster()
                if hasattr(self, '_dashboard_yenile'):
                    self._dashboard_yenile()
            except Exception as e:
                try:
                    bag2 = db_baglanti.baglan()
                    cur2 = bag2.cursor()
                    cur2.execute("SET FOREIGN_KEY_CHECKS = 1")
                    bag2.commit()
                    db_baglanti.baglanti_kapat(bag2, cur2)
                except:
                    pass
                siber_mesaj("Sistem Hatası", f"Veritabanı hatası oluştu:\n{e}", "hata", self)

    def _uyeler(self):
        w, lay = self._sayfa_widget("👥  Üye Yönetimi")
        lay.addWidget(aksiyon_bar_olustur([
            ("➕  Yeni Üye Ekle", "btnBasari",  self._uye_ekle),
            ("✏️  Düzenle",       "",           self._uye_duzenle),
            ("🗑️  Sil",           "btnTehlike", self._uye_sil),
        ]))
        self.uye_tablo = tablo_olustur(["ID","Ad","Soyad","Telefon","E-posta","Üyelik","Bitiş","Durum"])
        self._uyeler_yenile()
        lay.addWidget(self.uye_tablo)
        return w

    # ANTRENÖRLER
    def _antrenorler_yenile(self):
        rows = sorgu_calistir(
            "SELECT antrenor_id,ad,soyad,uzmanlik,telefon,email,maas FROM antrenorler ORDER BY antrenor_id DESC"
        )
        tabloyu_doldur(self.ant_tablo, rows)

    def _ant_ekle(self):
        from antrenor_form import AntrenorForm
        f = AntrenorForm(parent=self)
        if f.exec_(): self._antrenorler_yenile()

    def _ant_duzenle(self):
        sel = self.ant_tablo.selectedItems()
        # Siberpunk Seçim Koruması
        if not sel:
            siber_mesaj("Seçim Eksik", "Düzenlemek için lütfen tablodan bir antrenör seçin.", "uyari", self)
            return
            
        aid = int(self.ant_tablo.item(sel[0].row(), 0).text())
        from antrenor_form import AntrenorForm
        f = AntrenorForm(antrenor_id=aid, parent=self)
        if f.exec_(): self._antrenorler_yenile()

    def _ant_sil(self):
        sel = self.ant_tablo.selectedItems()
        if not sel:
            siber_mesaj("Seçim Eksik", "Silmek için lütfen tablodan bir antrenör seçin.", "uyari", self)
            return  # ← return if bloğunun İÇİNDE olmalı
        
        secili_satir = sel[0].row()
        aid = self.ant_tablo.item(secili_satir, 0).text()
        ad  = self.ant_tablo.item(secili_satir, 1).text()
        
        if siber_mesaj("Antrenör Silme Onayı", f"{ad} isimli antrenörü silmek istiyor musunuz?", "soru", self):
            try:
                bag = db_baglanti.baglan()
                cur = bag.cursor()
                cur.execute("SET FOREIGN_KEY_CHECKS = 0")
                cur.execute("DELETE FROM antrenorler WHERE antrenor_id = %s", (aid,))
                cur.execute("SET FOREIGN_KEY_CHECKS = 1")
                bag.commit()
                db_baglanti.baglanti_kapat(bag, cur)
                self.ant_tablo.removeRow(secili_satir)
                ToastNotification(self, f"{ad} başarıyla silindi.", "basari").goster()
                if hasattr(self, '_dashboard_yenile'):
                    self._dashboard_yenile()
            except Exception as e:
                try:
                    bag2 = db_baglanti.baglan()
                    cur2 = bag2.cursor()
                    cur2.execute("SET FOREIGN_KEY_CHECKS = 1")
                    bag2.commit()
                    db_baglanti.baglanti_kapat(bag2, cur2)
                except:
                    pass
                siber_mesaj("Sistem Hatası", f"Veritabanı hatası oluştu:\n{e}", "hata", self)

    def _antrenorler(self):
        w, lay = self._sayfa_widget("🏋 Antrenör Yönetimi")
        lay.addWidget(aksiyon_bar_olustur([
            ("➕ Yeni Antrenör Ekle", "btnBasari",  self._ant_ekle),
            ("✏️ Düzenle",            "",           self._ant_duzenle),
            ("🗑️ Sil",               "btnTehlike", self._ant_sil),
        ]))
        self.ant_tablo = tablo_olustur(["ID","Ad","Soyad","Uzmanlık","Telefon","E-posta","Maaş (₺)"])
        self._antrenorler_yenile()
        lay.addWidget(self.ant_tablo)
        return w

    # DERSLER
    def _dersler_yenile(self):
        rows = sorgu_calistir("""
            SELECT d.ders_id, d.ders_adi, CONCAT(a.ad,' ',a.soyad), d.ders_saati, d.kapasite, d.salon
            FROM dersler d LEFT JOIN antrenorler a ON d.antrenor_id=a.antrenor_id
            ORDER BY d.ders_id DESC
        """)
        tabloyu_doldur(self.ders_tablo, rows)

    def _ders_ekle(self):
        from ders_form import DersForm
        f = DersForm(parent=self)
        if f.exec_(): self._dersler_yenile()

    def _ders_duzenle(self):
        sel = self.ders_tablo.selectedItems()
        # Siberpunk Seçim Koruması
        if not sel:
            siber_mesaj("Seçim Eksik", "Düzenlemek için lütfen tablodan bir ders seçin.", "uyari", self)
            return
            
        did = int(self.ders_tablo.item(sel[0].row(), 0).text())
        from ders_form import DersForm
        f = DersForm(ders_id=did, parent=self)
        if f.exec_(): self._dersler_yenile()

    def _ders_sil(self):
        sel = self.ders_tablo.selectedItems()
        if not sel:
            siber_mesaj("Seçim Eksik", "Silmek için lütfen tablodan bir ders seçin.", "uyari", self)
            return  # ← return if bloğunun İÇİNDE olmalı
        
        secili_satir = sel[0].row()
        did = self.ders_tablo.item(secili_satir, 0).text()
        ad  = self.ders_tablo.item(secili_satir, 1).text()
        
        if siber_mesaj("Ders Silme Onayı", f"{ad} dersini silmek istiyor musunuz?", "soru", self):
            try:
                bag = db_baglanti.baglan()
                cur = bag.cursor()
                cur.execute("SET FOREIGN_KEY_CHECKS = 0")
                cur.execute("DELETE FROM dersler WHERE ders_id = %s", (did,))
                cur.execute("SET FOREIGN_KEY_CHECKS = 1")
                bag.commit()
                db_baglanti.baglanti_kapat(bag, cur)
                self.ders_tablo.removeRow(secili_satir)
                ToastNotification(self, f"{ad} dersi başarıyla silindi.", "basari").goster()
            except Exception as e:
                try:
                    bag2 = db_baglanti.baglan()
                    cur2 = bag2.cursor()
                    cur2.execute("SET FOREIGN_KEY_CHECKS = 1")
                    bag2.commit()
                    db_baglanti.baglanti_kapat(bag2, cur2)
                except:
                    pass
                siber_mesaj("Sistem Hatası", f"Veritabanı hatası oluştu:\n{e}", "hata", self)

    def _dersler(self):
        w, lay = self._sayfa_widget("📅 Ders Programı")
        lay.addWidget(aksiyon_bar_olustur([
            ("➕ Yeni Ders Ekle", "btnBasari",  self._ders_ekle),
            ("✏️ Düzenle",        "",           self._ders_duzenle),
            ("🗑️ Sil",            "btnTehlike", self._ders_sil),
        ]))
        self.ders_tablo = tablo_olustur(["ID","Ders Adı","Antrenör","Saat","Kapasite","Salon"])
        self._dersler_yenile()
        lay.addWidget(self.ders_tablo)
        return w

    # ÖDEMELER
    def _odemeler_yenile(self):
     rows = sorgu_calistir("""
        SELECT CONCAT(u.ad,' ',u.soyad), oy.yontem_adi, o.tutar, o.odeme_tarihi, o.aciklama
        FROM odemeler o
        LEFT JOIN uyeler u ON o.uye_id = u.uye_id
        LEFT JOIN odeme_yontemleri oy ON o.odeme_yontem_id = oy.odeme_yontem_id
        WHERE u.uye_id IS NOT NULL
        ORDER BY o.odeme_id DESC
        """)
     tabloyu_doldur(self.odeme_tablo, rows)

    def _odeme_al(self):
        from odeme_form import OdemeForm
        f = OdemeForm(parent=self)
        if f.exec_():
            self._odemeler_yenile()
            self._kasa_yenile()

    def _odemeler(self):
        w, lay = self._sayfa_widget("💰  Ödeme Kayıtları")
        lay.addWidget(aksiyon_bar_olustur([
            ("💰  Tahsilat Al", "btnBasari", self._odeme_al),
        ]))
        self.odeme_tablo = tablo_olustur(["Üye","Yöntem","Tutar (₺)","Tarih","Açıklama"])
        self._odemeler_yenile()
        lay.addWidget(self.odeme_tablo)
        return w

    # EKİPMANLAR
    def _ekipmanlar(self):
        w, lay = self._sayfa_widget("🔧  Ekipman Yönetimi")
        t = tablo_olustur(["Ekipman","Tür","Adet","Durum","Alım Tarihi"])
        rows = sorgu_calistir("""
            SELECT e.ekipman_adi, et.tur_adi, e.adet, e.durum, e.alim_tarihi
            FROM ekipmanlar e LEFT JOIN ekipman_turleri et ON e.ekipman_tur_id=et.ekipman_tur_id
        """)
        tabloyu_doldur(t, rows, renkli_sutun=3)
        lay.addWidget(t)
        return w

    # STOKLAR
    def _stoklar(self):
        w, lay = self._sayfa_widget("📦  Stok Takibi")
        t = tablo_olustur(["Ürün Adı","Miktar","Birim","Son Güncelleme"])
        rows = sorgu_calistir("SELECT urun_adi,miktar,birim,son_guncelleme FROM stoklar ORDER BY urun_adi")
        tabloyu_doldur(t, rows)
        lay.addWidget(t)
        return w

    # KASA
    def _kasa_yenile(self):
        if not hasattr(self, 'kart_gelir'): return
        ozet = sorgu_calistir("SELECT islem_tipi, SUM(tutar) FROM kasa GROUP BY islem_tipi")
        gelir_top = gider_top = 0
        for tip, toplam in ozet:
            if tip == "gelir": gelir_top = float(toplam)
            else: gider_top = float(toplam)
        net = gelir_top - gider_top
        self.kart_gelir.guncelle(f"{gelir_top:,.0f}")
        self.kart_gider.guncelle(f"{gider_top:,.0f}")
        self.kart_net.guncelle(f"{net:,.0f}")
        rows = sorgu_calistir("SELECT gider_turu,tutar,gider_tarihi,aciklama FROM giderler ORDER BY gider_id DESC")
        tabloyu_doldur(self.gider_tablo, rows)

    def _gider_ekle(self):
        from gider_form import GiderForm
        f = GiderForm(parent=self)
        if f.exec_(): self._kasa_yenile()

    def _kasa(self):
        w, lay = self._sayfa_widget("💼  Kasa & Giderler")
        kl = QHBoxLayout(); kl.setSpacing(14)
        self.kart_gelir = HudCard("TOPLAM GELİR (₺)", "0", "📈", "#10B981")
        self.kart_gider = HudCard("TOPLAM GİDER (₺)", "0", "📉", "#EF4444")
        self.kart_net   = HudCard("NET KASA (₺)",     "0", "💼", "#6C63FF")
        kl.addWidget(self.kart_gelir); kl.addWidget(self.kart_gider); kl.addWidget(self.kart_net)
        lay.addLayout(kl)
        lay.addWidget(aksiyon_bar_olustur([("📉  Yeni Gider Ekle", "btnTehlike", self._gider_ekle)]))
        self.gider_tablo = tablo_olustur(["Gider Türü","Tutar (₺)","Tarih","Açıklama"])
        self._kasa_yenile()
        lay.addWidget(self.gider_tablo)
        return w

    # RAPORLAR
    def _raporlar(self):
        w, lay = self._sayfa_widget("📄  Sistem Raporları")
        bilgi = QLabel("Veritabanı kayıtlarınızı CSV formatında dışa aktarın veya grafik analizlere göz atın.")
        bilgi.setWordWrap(True)
        bilgi.setStyleSheet("color:#555580; font-size:12px; background:transparent; border:none;")
        lay.addWidget(bilgi)

        bg = QGridLayout(); bg.setSpacing(12)
        def rapor_btn(baslik, ikon, tablo):
            btn = QPushButton(f"{ikon}  {baslik}")
            btn.setObjectName("btnBasari")
            btn.setFixedHeight(44)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda: self._csv_disa_aktar(tablo, baslik))
            return btn
        bg.addWidget(rapor_btn("Üyeler Listesi",   "👥", "uyeler"),      0, 0)
        bg.addWidget(rapor_btn("Ödeme Geçmişi",    "💰", "odemeler"),    0, 1)
        bg.addWidget(rapor_btn("Kasa ve Giderler", "💼", "giderler"),    1, 0)
        bg.addWidget(rapor_btn("Antrenör Listesi", "🏋", "antrenorler"), 1, 1)
        lay.addLayout(bg)

        gl = QHBoxLayout(); gl.setSpacing(16)

        fig1 = Figure(figsize=(4.5, 3), facecolor="#08081E")
        c1 = FigureCanvas(fig1)
        ax1 = fig1.add_subplot(111)
        ax1.set_facecolor("#08081E")
        ax1.tick_params(colors="#7B7BAA", labelsize=9)
        for s in ax1.spines.values(): s.set_color("#1E1E4A")
        kasa = sorgu_calistir("SELECT islem_tipi, SUM(tutar) FROM kasa GROUP BY islem_tipi")
        gelir = gider = 0
        for tip, tutar in kasa:
            if tip == "gelir": gelir = tutar
            else: gider = tutar
        ax1.bar(["Gelir","Gider"], [gelir, gider], color=["#8B5CF6","#3B82F6"], width=0.5, edgecolor="none")
        ax1.set_title("Kasa Özeti (₺)", color="#A78BFA", pad=10, fontsize=11, weight="bold")
        fig1.tight_layout()
        c1.setStyleSheet("border:1px solid #1E1E4A; border-radius:8px;")

        fig2 = Figure(figsize=(4.5, 3), facecolor="#08081E")
        c2 = FigureCanvas(fig2)
        ax2 = fig2.add_subplot(111)
        ax2.set_facecolor("#08081E")
        uye_data = sorgu_calistir("""
            SELECT ut.tip_adi, COUNT(u.uye_id)
            FROM uyeler u JOIN uyelik_tipleri ut ON u.uyelik_tip_id=ut.uyelik_tip_id
            GROUP BY ut.tip_adi
        """)
        if uye_data:
            labels = [r[0] for r in uye_data]
            sizes  = [r[1] for r in uye_data]
            colors = ["#6C63FF","#3B82F6","#8B5CF6","#A78BFA","#60A5FA"]
            ax2.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90,
                    colors=colors[:len(labels)],
                    textprops={"color":"#A78BFA","weight":"bold","fontsize":9})
        ax2.set_title("Üyelik Dağılımı", color="#A78BFA", pad=10, fontsize=11, weight="bold")
        fig2.tight_layout()
        c2.setStyleSheet("border:1px solid #1E1E4A; border-radius:8px;")

        gl.addWidget(c1); gl.addWidget(c2)
        lay.addLayout(gl)
        lay.addStretch()
        return w

    def _csv_disa_aktar(self, tablo_adi, dosya_baslik):
        dosya_yolu, _ = QFileDialog.getSaveFileName(
            self, f"{dosya_baslik} Raporunu Kaydet",
            f"{tablo_adi}_raporu.csv", "CSV Dosyası (*.csv);;Tüm Dosyalar (*)"
        )
        if not dosya_yolu: return
        try:
            sonuc = sorgu_calistir(f"SELECT * FROM {tablo_adi}")
            bag = db_baglanti.baglan()
            if not bag: return
            cur = bag.cursor()
            cur.execute(f"SELECT * FROM {tablo_adi} LIMIT 0")
            sutunlar = [d[0] for d in cur.description]
            db_baglanti.baglanti_kapat(bag, cur)
            with open(dosya_yolu, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f, delimiter=";")
                w.writerow(sutunlar)
                if sonuc: w.writerows(sonuc)
            ToastNotification(self, f"{dosya_baslik} raporu kaydedildi.", "basari").goster()
        except Exception as e:
            ToastNotification(self, f"Hata: {str(e)}", "hata").goster()