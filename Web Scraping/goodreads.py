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

def scrape_goodreads():
    url='https://www.goodreads.com/quotes/tag/one-liner'
    response = requests.get(url,headers=get_headers())
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = []
    for div in soup.select('.quoteText'):
        text = div.get_text(strip=True).split("-")[0].strip()
        if len(text) >20:
            quotes.append(text)


    with open("goodreads.txt", "w", encoding="utf-8") as f:
        for quote in quotes:
            f.write(quote+ "\n")

    print(f"GoodReads: {len(quotes)} saved in goodreads.txt.")


scrape_goodreads()  