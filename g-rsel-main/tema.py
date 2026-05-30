# -*- coding: utf-8 -*-
# TitanFit Gym – Ortak Tema Modülü

RENKLER = {
    # Arka planlar
    "bg_ana":           "#07071A",   # Derin lacivert-siyah
    "bg_panel":         "#0D0D2B",   # Koyu lacivert panel
    "bg_kart":          "#0F0F30",   # Kart arka planı
    "bg_input":         "#0A0A20",   # Input arka planı
    "bg_sidebar":       "#090920",   # Sidebar arka planı

    # Kenarlıklar
    "border":           "#1E1E4A",   # Varsayılan kenarlık
    "border_focus":     "#6C63FF",   # Mor vurgu
    "border_accent":    "#00D4FF",   # Cyan vurgu

    # Metin
    "metin_ana":        "#E8E8FF",   # Parlak beyaz-mor
    "metin_ust":        "#7B7BAA",   # Soluk metin
    "metin_yardim":     "#A78BFA",   # Açık mor yardımcı metin

    # Aksanlar (Mavi-Mor Paleti)
    "mor_parlak":       "#8B5CF6",   # Ana mor
    "mor_koyu":         "#6D28D9",   # Koyu mor
    "mor_acik":         "#A78BFA",   # Açık mor
    "mavi_parlak":      "#3B82F6",   # Ana mavi
    "mavi_neon":        "#00D4FF",   # Neon cyan
    "mavi_koyu":        "#1D4ED8",   # Koyu mavi

    # Durum Renkleri
    "basari":           "#10B981",   # Yeşil başarı
    "tehlike":          "#EF4444",   # Kırmızı tehlike
    "uyari":            "#F59E0B",   # Sarı uyarı

    # Gradyanlar (stylesheet'te doğrudan kullanılacak)
    "grad_buton":       "qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #6C63FF,stop:1 #3B82F6)",
    "grad_buton_hover": "qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #8B5CF6,stop:1 #60A5FA)",
    "grad_sidebar":     "qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0D0D2B,stop:1 #07071A)",
}

FONTLAR = {
    "kucuk":        "11px",
    "normal":       "13px",
    "buyuk":        "15px",
    "baslik":       "18px",
    "buyuk_baslik": "32px",
    "logo":         "56px",
}

