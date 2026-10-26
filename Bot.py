
import os
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import html

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL_ID"]

FEEDS = [
    "https://www.federalreserve.gov/feeds/press_all.xml",
    "https://www.eia.gov/rss/todayinenergy.xml",
    "https://www.bls.gov/feed/news_release/empsit.rss",
]

def send(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": CHANNEL,
        "text": text,
        "disable_web_page_preview": "true"
    }).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.status == 200

for feed in FEEDS:
    try:
        req = urllib.request.Request(
            feed, headers={"User-Agent": "MARKGlobalTrading/1.0"}
        )
        root = ET.fromstring(urllib.request.urlopen(req, timeout=20).read())
        for item in root.findall(".//item")[:3]:
            title = item.findtext("title", default="").strip()
            link = item.findtext("link", default="").strip()
            if title and link:
                message = (
                    "🌍 MARK GLOBAL TRADING\n\n"
                    f"📰 {html.unescape(title)}\n\n"
                    f"🔗 {link}\n\n"
                    "تداول بثقة، تداول بأمان"
                )
                send(message)
    except Exception as e:
        print(f"Feed error: {e}")
