import requests
from concurrent.futures import ThreadPoolExecutor
import time

class ProxyManager:
    REQUIRED_PROXIES = 500
    PROXIES_PER_SOURCE = 150

    PROXY_SOURCES = [
        "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    ]

    def __init__(self):
        self.final_proxies = set()

    def fetch_proxies_from_source(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            proxies = list(set(response.text.strip().splitlines()))
            return proxies[:self.PROXIES_PER_SOURCE]
        except Exception as e:
            print(f"[!] Failed to fetch from {url}: {e}")
            return []

    def test_proxy(self, proxy):
        try:
            response = requests.get(
                "https://ipinfo.io/json",
                proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                timeout=5,
            )
            data = response.json()
            country = data.get("country", "")
            if country in ["DE", "FR", "NL", "SE", "NO", "FI", "IT", "ES", "BE", "CH", "AT", "DK", "IE", "GB", "PL"]:
                return proxy
        except:
            pass
        return None

    def fetch_and_test_proxies(self):
        tried_sources = set()
        while len(self.final_proxies) < self.REQUIRED_PROXIES:
            print(f"\n[*] Looking for proxies... {len(self.final_proxies)}/{self.REQUIRED_PROXIES}")

            all_candidates = set()
            for source in self.PROXY_SOURCES:
                if source in tried_sources:
                    continue
                candidates = self.fetch_proxies_from_source(source)
                all_candidates.update(candidates)
                tried_sources.add(source)

            if not all_candidates:
                print("[!] No new proxies fetched. Retrying in 10 seconds...")
                time.sleep(10)
                tried_sources.clear()
                continue

            print(f"[+] Testing {len(all_candidates)} proxies...")
            with ThreadPoolExecutor(max_workers=100) as executor:
                results = list(executor.map(self.test_proxy, all_candidates))

            valid = set(filter(None, results))
            self.final_proxies.update(valid)

            if len(self.final_proxies) >= self.REQUIRED_PROXIES:
                print(f"[✓] Found {len(self.final_proxies)} valid proxies.")
                break
            else:
                print(f"[-] Only {len(self.final_proxies)} valid so far. Retrying...")

            time.sleep(5)
            tried_sources.clear()

    def get_valid_proxies(self):
        return list(self.final_proxies)
