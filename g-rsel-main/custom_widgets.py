# -*- coding: utf-8 -*-
# TitanFit Gym – Özel Widget Bileşenleri 

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
    QGraphicsDropShadowEffect, QGraphicsOpacityEffect, QApplication, QDialog
)
from PyQt5.QtCore import Qt, QPoint, QRect, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QLinearGradient, QBrush

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt

class SiberMessageBox(QDialog):
    def __init__(self, baslik, mesaj, ikon_tipi="bilgi", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 180)
        
        renk = "#6C63FF"
        ikon = "ℹ️"
        if ikon_tipi == "hata": renk = "#EF4444"; ikon = "❌"
        elif ikon_tipi == "uyari": renk = "#F59E0B"; ikon = "⚠️"
        elif ikon_tipi == "soru": renk = "#3B82F6"; ikon = "❓"
        elif ikon_tipi == "basari": renk = "#10B981"; ikon = "✅"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        panel = QWidget()
        panel.setObjectName("MsgPanel")
        panel.setStyleSheet(f"QWidget#MsgPanel {{ background-color: #0A0A22; border: 2px solid {renk}; border-radius: 12px; }}")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 15, 20, 15)
        
        lbl_baslik = QLabel(f"{ikon}  {baslik.upper()}")
        lbl_baslik.setStyleSheet(f"color: {renk}; font-size: 13px; font-weight: 800; background:transparent;")
        panel_layout.addWidget(lbl_baslik)
        
        lbl_mesaj = QLabel(mesaj)
        lbl_mesaj.setWordWrap(True)
        lbl_mesaj.setStyleSheet("color: #E8E8FF; font-size: 12px; font-weight: 600; padding: 10px 0; background:transparent;")
        panel_layout.addWidget(lbl_mesaj)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        if ikon_tipi == "soru":
            btn_hayir = QPushButton("HAYIR")
            btn_hayir.setCursor(Qt.PointingHandCursor)
            btn_hayir.setStyleSheet("background-color: #141438; color: #7B7BAA; border: 1px solid #1E1E4A; padding: 7px 20px; border-radius: 6px; font-weight: 700;")
            btn_hayir.clicked.connect(self.reject)
            
            btn_evet = QPushButton("EVET")
            btn_evet.setCursor(Qt.PointingHandCursor)
            btn_evet.setStyleSheet(f"background-color: {renk}22; color: {renk}; border: 1px solid {renk}; padding: 7px 24px; border-radius: 6px; font-weight: 700;")
            btn_evet.clicked.connect(self.accept)
            
            btn_layout.addWidget(btn_hayir)
            btn_layout.addWidget(btn_evet)
        else:
            btn_tamam = QPushButton("TAMAM")
            btn_tamam.setCursor(Qt.PointingHandCursor)
            btn_tamam.setStyleSheet("background-color: #1E1E4A; color: #A78BFA; border: 1px solid #6C63FF; padding: 7px 24px; border-radius: 6px; font-weight: 700;")
            btn_tamam.clicked.connect(self.accept)
            btn_layout.addWidget(btn_tamam)
            
        panel_layout.addLayout(btn_layout)
        layout.addWidget(panel)

