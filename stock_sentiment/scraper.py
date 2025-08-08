import requests
from bs4 import BeautifulSoup

def fetch_news(query, max_articles=10):
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?q={query}+site:moneycontrol.com+OR+site:economictimes.indiatimes.com&tbm=nws"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = []
    for item in soup.find_all('div', attrs={'class': 'BVG0Nb'}, limit=max_articles):
        headlines.append(item.text)
    return headlines
