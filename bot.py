import os
import requests
from bs4 import BeautifulSoup

TOKEN = "8986862577:AAGI71U8FM-AkNMlyegfoCqIsNRlvL4_xNU"
CHAT_ID = "@godmofi"
RECORD_FILE = "sent_pdfs.txt"

ZONES = {
    "Thiruvananthapuram": "https://rrb.indianrailways.gov.in/getdata?loc=thiruvananthapuram",
    "Chennai": "https://rrb.indianrailways.gov.in/getdata?loc=chennai",
    "Ajmer": "https://rrb.indianrailways.gov.in/getdata?loc=ajmer",
    "Ahmedabad": "https://rrb.indianrailways.gov.in/getdata?loc=ahmedabad",
    "Bengaluru": "https://rrb.indianrailways.gov.in/getdata?loc=bengaluru",
    "Bhopal": "https://rrb.indianrailways.gov.in/getdata?loc=bhopal",
    "Bhubaneswar": "https://rrb.indianrailways.gov.in/getdata?loc=bhubaneswar",
    "Bilaspur": "https://rrb.indianrailways.gov.in/getdata?loc=bilaspur",
    "Chandigarh": "https://rrb.indianrailways.gov.in/getdata?loc=chandigarh",
    "Gorakhpur": "https://rrb.indianrailways.gov.in/getdata?loc=gorakhpur",
    "Guwahati": "https://rrb.indianrailways.gov.in/getdata?loc=guwahati",
    "Jammu": "https://rrb.indianrailways.gov.in/getdata?loc=jammu",
    "Kolkata": "https://rrb.indianrailways.gov.in/getdata?loc=kolkata",
    "Malda": "https://rrb.indianrailways.gov.in/getdata?loc=malda",
    "Mumbai": "https://rrb.indianrailways.gov.in/getdata?loc=mumbai",
    "Muzaffarpur": "https://rrb.indianrailways.gov.in/getdata?loc=muzaffarpur",
    "Patna": "https://rrb.indianrailways.gov.in/getdata?loc=patna",
    "Prayagraj": "https://rrb.indianrailways.gov.in/getdata?loc=prayagraj",
    "Ranchi": "https://rrb.indianrailways.gov.in/getdata?loc=ranchi",
    "Secunderabad": "https://rrb.indianrailways.gov.in/getdata?loc=secunderabad",
    "Siliguri": "https://rrb.indianrailways.gov.in/getdata?loc=siliguri"
}

def load_sent_pdfs():
    if not os.path.exists(RECORD_FILE):
        return set()
    with open(RECORD_FILE, "r") as f:
        return set(f.read().splitlines())

def save_sent_pdf(pdf_url):
    with open(RECORD_FILE, "a") as f:
        f.write(pdf_url + "\n")

def send_to_telegram(link_url, link_text, zone_name):
    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    caption = (
        f"🚨 **RRB {zone_name} Update** 🚂\n\n"
        f"📄 **{link_text}**\n\n"
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
                'text': f"🚨 **RRB {zone_name} Update**\n📄 {link_text}\n🔗 Link: {link_url}\n\n🚀 Join @godmofi",
                'parse_mode': 'Markdown'
            }
            requests.post(msg_url, data=msg_payload)
    except Exception as e:
        print(f"Telegram Send Error: {e}")

def check_all_zones():
    sent_pdfs = load_sent_pdfs()

    for zone_name, target_url in ZONES.items():
        try:
            proxy_url = f"https://api.codetabs.com/v1/proxy?quest={requests.utils.quote(target_url)}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            
            response = requests.get(proxy_url, headers=headers, timeout=25)
            
            if response.status_code == 200:
                html_content = response.text
                if response.headers.get('content-type', '').startswith('application/json'):
                    try:
                        res_json = response.json()
                        if isinstance(res_json, dict) and 'contents' in res_json:
                            html_content = res_json['contents']
                    except:
                        pass

                soup = BeautifulSoup(html_content, 'html.parser')
                links = soup.find_all('a', href=True)
                
                # Yahan print karke dekhenge ki site se kya links mil rahe hain
                print(f"--- {zone_name}: Total Links Found: {len(links)} ---")
                
                for link in links:
                    href = link['href']
                    text = link.text.strip()
                    print(f"Link: {href} | Text: {text[:30]}") # Debug print
                    
                    if any(kw in href.lower() for kw in ['.pdf', 'examsdocuments', 'getdata', 'image/']):
                        if not href.startswith('http'):
                            href = requests.compat.urljoin(target_url, href)

                        if href not in sent_pdfs:
                            pdf_name = text or f"RRB {zone_name} Official Notice"
                            pdf_name = pdf_name.replace('\n', ' ').strip()
                            if len(pdf_name) > 80:
                                pdf_name = pdf_name[:77] + "..."
                            
                            send_to_telegram(href, pdf_name, zone_name)
                            save_sent_pdf(href)
                            sent_pdfs.add(href)
        except Exception as e:
            print(f"Error on {zone_name}: {e}")

if __name__ == "__main__":
    check_all_zones()
