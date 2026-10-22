import os
import requests
from bs4 import BeautifulSoup

def test_print():
    target_url = "https://rrb.indianrailways.gov.in/getdata?loc=thiruvananthapuram"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target_url, headers=headers, timeout=15)
        print("Status Code:", response.status_code)
        print("Page Length:", len(response.text))
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        print(f"Total <a> tags found: {len(links)}")
        
        for link in links[:5]:
            print("Found Link:", link['href'], "Text:", link.text.strip())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_print()
