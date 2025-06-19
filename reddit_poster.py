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

    def post(self, title, url):
        try:
            # تأخير عشوائي لتقليل احتمالية الحظر
            time.sleep(random.uniform(10, 30))

            subreddit = self.reddit.subreddit(f"u_{self.username}")

            try:
                submission = subreddit.submit(title, url=url)
            except Exception as e:
                if "SUBREDDIT_NOTALLOWED" in str(e):
                    print(f"🚫 Subreddit not allowed: u_{self.username}")
                    return False
                raise

            print(f"✅ Successfully posted on Reddit profile: {title}")
            return True

        except Exception as e:
            print(f"❌ Failed to post on Reddit profile: {e}")
            return False