ANA_STYLESHEET = f"""
    /* ── Genel ─────────────────────────────────────── */
    QWidget {{
        background-color: {RENKLER['bg_ana']};
        color: {RENKLER['metin_ana']};
        font-family: "Segoe UI", "Consolas";
        font-size: {FONTLAR['normal']};
    }}

    /* ── Sol Panel / Sidebar ────────────────────────── */
    QFrame#leftPanel {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0D0D2B,stop:1 #07071A);
        border-right: 1px solid {RENKLER['border_focus']};
        border-radius: 0px;
    }}

    QFrame#rightPanel {{
        background-color: {RENKLER['bg_panel']};
        border: none;
    }}

    QFrame#kart {{
        background-color: {RENKLER['bg_kart']};
        border: 1px solid {RENKLER['border']};
        border-radius: 10px;
    }}

    /* ── Başlıklar ──────────────────────────────────── */
    QLabel#title {{
        font-size: {FONTLAR['buyuk_baslik']};
        font-weight: 900;
        letter-spacing: 1px;
        color: {RENKLER['mor_acik']};
    }}

    QLabel#subtitle {{
        font-size: {FONTLAR['buyuk']};
        letter-spacing: 0.5px;
        color: {RENKLER['metin_ust']};
    }}

    QLabel {{
        font-size: {FONTLAR['normal']};
        color: {RENKLER['metin_ana']};
    }}

    QLabel#logo {{
        font-size: {FONTLAR['logo']};
        color: {RENKLER['mor_parlak']};
    }}

    QLabel#panelText {{
        font-size: {FONTLAR['baslik']};
        font-weight: bold;
        color: {RENKLER['mor_acik']};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    QLabel#panelSub {{
        color: {RENKLER['metin_yardim']};
        font-size: {FONTLAR['kucuk']};
    }}

    /* ── Giriş Alanları ─────────────────────────────── */
    QLineEdit, QComboBox, QDateEdit, QTimeEdit, QSpinBox, QTextEdit {{
        background-color: {RENKLER['bg_input']};
        border: 1px solid {RENKLER['border']};
        border-bottom: 2px solid {RENKLER['mor_koyu']};
        border-radius: 6px;
        padding: 9px 12px;
        font-size: {FONTLAR['normal']};
        color: {RENKLER['metin_ana']};
        selection-background-color: {RENKLER['mor_parlak']};
    }}

    QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus, QSpinBox:focus {{
        border: 1px solid {RENKLER['mor_parlak']};
        border-bottom: 2px solid {RENKLER['mavi_neon']};
        background-color: rgba(107, 99, 255, 0.07);
    }}

    QLineEdit:hover, QComboBox:hover, QDateEdit:hover, QSpinBox:hover {{
        border-color: {RENKLER['mor_acik']};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 28px;
    }}

    QComboBox::down-arrow {{
        width: 12px;
        height: 12px;
        color: {RENKLER['mor_acik']};
    }}

    QComboBox QAbstractItemView {{
        background-color: {RENKLER['bg_kart']};
        border: 1px solid {RENKLER['border_focus']};
        selection-background-color: {RENKLER['mor_parlak']};
        color: {RENKLER['metin_ana']};
        outline: none;
    }}

    QDateEdit::drop-down, QTimeEdit::drop-down {{
        border: none;
        width: 24px;
    }}

    QSpinBox::up-button, QSpinBox::down-button {{
        background: {RENKLER['bg_kart']};
        border: 1px solid {RENKLER['border']};
        width: 18px;
    }}

    QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
        background: {RENKLER['mor_parlak']};
    }}

    /* ── Butonlar ───────────────────────────────────── */
    /* ── Butonlar ───────────────────────────────────── */
    QPushButton {{
        background: transparent;
        border: 1.5px solid {RENKLER['mor_parlak']};
        border-radius: 6px;
        padding: 9px 20px;
        font-size: {FONTLAR['normal']};
        font-weight: 700;
        color: {RENKLER['mor_acik']};
        min-width: 80px;
    }}

    QPushButton:hover {{
        background: {RENKLER['grad_buton']};
        color: white;
        /* border-color: transparent yerine alt satırı yazdık: */
        border: 1.5px solid transparent; 
    }}

    QPushButton:pressed {{
        background: {RENKLER['mor_koyu']};
        border: 1.5px solid transparent;
    }}

    QPushButton:disabled {{
        color: {RENKLER['metin_ust']};
        border: 1.5px solid {RENKLER['border']};
    }}

    QPushButton#loginButton {{
        background: {RENKLER['grad_buton']};
        color: white;
        border: 1.5px solid transparent; /* Standart butonlarla aynı border yapısı */
        font-weight: 800;
        letter-spacing: 1px;
        padding: 12px 20px;
    }}

    QPushButton#loginButton:hover {{
        background: {RENKLER['grad_buton_hover']};
        border: 1.5px solid transparent;
    }}

    QPushButton#btnTehlike {{
        border: 1.5px solid {RENKLER['tehlike']};
        color: {RENKLER['tehlike']};
    }}

    QPushButton#btnTehlike:hover {{
        background-color: {RENKLER['tehlike']};
        color: white;
        border: 1.5px solid transparent;
    }}

    QPushButton#btnBasari {{
        border: 1.5px solid {RENKLER['basari']};
        color: {RENKLER['basari']};
    }}

    QPushButton#btnBasari:hover {{
        background-color: {RENKLER['basari']};
        color: white;
        border: 1.5px solid transparent;
    }}

    /* ── Tablo ──────────────────────────────────────── */
    QTableWidget {{
        background-color: {RENKLER['bg_kart']};
        border: 1px solid {RENKLER['border_focus']};
        border-radius: 8px;
        gridline-color: {RENKLER['border']};
        font-size: {FONTLAR['normal']};
        selection-background-color: rgba(107, 99, 255, 0.35);
        selection-color: white;
        alternate-background-color: rgba(13, 13, 43, 0.6);
    }}

    QTableWidget::item {{
        padding: 7px 10px;
        border-bottom: 1px solid {RENKLER['border']};
    }}

    QTableWidget::item:hover {{
        background-color: rgba(107, 99, 255, 0.15);
    }}

    QHeaderView::section {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #0F0F30,stop:1 #09091F);
        color: {RENKLER['mor_acik']};
        font-weight: bold;
        font-size: {FONTLAR['kucuk']};
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 10px 12px;
        border: none;
        border-bottom: 2px solid {RENKLER['mor_parlak']};
        border-right: 1px solid {RENKLER['border']};
    }}

    QHeaderView::section:last {{
        border-right: none;
    }}

    /* ── ScrollBar ──────────────────────────────────── */
    QScrollBar:vertical {{
        background: {RENKLER['bg_ana']};
        width: 8px;
        border-left: 1px solid {RENKLER['border']};
        border-radius: 4px;
    }}

    QScrollBar::handle:vertical {{
        background: {RENKLER['mor_koyu']};
        min-height: 30px;
        border-radius: 4px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {RENKLER['mor_parlak']};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background: {RENKLER['bg_ana']};
        height: 8px;
        border-top: 1px solid {RENKLER['border']};
        border-radius: 4px;
    }}

    QScrollBar::handle:horizontal {{
        background: {RENKLER['mor_koyu']};
        border-radius: 4px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {RENKLER['mor_parlak']};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    /* ── MessageBox ─────────────────────────────────── */
    QMessageBox {{
        background-color: {RENKLER['bg_panel']};
        color: {RENKLER['metin_ana']};
    }}

    QMessageBox QPushButton {{
        min-width: 80px;
        padding: 8px 20px;
    }}

    /* ── Dialog ─────────────────────────────────────── */
    QDialog {{
        background-color: {RENKLER['bg_panel']};
    }}

    /* ── CalendarWidget ─────────────────────────────── */
    QCalendarWidget {{
        background-color: {RENKLER['bg_kart']};
        color: {RENKLER['metin_ana']};
    }}

    QCalendarWidget QToolButton {{
        background-color: {RENKLER['mor_parlak']};
        color: white;
        border-radius: 4px;
        padding: 4px 8px;
    }}

    QCalendarWidget QAbstractItemView {{
        background-color: {RENKLER['bg_kart']};
        selection-background-color: {RENKLER['mor_parlak']};
        color: {RENKLER['metin_ana']};
    }}
"""


def uygula_tema(widget):
    """Herhangi bir QWidget'e tam temayı uygular."""
    widget.setStyleSheet(ANA_STYLESHEET)