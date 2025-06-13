import requests
from bs4 import BeautifulSoup

def get_articles(proxy):
    """
    يجلب روابط المقالات من مدونة بلوجر باستخدام بروكسي محدد.
    """
    url = "https://ammuse12345.blogspot.com"
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }

    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch blog: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        articles = []
        for link in links:
            href = link.get('href')
            if href and href.startswith("https://ammuse1234.blogspot.com/") and "/search" not in href:
                articles.append(href)

        # إزالة التكرار
        articles = list(set(articles))

        print(f"✅ Found {len(articles)} articles.")
        return articles

    except Exception as e:
        print(f"❌ Error fetching articles: {e}")
        return []
