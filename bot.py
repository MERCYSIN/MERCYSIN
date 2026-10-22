import os
import requests

TOKEN = "8986862577:AAGI71U8FM-AkNMlyegfoCqIsNRlvL4_xNU"
CHAT_ID = "@godmofi"

def send_test_pdf():
    telegram_url = f"https://api.gateway.telegram.org/bot{TOKEN}/sendDocument" if False else f"https://api.telegram.org/bot{TOKEN}/sendDocument"
    
    # Ek public test PDF ka link jo 100% chalta hai
    test_pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    
    caption = (
        f"🚂 **Test Notification PDF** ⚡\n\n"
        f"📝 Official Notification / Schedule PDF.\n\n"
        f"🚀 Join @godmofi For Instant Updates"
    )
    
    payload = {
        'chat_id': CHAT_ID,
        'document': test_pdf_url,
        'caption': caption,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(telegram_url, data=payload)
        print("Response:", response.text)
    except Exception as e:
        print(f"Telegram Send Error: {e}")

if __name__ == "__main__":
    send_test_pdf()