def siber_mesaj(baslik, mesaj, ikon_tipi="bilgi", parent=None):
    box = SiberMessageBox(baslik, mesaj, ikon_tipi, parent)
    return box.exec_() == QDialog.Accepted

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.start_pos = None
        self.setFixedHeight(44)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #0D0D2B, stop:0.5 #0F0F35, stop:1 #0D0D2B);
                border-bottom: 1px solid #6C63FF;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }
            QLabel {
                color: #A78BFA;
                font-family: 'Segoe UI';
                font-weight: 600;
                font-size: 13px;
                letter-spacing: 3px;
                border: none;
                background: transparent;
            }
            QPushButton {
                background: transparent;
                border: none;
                color: #555580;
                font-size: 14px;
                font-weight: bold;
                border-radius: 0px;
                padding: 0px;
            }
            QPushButton:hover {
                color: #A78BFA;
                background: rgba(107, 99, 255, 0.15);
                border-radius: 4px;
            }
            QPushButton#btnClose:hover {
                color: #EF4444;
                background: rgba(239, 68, 68, 0.15);
                border-radius: 4px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 10, 0)
        layout.setSpacing(6)

        # İkon
        icon_lbl = QLabel("⬡")
        icon_lbl.setStyleSheet("color: #6C63FF; font-size: 16px; letter-spacing: 0px; border:none; background:transparent;")
        layout.addWidget(icon_lbl)

        self.title_label = QLabel("T I T A N F I T   G Y M   S Y S T E M")
        layout.addWidget(self.title_label)
        layout.addStretch()

        # Pencere Kontrol Butonları
        for text, obj_name, slot in [
            ("─", "btnMin", self.parent.showMinimized),
            ("☐", "btnMax", self.toggle_max),
            ("✕", "btnClose", self.parent.close),
        ]:
            btn = QPushButton(text)
            btn.setObjectName(obj_name)
            btn.setFixedSize(32, 28)
            btn.clicked.connect(slot)
            layout.addWidget(btn)

    def toggle_max(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
     if (
        event.buttons() & Qt.LeftButton
        and self.start_pos is not None
        and not self.parent.isMaximized()
     ):
        self.parent.move(event.globalPos() - self.start_pos)


class CircularProgress(QWidget):
    def __init__(self, target_value=0, title="", color="#8B5CF6", parent=None):
        super().__init__(parent)
        self.target_value = target_value
        self.current_value = 0
        self.title = title
        self.color = color
        self.setFixedSize(170, 170)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)

    def guncelle(self, val):
        try:
            # String içindeki tüm virgülleri temizleyip sayıya çeviriyoruz
            temiz_val = str(val).replace(',', '').strip()
            self.target_value = int(float(temiz_val))
        except (ValueError, TypeError):
            self.target_value = 0
        self.current_value = 0
        self.timer.start(16)

    def _animate(self):
        step = max(1, self.target_value // 25)
        if self.current_value < self.target_value:
            self.current_value = min(self.current_value + step, self.target_value)
            self.update()
        else:
            self.current_value = self.target_value
            self.timer.stop()
            self.update()

    def paintEvent(self, event):
        w, h = self.width(), self.height()
        margin = 20
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Çemberi dikeyde (Y ekseninde) yukarı kaydırmak yerine 
        # tam merkezde kalması için 'margin - 10' yerine direkt 'margin' yapıyoruz
        rect = QRect(margin, margin - 5, w - margin * 2, h - margin * 2 - 15)

        # Arka plan çemberi
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(10, 10, 30, 220))
        painter.drawEllipse(rect)

        # Dış yay (gri hat)
        pen = QPen()
        pen.setColor(QColor(30, 30, 74))
        pen.setWidth(8)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(rect, 0, 360 * 16)

        # Aktif ilerleme yayı
        pen.setColor(QColor(self.color))
        painter.setPen(pen)
        
        en_yuksek = max(self.target_value, self.current_value, 1)
        ratio = self.current_value / en_yuksek
        
        span = int(360 * ratio * 16)
        painter.drawArc(rect, int(90 * 16), -span)

        # Değer metni (Rakamlar çemberin tam ortasına otursun)
        painter.setPen(QPen(QColor("#E8E8FF")))
        font = QFont("Segoe UI", 22, QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignCenter, str(self.current_value))

        # Başlık metni (Çemberden iyice uzaklaştırıp en alta sabitledik)
        font2 = QFont("Segoe UI", 9, QFont.Bold)
        painter.setFont(font2)
        painter.setPen(QPen(QColor(self.color)))
        title_rect = QRect(0, h - 22, w, 20)  # y koordinatını h-22 yaparak tabana yaklaştırdık
        painter.drawText(title_rect, Qt.AlignCenter, self.title)

        painter.end()


