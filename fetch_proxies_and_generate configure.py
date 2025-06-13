import random
import json
from proxy_manager import ProxyManager
from get_articles import get_articles_from_blog

BLOG_URL = "https://ammuse12345.blogspot.com"
AGENT_RANGE = (100, 500)

def main():
    agent_count = random.randint(*AGENT_RANGE)
    print(f"[•] Generating {agent_count} agents...")

    proxy_manager = ProxyManager(agent_count)
    proxies = proxy_manager.fetch_and_test_proxies()

    articles = get_articles_from_blog(BLOG_URL)
    if not articles:
        print("[×] No articles found.")
        return

    with open("account.json", "r") as f:
        accounts = json.load(f)

    config = {"agents": []}
    for i in range(agent_count):
        config["agents"].append({
            "id": i,
            "proxy": proxies[i % len(proxies)],
            "articles_to_visit": random.sample(articles, min(3, len(articles))),
            "platforms": ["reddit", "pinterest"]
        })

    with open("agent_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print(f"[✓] Config generated for {agent_count} agents.")

if __name__ == "__main__":
    main()
