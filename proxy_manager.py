import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ✅ قائمة الدول الأوروبية المسموح بها
EUROPEAN_COUNTRIES = {
    "fr",  # France
    "de",  # Germany
    "nl",  # Netherlands
    "it",  # Italy
    "es",  # Spain
    "gb",  # United Kingdom
    "pl",  # Poland
    "se",  # Sweden
    "fi",  # Finland
    "no",  # Norway
    "dk",  # Denmark
    "be",  # Belgium
    "at",  # Austria
    "ch",  # Switzerland
    "ie",  # Ireland
    "cz",  # Czech Republic
    "pt",  # Portugal
    "sk",  # Slovakia
    "gr",  # Greece
    "hu",  # Hungary
    "ro",  # Romania
    "bg",  # Bulgaria
    "hr",  # Croatia
    "ee",  # Estonia
    "lt",  # Lithuania
    "lv",  # Latvia
    "si",  # Slovenia
    "cy",  # Cyprus
    "lu",  # Luxembourg
}

# ⬇️ توليد رابط ديناميكي من الدول الأوروبية
country_param = ",".join(EUROPEAN_COUNTRIES)

# ✅ مصادر البروكسي
PROXY_SOURCES = [
    f"https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=3000&country={country_param}&ssl=all&anonymity=elite",
    "https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-List/master/proxy-list.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt"
]

# ✅ اختبار البروكسي
def is_proxy_working(proxy, test_url="https://ammuse12345.blogspot.com", timeout=7):
    try:
        response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=timeout)
        return response.status_code == 200
    except:
        return False

# ✅ تحميل البروكسيات من مصدر معين
def fetch_proxies_from_source(source_url):
    try:
        response = requests.get(source_url, timeout=10)
        proxies = response.text.strip().split("\n")
        return [p.strip() for p in proxies if ":" in p]
    except:
        return []

# ✅ تحميل من كل المصادر
def fetch_all_proxies():
    all_proxies = set()
    for url in PROXY_SOURCES:
        proxies = fetch_proxies_from_source(url)
        all_proxies.update(proxies)
    return list(all_proxies)

# ✅ اختبار بالتوازي
def validate_proxies_parallel(proxy_list, max_workers=50):
    valid_proxies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {executor.submit(is_proxy_working, proxy): proxy for proxy in proxy_list}
        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                if future.result():
                    valid_proxies.append(proxy)
            except:
                continue
    return valid_proxies

# ✅ جلب العدد المطلوب من البروكسيات الأوروبية
def get_required_proxies(required_count=50, max_attempts=10):
    all_valid = set()
    attempt = 0

    while len(all_valid) < required_count and attempt < max_attempts:
        print(f"🔄 Attempt {attempt + 1}: Fetching new proxies...")
        raw_proxies = fetch_all_proxies()
        random.shuffle(raw_proxies)
        valid = validate_proxies_parallel(raw_proxies)
        all_valid.update(valid)
        print(f"✅ Found {len(all_valid)} valid proxies so far.")
        attempt += 1
        time.sleep(2)

    if len(all_valid) >= required_count:
        print(f"🎯 Success! Got {required_count} proxies.")
    else:
        print(f"⚠️ Only got {len(all_valid)} proxies after {max_attempts} attempts.")

    return list(all_valid)[:required_count]
