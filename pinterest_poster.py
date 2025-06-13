import requests
import random
import time

class PinterestPoster:
    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = "https://api.pinterest.com/v1/pins/"

    def post(self, board_id, note, link):
        """
        نشر Pin جديد على لوحة Pinterest.
        """
        url = f"{self.base_url}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "board": board_id,
            "note": note,
            "link": link,
            # يمكنك إضافة "image_url" هنا لو لديك صورة
        }

        try:
            # تأخير عشوائي لمحاكاة سلوك بشري
            time.sleep(random.uniform(10, 30))
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                print(f"✅ Posted on Pinterest: {note}")
                return True
            else:
                print(f"❌ Pinterest post failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Pinterest post exception: {e}")
            return False
