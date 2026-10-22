import os
import requests
from bs4 import BeautifulSoup

TOKEN = "8986862577:AAGI71U8FM-AkNMlyegfoCqIsNRlvL4_xNU"
CHAT_ID = "@godmofi"
RECORD_FILE = "sent_pdfs.txt"

def load_sent_pdfs():
    if not os.path.exists(RECORD_FILE):
        return set()
    with open(RECORD_FILE, "r") as f:
        return set(f.read().splitlines())

def save_sent_pdf(pdf_url):
    with open(RECORD_FILE, "a") as f:
        f.write(pdf_url + "\n")

def send_to_telegram(link_url, link_text):
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    
    caption = (
        f"🚂 **{link_text}** ⚡\n\n"
        f"📝 Official Railway Notification / PDF Update.\n\n"
        f"🚀 Join @godmofi For Instant Updates"
    )
    
    payload = {
        'chat_id': CHAT_ID,
        'document': link_url,
        'caption': caption,
        'parse_mode': 'Markdown'
    }
    
    try:
        resp = requests.post(telegram_url, data=payload)
        if resp.status_code != 200:
            msg_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            msg_payload = {
                'chat_id': CHAT_ID,
                'text': f"🚂 **{link_text}**\n🔗 Link: {link_url}\n\n🚀 Join @godmofi",
                'parse_mode': 'Markdown'
            }
            requests.post(msg_url, data=msg_payload)
    except Exception as e:
        print(f"Telegram Send Error: {e}")

def check_all_websites():
    if not os.path.exists("urls.txt"):
        return

    with open("urls.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    sent_pdfs = load_sent_pdfs()

    for target_url in urls:
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(target_url, headers=headers, timeout=20)
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.text.strip()
                
                # Naye portal ke patterns (.pdf, examsDocuments, image, ya getdata) ko target karega
                if any(kw in href.lower() for kw in ['.pdf', 'examsdocuments', 'getdata', 'image/']):
                    if not href.startswith('http'):
                        href = requests.compat.urljoin(target_url, href)

                    if href not in sent_pdfs:
                        pdf_name = text or "RRB Official Notice PDF"
                        pdf_name = pdf_name.replace('\n', ' ').strip()
                        if len(pdf_name) > 80:
                            pdf_name = pdf_name[:77] + "..."
                        
                        send_to_telegram(href, pdf_name)
                        save_sent_pdf(href)
                        sent_pdfs.add(href)
        except Exception as e:
            print(f"Error on {target_url}: {e}")

if __name__ == "__main__":
    check_all_websites()
