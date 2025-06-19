import pytumblr
import os
import time
import random

class TumblrPoster:
    def __init__(self):
        self.consumer_key = os.getenv("TUMBLR_CONSUMER_KEY")
        self.consumer_secret = os.getenv("TUMBLR_CONSUMER_SECRET")
        self.oauth_token = os.getenv("TUMBLR_OAUTH_TOKEN")
        self.oauth_secret = os.getenv("TUMBLR_OAUTH_SECRET")
        self.blog_name = os.getenv("TUMBLR_BLOG_NAME")  # مثلاً yourblog.tumblr.com

        if not all([self.consumer_key, self.consumer_secret, self.oauth_token, self.oauth_secret, self.blog_name]):
            raise ValueError("Missing Tumblr API credentials or blog name in environment variables.")

        self.client = pytumblr.TumblrRestClient(
            self.consumer_key,
            self.consumer_secret,
            self.oauth_token,
            self.oauth_secret
        )

    def post(self, title, url=None):
        try:
            # بناء نص المنشور
            body = title
            if url:
                body += f"\n{url}"

            # تأخير عشوائي
            time.sleep(random.uniform(5, 15))

            self.client.create_text(self.blog_name, state="published", title=title, body=body)
            print(f"✅ Successfully posted to Tumblr: {title[:50]}...")
            return True
        except Exception as e:
            print(f"❌ Failed to post on Tumblr: {e}")
            return False
