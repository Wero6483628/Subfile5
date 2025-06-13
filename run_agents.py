import json
from agent import run_agent

def load_accounts():
    with open("account.json", "r") as f:
        return json.load(f)

def main():
    accounts = load_accounts()

    with open("agent_config.json", "r") as f:
        config = json.load(f)

    for agent in config["agents"]:
        reddit_account = accounts['reddit'][agent['id'] % len(accounts['reddit'])] if accounts['reddit'] else None
        pinterest_account = accounts['pinterest'][agent['id'] % len(accounts['pinterest'])] if accounts['pinterest'] else None

        run_agent(
            agent_id=agent['id'],
            proxy=agent['proxy'],
            articles=agent['articles_to_visit'],
            reddit_account=reddit_account,
            pinterest_account=pinterest_account
        )

if __name__ == "__main__":
    main()
