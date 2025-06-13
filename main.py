import random
import json
import os
from proxy_manager import ProxyManager
from agent import run_agent
from concurrent.futures import ThreadPoolExecutor

def load_articles():
    try:
        with open("articles.json", "r") as f:
            return json.load(f)
    except:
        print("[⚠️] Failed to load articles.json")
        return []

def generate_agent_config(proxy_list, articles, agent_count):
    agents = []
    articles_per_agent = max(1, len(articles) // agent_count)
    random.shuffle(articles)

    for i in range(agent_count):
        agent_articles = articles[i * articles_per_agent:(i + 1) * articles_per_agent]
        agent = {
            "proxy": proxy_list[i] if i < len(proxy_list) else None,
            "delay": random.randint(5, 12),
            "articles_to_visit": agent_articles,
            "platforms": ["reddit", "pinterest"]
        }
        agents.append(agent)

    return agents

def main():
    print("[⚙️] Starting AI Agent system...")

    # عدد الـ Agents المطلوب (عشوائي بين 100 و 500)
    agent_count = random.randint(100, 500)
    print(f"[ℹ️] Agent count for this run: {agent_count}")

    # جلب البروكسيات الأوروبية الصالحة
    pm = ProxyManager(required_proxies=agent_count)
    pm.fetch_and_test_proxies()
    proxies = pm.get_valid_proxies()
    print(f"[✅] Got {len(proxies)} working proxies.")

    # تحميل المقالات من ملف خارجي
    articles = load_articles()
    if not articles:
        print("[❌] No articles found. Exiting.")
        return

    # توليد إعدادات الـ Agents
    agents = generate_agent_config(proxies, articles, agent_count)

    # تحميل الحسابات
    with open("account.json", "r") as f:
        accounts = json.load(f)

    # تشغيل كل Agent
    with ThreadPoolExecutor(max_workers=30) as executor:
        for agent in agents:
            executor.submit(run_agent, agent, accounts)

if __name__ == "__main__":
    main()
