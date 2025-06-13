import requests
from bs4 import BeautifulSoup

def get_articles_from_blog(blog_url):
    try:
        response = requests.get(blog_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        return list({link['href'] for link in links if link.get('href', '').startswith("https://")})
    except Exception as e:
        print(f"Error fetching articles: {e}")
        return []
