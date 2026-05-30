import sys
import traceback

def log(msg):
    print(msg, flush=True)

try:
    log("Importing...")
    from PyQt5.QtWidgets import QApplication
    from admin_panel import AdminPanel
    log("Starting app...")
    app = QApplication(sys.argv)
    log("Creating panel...")
    kullanici = {'kullanici_id': 1, 'ad': 'Ahmet', 'soyad': 'Yılmaz', 'rol': 'admin'}
    panel = AdminPanel(kullanici)
    log("Success!")
except Exception as e:
    traceback.print_exc()
