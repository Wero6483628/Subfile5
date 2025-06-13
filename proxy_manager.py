import requests
from concurrent.futures import ThreadPoolExecutor
import time

class ProxyManager:
    REQUIRED_PROXIES = 100  # سيتم تغييره لاحقًا حسب الرقم العشوائي
    PROXIES_PER_SOURCE = 500

    PROXY_SOURCES = [
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
        "https://proxyspace.pro/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt"
    ]

    EUROPEAN_COUNTRIES = {"DE", "FR", "NL", "SE", "NO", "FI", "IT", "ES", "BE", "CH", "AT", "DK", "IE", "GB", "PL"}

    def __init__(self, required_count):
        self.REQUIRED_PROXIES = required_count
        self.final_proxies = set()

    def fetch_proxies_from_source(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return list(set(response.text.strip().splitlines()))[:self.PROXIES_PER_SOURCE]
        except:
            return []

    def test_proxy(self, proxy):
        try:
            response = requests.get(
                "https://ipinfo.io/json",
                proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                timeout=5,
            )
            data = response.json()
            if data.get("country") in self.EUROPEAN_COUNTRIES:
                return proxy
        except:
            pass
        return None

    def fetch_and_test_proxies(self):
        while len(self.final_proxies) < self.REQUIRED_PROXIES:
            all_candidates = set()
            for source in self.PROXY_SOURCES:
                all_candidates.update(self.fetch_proxies_from_source(source))

            with ThreadPoolExecutor(max_workers=100) as executor:
                results = executor.map(self.test_proxy, all_candidates)
                self.final_proxies.update(filter(None, results))

            time.sleep(3)

        return list(self.final_proxies)[:self.REQUIRED_PROXIES]
