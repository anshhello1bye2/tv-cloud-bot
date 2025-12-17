import imaplib
import email
import time
import os

GMAIL_ID = os.environ.get("GMAIL_ID")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

def connect():
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(GMAIL_ID, GMAIL_APP_PASSWORD)
    imap.select("inbox")
    return imap

print("☁️ TradingView cloud bot started")

seen = set()
imap = connect()

while True:
    try:
        status, messages = imap.search(None, '(FROM "noreply@tradingview.com")')

        if status == "OK":
            for num in messages[0].split():
                if num in seen:
                    continue

                _, data = imap.fetch(num, "(RFC822)")
                msg = email.message_from_bytes(data[0][1])
                subject = msg["subject"]

                print("🚨 ALERT RECEIVED:", subject)

                seen.add(num)

        time.sleep(10)

    except Exception as e:
        print("⚠️ Error, reconnecting:", e)
        time.sleep(5)
        imap = connect()
