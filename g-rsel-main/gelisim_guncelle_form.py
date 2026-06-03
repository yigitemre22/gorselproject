from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
import db_baglanti

class GelisimGuncelleForm(QDialog):
    def __init__(self, row_data, parent=None):
        super().__init__(parent)
        self.row_data = row_data # [Ad, Soyad, Kilo, Boy, Yağ, Tarih, ID]
        self.setWindowTitle("Üye Gelişimi Güncelle")
        self.setMinimumWidth(300)

        # Layout oluştur
        layout = QVBoxLayout()
        
        # row_data içerisindeki indeksleri tablonuzdaki sütun sırasına göre ayarladık:
        # 0:Ad, 1:Soyad, 2:Kilo, 3:Boy, 4:Yağ, 5:Tarih, 6:gelisim_id
        
        self.input_kilo = QLineEdit(str(row_data[2])) 
        self.input_boy = QLineEdit(str(row_data[3]))  
        self.input_yag = QLineEdit(str(row_data[4]))  
        
        layout.addWidget(QLabel("Kilo (KG):"))
        layout.addWidget(self.input_kilo)
        layout.addWidget(QLabel("Boy (M):"))
        layout.addWidget(self.input_boy)
        layout.addWidget(QLabel("Yağ Oranı (%):"))
        layout.addWidget(self.input_yag)
        
        btn_kaydet = QPushButton("Kaydet")
        btn_kaydet.clicked.connect(self._kaydet)
        layout.addWidget(btn_kaydet)
        
        self.setLayout(layout)

    def _kaydet(self):
        # row_data[6] bizim gelisim_id değerimizdir
        gelisim_id = self.row_data[6]
        
        # Veritabanında tablonuzun adı 'gelisim' olarak düzeltildi
        sorgu = "UPDATE gelisim SET kilo = ?, boy = ?, yag_orani = ? WHERE gelisim_id = ?"
        
        try:
            db_baglanti.sorgu_calistir(sorgu, (
                self.input_kilo.text(), 
                self.input_boy.text(), 
                self.input_yag.text(), 
                gelisim_id
            ))
            self.accept() # İşlem başarılıysa formu kapat
        except Exception as e:
            print(f"Güncelleme hatası: {e}")