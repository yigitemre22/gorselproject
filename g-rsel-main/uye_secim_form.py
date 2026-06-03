from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton
import db_baglanti

class UyeSecimForm(QDialog):
    def __init__(self, antrenor_id, parent=None):
        super().__init__(parent)
        self.antrenor_id = antrenor_id
        self.setWindowTitle("Üye Seç")
        self.setFixedSize(400, 500)
        
        lay = QVBoxLayout(self)
        self.tablo = QTableWidget()
        self.tablo.setColumnCount(2)
        self.tablo.setHorizontalHeaderLabels(["ID", "Üye Adı Soyadı"])
        lay.addWidget(self.tablo)
        
        self.btn_ekle = QPushButton("Seçili Üyeyi Ata")
        self.btn_ekle.clicked.connect(self._ata)
        lay.addWidget(self.btn_ekle)
        
        self._listele()

    def _listele(self):
        # Henüz bu antrenöre atanmamış üyeleri listele
        rows = db_baglanti.sorgu_calistir("""
            SELECT uye_id, ad || ' ' || soyad FROM uyeler 
            WHERE uye_id NOT IN (SELECT uye_id FROM uye_Antrenor WHERE antrenor_id = ?)
        """, (self.antrenor_id,))
        
        for row_idx, row_data in enumerate(rows):
            self.tablo.insertRow(row_idx)
            self.tablo.setItem(row_idx, 0, QTableWidgetItem(str(row_data[0])))
            self.tablo.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))

    def _ata(self):
        sel = self.tablo.selectedItems()
        if not sel: return
        uye_id = self.tablo.item(sel[0].row(), 0).text()
        
        db_baglanti.sorgu_calistir("INSERT INTO uye_Antrenor (uye_id, antrenor_id) VALUES (?, ?)", 
                                   (uye_id, self.antrenor_id))
        self.accept()