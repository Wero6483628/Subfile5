import requests
import time
import random
from message_generator import generate_message

def simulate_article_visit(url, proxy=None):
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy} if proxy else None, timeout=10)
        if response.status_code == 200:
            print(f"[✓] Visited: {url}")
            time.sleep(random.uniform(2, 4))
            return True
    except Exception as e:
        print(f"[×] Visit failed: {e}")
    return False

def post_to_reddit(article_url, token, username):
    print(f"[Reddit] {username} posting: {article_url}")
    return True  # mock success

def post_to_pinterest(article_url, token, username):
    print(f"[Pinterest] {username} pinning: {article_url}")
    return True  # mock success

def run_agent(agent_id, proxy, articles, reddit_account, pinterest_account):
    for url in articles:
        simulate_article_visit(url, proxy)
        if reddit_account:
            post_to_reddit(url, reddit_account['reddit_token'], reddit_account['reddit_username'])
        if pinterest_account:
            post_to_pinterest(url, pinterest_account['pinterest_token'], pinterest_account['pinterest_username'])
        time.sleep(random.uniform(3, 7))
