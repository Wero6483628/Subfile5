import json
import random
from agent import run_agent
from concurrent.futures import ThreadPoolExecutor

def load_articles():
    try:
        with open("articles.json", "r") as f:
            return json.load(f)
    except:
        print("[⚠️] Failed to load articles.json")
        return []

def load_proxies():
    try:
        with open("proxies.json", "r") as f:
            return json.load(f)
    except:
        print("[❌] proxies.json not found or invalid.")
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
    print("[🤖] Starting AI Agent Runner...")

    proxies = load_proxies()
    if not proxies:
        return

    articles = load_articles()
    if not articles:
        print("[❌] No articles found. Exiting.")
        return

    agent_count = len(proxies)
    print(f"[ℹ️] Running {agent_count} agents...")

    agents = generate_agent_config(proxies, articles, agent_count)

    with open("account.json", "r") as f:
        accounts = json.load(f)

    with ThreadPoolExecutor(max_workers=30) as executor:
        for agent in agents:
            executor.submit(run_agent, agent, accounts)

    print("[✅] All agents submitted.")

if __name__ == "__main__":
    main()
