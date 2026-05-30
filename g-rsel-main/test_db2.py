import sys
import traceback
def log(msg): print(msg, flush=True)

try:
    import db_baglanti
    log("Connecting...")
    bag = db_baglanti.baglan()
    log("Connected. Getting cursor...")
    cur = bag.cursor()
    log("Executing...")
    cur.execute("SELECT 1", ())
    log("Fetching...")
    sonuc = cur.fetchall()
    log(f"Sonuc: {sonuc}")
    cur.close()
    bag.close()
except Exception as e:
    traceback.print_exc()
