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
            url = "https://api.pinterest.com/v1/pins/"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            data = {
                "board": self.board_id,
                "note": note,
                "link": link,
            }
            if image_url:
                data["image_url"] = image_url

            time.sleep(random.uniform(10, 30))
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
