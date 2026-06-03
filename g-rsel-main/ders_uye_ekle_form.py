from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel
import db_baglanti

class DersUyeEkleForm(QDialog):
    def __init__(self, ders_id, antrenor_id, parent=None):
        super().__init__(parent)
        self.ders_id = ders_id
        self.antrenor_id = antrenor_id
        self.setWindowTitle("Derse Üye Ekle")
        self.setFixedSize(400, 500)
        
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Bu derse eklenecek üyeyi seçin:"))
        
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(2)
        self.tablo.setHorizontalHeaderLabels(["ID", "Üye Adı Soyadı"])
        lay.addWidget(self.tablo)
        
        self.btn_ekle = QPushButton("Ekle")
        self.btn_ekle.setStyleSheet("background: #6C63FF; color: white; padding: 8px;")
        self.btn_ekle.clicked.connect(self._derse_ata)
        lay.addWidget(self.btn_ekle)
        
        self._listele()

    def _listele(self):
        print(f"Debug: Aranan Antrenor ID: {self.antrenor_id}") # Terminalde ne yazıyor?
        
        query = "SELECT uye_id, ad || ' ' || soyad FROM uyeler WHERE uye_id IN (SELECT uye_id FROM uye_Antrenor WHERE antrenor_id = ?)"
        rows = db_baglanti.sorgu_calistir(query, (self.antrenor_id,))
        
        print(f"Debug: Dönen satır sayısı: {len(rows) if rows else 0}")
        
        if rows:
            self.tablo.setRowCount(0) # Önce tabloyu temizle
            for row_idx, row_data in enumerate(rows):
                self.tablo.insertRow(row_idx)
                self.tablo.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
                self.tablo.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))

    def _derse_ata(self):
        sel = self.tablo.selectedItems()
        if not sel: return
        uye_id = self.tablo.item(sel[0].row(), 0).text()
        
        # INSERT INTO kısmında da tabloyu 'uyeDers' olarak güncelledik
        db_baglanti.sorgu_calistir("INSERT INTO uyeDers (ders_id, uye_id) VALUES (?, ?)", 
                                   (self.ders_id, uye_id))
        self.accept()