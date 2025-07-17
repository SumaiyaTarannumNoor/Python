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



def scrape_azquotes():
    url = 'https://www.azquotes.com/quotes/topics/one-liners.html'
    response = requests.get(url, headers=get_headers())
    soup = BeautifulSoup(response.text, 'html.parser')


    quotes = [a.text.strip() for a in soup.select("a.title") if len(a.text.strip()) > 10]

    with open("azquotes.txt", "w", encoding="utf-8") as f:
        for quote in quotes:
            f.write(quote + "\n")

    print(f"AZQuotes: {len(quotes)} quotes saved to azquotes.txt.")   


scrape_azquotes()         