class HudCard(QWidget):
    def __init__(self, baslik, deger, ikon, renk="#8B5CF6", parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)  # Rakamların sığması için dikey boyutu 120'ye çektik
        self.renk = renk
        self._setup_style(renk)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(14)

        # İkon alanı
        self.lbl_ikon = QLabel(ikon)
        self.lbl_ikon.setObjectName("ikon")
        self.lbl_ikon.setFixedSize(50, 50)
        self.lbl_ikon.setAlignment(Qt.AlignCenter)
        self.lbl_ikon.setStyleSheet(f"""
            QLabel {{
                font-size: 26px;
                background: rgba(107, 99, 255, 0.12);
                border: 1px solid rgba(107, 99, 255, 0.25);
                border-radius: 10px;
                color: {renk};
            }}
        """)
        layout.addWidget(self.lbl_ikon)

        # Metin alanı
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        text_layout.setAlignment(Qt.AlignVCenter) # Dikeyde tam ortalansınlar

        self.lbl_baslik = QLabel(baslik)
        self.lbl_baslik.setObjectName("baslik")
        self.lbl_baslik.setStyleSheet(f"""
            font-size: 11px;
            color: {renk};
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            background: transparent;
            border: none;
        """)

        self.lbl_deger = QLabel("0")
        self.lbl_deger.setObjectName("deger")
        self.lbl_deger.setStyleSheet("""
            font-size: 24px;
            font-weight: 900;
            color: #E8E8FF;
            background: transparent;
            border: none;
            font-family: 'Segoe UI';
        """)

        text_layout.addWidget(self.lbl_baslik)
        text_layout.addWidget(self.lbl_deger)
        layout.addLayout(text_layout)
        layout.addStretch()

        # Animasyon değişkenleri
        self.target_value = 0
        self.current_value = 0
        self.is_currency = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)

        self.guncelle(deger)

    def _setup_style(self, renk):
        self.setStyleSheet(f"""
            HudCard {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 rgba(15,15,48,0.95), stop:1 rgba(9,9,32,0.95));
                border: 1px solid {renk};
                border-left: 4px solid {renk};
                border-radius: 10px;
            }}
        """)

    def guncelle(self, yeni_deger):
        # Para formatı kontrolünü virgüle göre yapıyoruz
        self.is_currency = ',' in str(yeni_deger)
        
        # Sayıya çevirmeden önce stringi tamamen izole ediyoruz
        hedef_str = str(yeni_deger).replace(',', '').replace('₺', '').strip()
        try:
            self.target_value = int(float(hedef_str))
        except (ValueError, TypeError):
            self.target_value = 0
            
        self.current_value = 0
        self.timer.start(14)

    def _animate(self):
        step = max(1, self.target_value // 20)
        if self.current_value < self.target_value:
            self.current_value = min(self.current_value + step, self.target_value)
            # Sayıyı ekrana basarken binlik ayracını doğru formatta ekliyoruz
            gosterim = f"{self.current_value:,}" if self.is_currency else str(self.current_value)
            self.lbl_deger.setText(gosterim)
        else:
            gosterim = f"{self.target_value:,}" if self.is_currency else str(self.target_value)
            self.lbl_deger.setText(gosterim)
            self.timer.stop()


class ToastNotification(QWidget):
    def __init__(self, parent, mesaj, tur="basari"):
        super().__init__(parent)
        self.setWindowFlags(Qt.SubWindow | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        if tur == "basari":
            renk = "#10B981"
            ikon = "✅"
        else:
            renk = "#EF4444"
            ikon = "⚠️"

        self.setStyleSheet(f"""
            QWidget#toast_inner {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 rgba(10,10,32,0.97), stop:1 rgba(15,15,45,0.97));
                border: 1px solid {renk};
                border-left: 4px solid {renk};
                border-radius: 8px;
            }}
            QLabel {{
                color: #E8E8FF;
                font-family: 'Segoe UI';
                font-size: 12px;
                font-weight: 600;
                border: none;
                background: transparent;
            }}
        """)

        self.setFixedSize(310, 58)

        outer = QHBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        inner = QWidget(self)
        inner.setObjectName("toast_inner")
        inner.setFixedSize(310, 58)

        lay = QHBoxLayout(inner)
        lay.setContentsMargins(14, 10, 14, 10)
        lay.setSpacing(10)

        ikon_lbl = QLabel(ikon)
        ikon_lbl.setStyleSheet("font-size: 18px; border:none; background:transparent;")
        msg_lbl = QLabel(mesaj)
        msg_lbl.setWordWrap(True)

        lay.addWidget(ikon_lbl)
        lay.addWidget(msg_lbl, 1)
        outer.addWidget(inner)

        # Animasyonlar
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(450)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

        self.hide_timer = QTimer(self)
        self.hide_timer.timeout.connect(self._fade_out)
        self.hide_timer.setSingleShot(True)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")

    def goster(self):
        parent_rect = self.parent().rect()
        end_x = parent_rect.width() - self.width() - 20
        start_x = parent_rect.width()
        y = 56

        self.setGeometry(start_x, y, self.width(), self.height())
        self.show()
        self.raise_()

        self.anim.setStartValue(QPoint(start_x, y))
        self.anim.setEndValue(QPoint(end_x, y))
        self.anim.start()

        self.hide_timer.start(3200)

    def _fade_out(self):
        self.fade_anim.setDuration(450)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        self.fade_anim.finished.connect(self.close)
        self.fade_anim.start()