import sys
from PyQt5.QtWidgets import QApplication
from admin_panel import AdminPanel

if __name__ == '__main__':
    app = QApplication(sys.argv)
    kullanici = {'kullanici_id': 1, 'ad': 'Ahmet', 'soyad': 'Yılmaz', 'rol': 'admin'}
    print("Creating panel...", flush=True)
    panel = AdminPanel(kullanici)
    print("Showing panel...", flush=True)
    panel.show()
    print("Executing app...", flush=True)
    sys.exit(app.exec_())
