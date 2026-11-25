import os, smtplib, requests, yfinance as yf
from email.message import EmailMessage

SYMBOL = os.getenv("SYMBOL", "^NDX")          # ^IXIC = Composite, NQ=F = futures
TARGET = float(os.getenv("TARGET", "26300"))
DIRECTION = os.getenv("DIRECTION", "above")   # "above" or "below"

TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT = os.getenv("TG_CHAT_ID")
GMAIL = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PW = os.getenv("GMAIL_APP_PASSWORD")

def notify(msg):
    if TG_TOKEN and TG_CHAT:
        requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                      data={"chat_id": TG_CHAT, "text": msg}, timeout=15)
    if GMAIL and GMAIL_APP_PW:
        m = EmailMessage()
        m["Subject"], m["From"], m["To"] = "Nasdaq alert", GMAIL, GMAIL
        m.set_content(msg)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(GMAIL, GMAIL_APP_PW)
            s.send_message(m)

price = float(yf.Ticker(SYMBOL).fast_info["last_price"])
hit = price >= TARGET if DIRECTION == "above" else price <= TARGET
print(f"{SYMBOL}: {price:.2f} | target {TARGET} ({DIRECTION}) | hit={hit}")

if hit:
    notify(f"{SYMBOL} is {price:.2f} (target {TARGET} {DIRECTION})")
    with open(os.environ["GITHUB_OUTPUT"], "a") as f:
        f.write("hit=true\n")
