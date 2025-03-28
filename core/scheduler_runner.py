import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import schedule
import time
from main import main as envia_emails

def run():
    # Teste a cada minuto no segundo 30
    schedule.every().minute.at(":30").do(envia_emails)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run()
