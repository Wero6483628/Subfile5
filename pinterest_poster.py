import requests
import random
import time
import os

class PinterestPoster:
    def __init__(self):
        self.access_token = os.getenv("PINTEREST_ACESS_TOKEN")
        self.board_id = os.getenv("PINTEREST_BOARD_ID")

        if not all([self.access_token, self.board_id]):
            raise ValueError("❌ Missing Pinterest credentials in environment variables.")

    def post(self, note, link, image_url=None):
        try:
            url = "https://api.pinterest.com/v5/pins"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            data = {
                "board_id": self.board_id,
                "title": note,
                "link": link,
                "media_source": {
                    "source_type": "image_url",
                    "url": image_url or "https://i.imgur.com/abc123.jpg"
                }
            }

            time.sleep(random.uniform(10, 30))  # Delay before posting
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 201:
                print(f"✅ Posted on Pinterest: {note}")
                return True
            else:
                print(f"❌ Pinterest post failed: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Pinterest post exception: {e}")
            return False
