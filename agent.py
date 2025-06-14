import random
import time
import requests
from get_articles import get_articles
from bs4 import BeautifulSoup

class Agent:
    def __init__(self, proxy):
        self.proxy = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
        }

    def simulate_human_behavior(self, url):
        print(f"👀 Visiting: {url}")
        try:
            response = requests.get(url, proxies=self.proxy, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Scroll-like delay
            scroll_time = random.uniform(5, 12)
            print(f"🕒 Simulating read time: {int(scroll_time)}s")
            time.sleep(scroll_time)

            # Randomly interact with text or images (simulate)
            print("🧠 Simulating user interaction...")
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"❌ Failed to simulate behavior on {url}: {e}")

    def run(self):
        proxy_str = self.proxy["http"].replace("http://", "")
        articles = get_articles(proxy_str)
        if not articles:
            print("⚠️ No articles found.")
            return

        selected_articles = random.sample(articles, min(len(articles), random.randint(3, 5)))

        for article_url in selected_articles:
            try:
                self.simulate_human_behavior(article_url)

                # Generate unique message
                message = generate_message(article_url)
                print(f"📝 Message: {message}")

                # Post to Reddit
                print("📤 Posting to Reddit...")
                post_to_reddit(message, article_url)

                # Short delay before Pinterest
                time.sleep(random.randint(3, 6))

                # Post to Pinterest
                print("📌 Posting to Pinterest...")
                post_to_pinterest(message, article_url)

                # Wait between posts
                time.sleep(random.randint(8, 15))

            except Exception as e:
                print(f"❌ Error handling article {article_url}: {e}")
