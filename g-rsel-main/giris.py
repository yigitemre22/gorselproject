# -*- coding: utf-8 -*-
# TitanFit Gym – Giriş Ekranı 

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QMessageBox, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

import db_baglanti
import traceback
from tema import uygula_tema
from admin_panel import AdminPanel
from antrenor_panel import AntrenorPanel
from custom_widgets import CustomTitleBar


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("TitanFit Gym Yönetim Sistemi")
        self.setFixedSize(1100, 700)
        uygula_tema(self)
        self._init_ui()

    def _init_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(18, 18, 18, 18)

        # Ana çerçeve
        bg = QFrame()
        bg.setObjectName("bg_frame")
        bg.setStyleSheet("""
            QFrame#bg_frame {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #07071A, stop:0.5 #0D0D2B, stop:1 #07071A);
                border: 1px solid #6C63FF;
                border-radius: 14px;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(35)
        shadow.setColor(QColor(108, 99, 255, 160))
        shadow.setOffset(0, 0)
        bg.setGraphicsEffect(shadow)

        bg_layout = QVBoxLayout(bg)
        bg_layout.setContentsMargins(0, 0, 0, 0)
        bg_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        bg_layout.addWidget(self.title_bar)

        # İçerik
        content = QHBoxLayout()
        content.setContentsMargins(0, 0, 0, 0)
        content.setSpacing(0)

        # ── Sol Panel ────────────────────────────────────────
        left = QFrame()
        left.setObjectName("leftPanel")
        left.setStyleSheet("""
            QFrame#leftPanel {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 #0A0A25, stop:1 #0D0D35);
                border-right: 1px solid #1E1E4A;
                border-bottom-left-radius: 14px;
            }
        """)

        left_lay = QVBoxLayout(left)
        left_lay.setAlignment(Qt.AlignCenter)
        left_lay.setSpacing(12)
        left_lay.setContentsMargins(50, 60, 50, 60)

        logo = QLabel("⬡")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("font-size: 80px; color: #6C63FF; background: transparent; border: none;")

        gym_name = QLabel("TitanFit Gym")
        gym_name.setAlignment(Qt.AlignCenter)
        gym_name.setStyleSheet("""
            font-size: 30px;
            font-weight: 900;
            color: #A78BFA;
            background: transparent;
            border: none;
            letter-spacing: 2px;
        """)

        gym_sub = QLabel("Modern Spor Salonu\nYönetim Sistemi")
        gym_sub.setAlignment(Qt.AlignCenter)
        gym_sub.setStyleSheet("""
            font-size: 13px;
            color: #555580;
            background: transparent;
            border: none;
            line-height: 1.5;
        """)

        # Dekoratif çizgi
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("border: none; border-top: 1px solid #1E1E4A; margin: 10px 30px;")

        # Özellik listesi
        features = [
            ("📊", "Gerçek Zamanlı Dashboard"),
            ("👥", "Üye & Antrenör Yönetimi"),
            ("💰", "Ödeme & Kasa Takibi"),
            ("📊", "Gelişmiş Raporlama"),
        ]
        for ikon, metin in features:
            feat = QLabel(f"  {ikon}  {metin}")
            feat.setStyleSheet("""
                font-size: 12px;
                color: #7B7BAA;
                background: transparent;
                border: none;
                padding: 3px 0;
            """)
            left_lay.addWidget(feat)

        left_lay.addWidget(logo)
        left_lay.addSpacing(8)
        left_lay.addWidget(gym_name)
        left_lay.addWidget(gym_sub)
        left_lay.addSpacing(20)
        left_lay.addWidget(line)
        left_lay.addSpacing(10)
        for ikon, metin in features:
            feat = QLabel(f"  {ikon}  {metin}")
            feat.setStyleSheet("font-size: 12px; color: #7B7BAA; background: transparent; border: none; padding: 3px 0;")
            left_lay.addWidget(feat)

        # ── Sağ Panel ────────────────────────────────────────
        right = QFrame()
        right.setObjectName("rightPanel")
        right.setStyleSheet("""
            QFrame#rightPanel {
                background: transparent;
                border: none;
                border-bottom-right-radius: 14px;
            }
        """)

        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(60, 50, 60, 50)
        right_lay.setSpacing(0)
        right_lay.setAlignment(Qt.AlignVCenter)

        # Başlık
        title_lbl = QLabel("Hoş Geldiniz")
        title_lbl.setStyleSheet("""
            font-size: 28px;
            font-weight: 900;
            color: #A78BFA;
            background: transparent;
            border: none;
            letter-spacing: 1px;
        """)

        sub_lbl = QLabel("Devam etmek için giriş yapın")
        sub_lbl.setStyleSheet("""
            font-size: 13px;
            color: #555580;
            background: transparent;
            border: none;
            margin-bottom: 8px;
        """)

        right_lay.addWidget(title_lbl)
        right_lay.addWidget(sub_lbl)
        right_lay.addSpacing(30)

        # Form alanları
        def field_label(text):
            lbl = QLabel(text)
            lbl.setStyleSheet("font-size: 11px; color: #7B7BAA; font-weight: 700; letter-spacing: 1px; margin-bottom: 4px; background: transparent; border: none;")
            return lbl

        right_lay.addWidget(field_label("ROL"))
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Admin", "Antrenör"])
        self.role_combo.setFixedHeight(42)
        right_lay.addWidget(self.role_combo)
        right_lay.addSpacing(14)

        right_lay.addWidget(field_label("E-POSTA"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("ornek@email.com")
        self.username_input.setFixedHeight(42)
        right_lay.addWidget(self.username_input)
        right_lay.addSpacing(14)

        right_lay.addWidget(field_label("ŞİFRE"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("••••••••")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(42)
        self.password_input.returnPressed.connect(self.login)
        right_lay.addWidget(self.password_input)
        right_lay.addSpacing(28)

        login_btn = QPushButton("  Giriş Yap  →")
        login_btn.setObjectName("loginButton")
        login_btn.setFixedHeight(46)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.login)
        right_lay.addWidget(login_btn)

        right_lay.addStretch()

        content.addWidget(left, 2)
        content.addWidget(right, 3)
        bg_layout.addLayout(content)
        outer.addWidget(bg)

    def login(self):
        try:
            self._login_islemi()
        except Exception:
            QMessageBox.critical(self, "Beklenmedik Hata", traceback.format_exc())
# bg.setGraphicsEffect(shadow)
    def _login_islemi(self):
        role = self.role_combo.currentText()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Uyarı", "E-posta ve şifre boş bırakılamaz.")
            return

        baglanti = db_baglanti.baglan()
        if baglanti is None:
            QMessageBox.critical(self, "Bağlantı Hatası", "Veritabanına bağlanılamadı.")
            return

        cursor = None

        try:
            cursor = baglanti.cursor()

            # 👑 ADMIN LOGIN (SQLite uyumlu)
            if role == "Admin":
                cursor.execute("""
                    SELECT kullanici_id, ad, soyad, rol
                    FROM kullanicilar
                    WHERE email = ?
                    AND sifre = ?
                    AND rol = 'admin'
                    AND aktif = 1
                """, (username, password))

                kullanici = cursor.fetchone()

                if kullanici:
                    self.panel = AdminPanel(kullanici)
                    self.panel.show()
                    self.hide()
                else:
                    QMessageBox.warning(self, "Hata", "E-posta veya şifre hatalı.")

            # 🏋 ANTRENÖR LOGIN (SQLite FIX)
            else:
                cursor.execute("""
                    SELECT antrenor_id, ad, soyad
                    FROM antrenorler
                    WHERE email = ?
                    AND sifre = ?
                """, (username, password))

                antrenor = cursor.fetchone()

                if antrenor:
                    self.panel = AntrenorPanel(antrenor)
                    self.panel.show()
                    self.hide()
                else:
                    QMessageBox.warning(self, "Hata", "E-posta veya şifre hatalı.")

        except Exception:
            QMessageBox.critical(self, "Veritabanı Hatası", traceback.format_exc())

        finally:
            db_baglanti.baglanti_kapat(baglanti, cursor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setFont(QFont("Segoe UI", 10))
    w = LoginWindow()
    w.show()
    sys.exit(app.exec_())