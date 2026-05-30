import sys
import traceback
def log(msg): print(msg, flush=True)

try:
    from admin_panel import sorgu_calistir
    log("Testing DB...")
    res = sorgu_calistir("SELECT 1")
    log(f"Result: {res}")
except Exception as e:
    traceback.print_exc()
