 import json
from proxy import ProxyManager
from agent import Agent
import asyncio

def load_accounts(filepath="account.json"):
    with open(filepath, "r") as f:
        accounts = json.load(f)
    return accounts

async def main():
    accounts = load_accounts()
    print(f"Loaded {len(accounts)} accounts.")

    proxy_manager = ProxyManager()
    print("Fetching and testing proxies...")
    proxy_manager.fetch_and_test_proxies()  # sync method, لا تستخدم await هنا
    valid_proxies = proxy_manager.get_valid_proxies()
    print(f"Valid proxies found: {len(valid_proxies)}")

    num_agents = min(len(accounts), len(valid_proxies))
    print(f"Running {num_agents} agents...")

    agents = []
    for i in range(num_agents):
        account = accounts[i]
        proxy = valid_proxies[i]
        agent = Agent(account=account, proxy=proxy)
        agents.append(agent)

    await asyncio.gather(*(agent.run() for agent in agents))

if __name__ == "__main__":
    asyncio.run(main())
