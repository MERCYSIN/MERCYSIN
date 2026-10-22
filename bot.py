import os
import requests
from bs4 import BeautifulSoup

TOKEN = "8986862577:AAGI71U8FM-AkNMlyegfoCqIsNRlvL4_xNU"
CHAT_ID = "@godmofi"

def debug_check():
    target_url = "https://rrb.indianrailways.gov.in/getdata?loc=thiruvananthapuram"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links_found = []
        for link in soup.find_all('a', href=True):
            links_found.append(f"Text: {link.text.strip()} | Href: {link['href']}")
        
        # Pehle 10 links ko Telegram par text message me bhej do taaki humein pata chale site par kya hai
        debug_text = "\n".join(links_found[:10]) if links_found else "No links found!"
        
        telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(telegram_url, data={
            'chat_id': CHAT_ID,
            'text': f"🔍 **Debug Links:**\n{debug_text[:4000]}",
            'parse_mode': 'Markdown'
        })
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_check()
