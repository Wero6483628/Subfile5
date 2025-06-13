import json
import random
from proxy_manager import ProxyManager

def save_proxies_to_file(proxies):
    with open("proxies.json", "w") as f:
        json.dump(proxies, f)
    print(f"[✅] Saved {len(proxies)} working proxies to proxies.json")

def main():
    print("[🔌] Starting proxy fetching and testing...")
    agent_count = random.randint(100, 500)
    print(f"[ℹ️] Required proxies: {agent_count}")

    pm = ProxyManager(required_count=agent_count)
    working_proxies = pm.fetch_and_test_proxies()

    save_proxies_to_file(working_proxies)
    print("[✅] Proxy fetching done.")

if __name__ == "__main__":
    main()
