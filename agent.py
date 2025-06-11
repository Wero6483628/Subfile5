import json
import time
import random
import os
import requests

MAX_RETRIES = 3

# تحميل الحسابات من account.json
def load_accounts():
    if os.path.exists("account.json"):
        try:
            with open("account.json", "r") as f:
                accounts = json.load(f)
                return accounts
        except Exception as e:
            print(f"[⚠️] Failed to load account.json: {e}")
    return {"reddit": [], "pinterest": []}

# توزيع عشوائي لحساب من نوع معين
def get_random_account(accounts, platform):
    return random.choice(accounts.get(platform, [])) if accounts.get(platform) else None

def simulate_article_visit(url, proxy=None):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if proxy:
                print(f"[👣][Attempt {attempt}] Visiting {url} using proxy {proxy}")
                proxies = {
                    "http": proxy,
                    "https": proxy,
                }
            else:
                print(f"[👣][Attempt {attempt}] Visiting {url} without proxy")
                proxies = None

            # مثال بسيط لزيارة الصفحة (GET request)
            response = requests.get(url, proxies=proxies, timeout=10)
            if response.status_code == 200:
                time.sleep(random.uniform(2, 5))  # محاكاة وقت قراءة
                print(f"[✅] Successfully visited {url}")
                return True
            else:
                print(f"[❌] Failed to visit article, status code: {response.status_code}")
                time.sleep(2)
        except Exception as e:
            print(f"[❌] Error visiting article (attempt {attempt}): {e}")
            time.sleep(2)
    print(f"[⚠️] Failed to visit {url} after {MAX_RETRIES} attempts")
    return False

def post_to_reddit(article_url, account):
    token = account.get("reddit_token")
    username = account.get("reddit_username")
    if not token or not username:
        print(f"[⚠️] Missing Reddit token or username for account {username}")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": f"script by /u/{username}"
    }

    data = {
        "sr": "testsubreddit",  # استبدلها بالـ subreddit المناسب
        "title": f"Check this article: {article_url}",
        "url": article_url,
        "kind": "link"
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[📢][Attempt {attempt}] Reddit post by {username}: {article_url}")
            response = requests.post("https://oauth.reddit.com/api/submit", headers=headers, data=data, timeout=10)
            if response.status_code == 200 or response.status_code == 201:
                print(f"[✅] Successfully posted on Reddit: {article_url}")
                return True
            else:
                print(f"[❌] Reddit posting failed with status {response.status_code}: {response.text}")
            time.sleep(2)
        except Exception as e:
            print(f"[❌] Reddit posting error (attempt {attempt}): {e}")
            time.sleep(2)
    print(f"[⚠️] Failed to post on Reddit after {MAX_RETRIES} attempts")
    return False

def post_to_pinterest(article_url, account):
    token = account.get("pinterest_token")
    username = account.get("pinterest_username")
    if not token or not username:
        print(f"[⚠️] Missing Pinterest token or username for account {username}")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # مثال payload للنشر (يحتاج تعديل حسب API الفعلي لـ Pinterest)
    data = {
        "board": "me/my-board",  # عدل حسب البورد المناسب
        "note": f"Check out this article: {article_url}",
        "link": article_url,
        "image_url": "https://example.com/image.jpg"  # اختياري، حط صورة مناسبة أو احذف المفتاح
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[📌][Attempt {attempt}] Pinterest post by {username}: {article_url}")
            response = requests.post("https://api.pinterest.com/v1/pins/", headers=headers, json=data, timeout=10)
            if response.status_code in (200, 201):
                print(f"[✅] Successfully posted on Pinterest: {article_url}")
                return True
            else:
                print(f"[❌] Pinterest posting failed with status {response.status_code}: {response.text}")
            time.sleep(2)
        except Exception as e:
            print(f"[❌] Pinterest posting error (attempt {attempt}): {e}")
            time.sleep(2)
    print(f"[⚠️] Failed to post on Pinterest after {MAX_RETRIES} attempts")
    return False

def run_agent(agent_config, global_accounts):
    proxy = agent_config.get("proxy")
    delay = agent_config.get("delay", 5)
    articles = agent_config.get("articles_to_visit", [])
    platforms = agent_config.get("platforms", [])

    if not articles:
        print("[❌] No articles assigned to this agent.")
        return

    for url in articles:
        if not simulate_article_visit(url, proxy):
            continue

        if "reddit" in platforms:
            reddit_account = get_random_account(global_accounts, "reddit")
            if reddit_account:
                post_to_reddit(url, reddit_account)
            else:
                print("[⚠️] No Reddit account available.")

        if "pinterest" in platforms:
            pinterest_account = get_random_account(global_accounts, "pinterest")
            if pinterest_account:
                post_to_pinterest(url, pinterest_account)
            else:
                print("[⚠️] No Pinterest account available.")

        time.sleep(delay)

def main():
    global_accounts = load_accounts()

    try:
        with open("agent_config.json", "r") as f:
            config = json.load(f)
    except Exception as e:
        print(f"[❌] Failed to load agent_config.json: {e}")
        return

    agents = config.get("agents", [])
    print(f"[ℹ️] Starting {len(agents)} agents...")

    for agent in agents:
        run_agent(agent, global_accounts)

if __name__ == "__main__":
    main()
