import requests
from bs4 import BeautifulSoup

url = 'https://www.goodreads.com/quotes'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}


response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch page: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

taglines = []
tagline_elements = soup.find_all(['li', 'div'], class_='quoteText')

print(f"Found {len(tagline_elements)} tagline elements")

for elem in tagline_elements:
    tagline = elem.get_text(strip=True)
    if 5 < len(tagline) < 150:
        taglines.append(tagline)

if not taglines:
    print("No taglines found. The page might be dynamically rendered with JavaScript.")
else:
    with open('quote.txt', 'w', encoding='utf-8') as f:
        for line in taglines:
            f.write(line + '\n')
    print(f"{len(taglines)} taglines saved to taglines.txt")
