import praw
import random
import time
import os

class RedditPoster:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent="AgentBot/0.1"
        )

    def post(self, subreddit_name, title, url):
        """
        نشر الرابط في Subreddit مع عنوان جذاب.
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            time.sleep(random.uniform(10, 30))  # تأخير لمحاكاة التفاعل البشري
            subreddit.submit(title, url=url)
            print(f"✅ Posted on Reddit: {title}")
            return True
        except Exception as e:
            print(f"❌ Reddit post failed: {e}")
            return False
