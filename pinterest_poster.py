import requests
import random
import time

def post_to_pinterest(access_token, board_id, note, link, image_url=None):
    """
    دالة بسيطة تنشر Pin جديد على لوحة Pinterest معينة.
    (هذه نسخة مبدئية، تحتاج تضبيط بناءً على توثيق API الفعلي)
    """
    try:
        # تأخير عشوائي لمحاكاة التفاعل البشري
        time.sleep(random.uniform(10, 30))

        url = f"https://api.pinterest.com/v1/pins/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "board": board_id,
            "note": note,
            "link": link,
        }
        if image_url:
            data["image_url"] = image_url

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
