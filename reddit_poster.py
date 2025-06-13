import praw
import random
import time

class RedditPoster:
    def __init__(self, client_id, client_secret, username, password, user_agent="AgentBot/0.1"):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )
    
    def post(self, subreddit_name, title, url):
        """
        نشر الرابط في Subreddit مع عنوان جذاب.
        """
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            # تأخير عشوائي قبل النشر لمحاكاة التفاعل البشري
            time.sleep(random.uniform(10, 30))
            submission = subreddit.submit(title, url=url)
            print(f"✅ Posted on Reddit: {title}")
            return True
        except Exception as e:
            print(f"❌ Reddit post failed: {e}")
            return False
