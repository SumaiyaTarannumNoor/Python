import random
import requests
from bs4 import BeautifulSoup


USER_AGENTS = {
    "chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
    "edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
}

def get_headers():
    return {'User-Agent': random.choice(list(USER_AGENTS.values()))}

def scrape_quotefancy():
    url = 'https://quotefancy.com/short-motivational-quotes'
    response = requests.get(url, headers=get_headers())

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = []

    for item in soup.select("div.q-wrapper p.quote-p a.quote-a"):
        text = item.get_text(strip=True)
        if 5 < len(text) < 150:
            quotes.append(text)

    with open("quotefancy.txt","w", encoding = 'utf-8') as f:
          for quote in quotes:
            f.write(quote + "\n")

    print(f"Quotefancy: {len(quotes)} quotes saved on quotefancy.txt.") 


scrape_quotefancy()