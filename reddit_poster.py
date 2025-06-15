import praw
import random
import time
import os

class RedditPoster:
    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.username = os.getenv("REDDIT_USERNAME")
        self.password = os.getenv("REDDIT_PASSWORD")
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "AgentBot/0.1")

        if not all([self.client_id, self.client_secret, self.username, self.password]):
            raise ValueError("❌ Missing Reddit credentials in environment variables.")

        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            username=self.username,
            password=self.password,
            user_agent=self.user_agent
        )

    def post(self, subreddit_name, title, url):
        try:
            time.sleep(random.uniform(10, 30))
            subreddit = self.reddit.subreddit(subreddit_name)
            subreddit.submit(title, url=url)
            print(f"✅ Posted on Reddit: {title}")
            return True
        except Exception as e:
            print(f"❌ Reddit post failed: {e}")
            return False
