import random
import time
from proxy_manager import get_required_proxies, is_proxy_working
from agent import Agent

# ✅ تحديد عدد الـ Agents عشوائيًا بين 10 و15
agent_count = random.randint(10, 15)
print(f"🔢 Running {agent_count} agents...")

final_proxies = []
max_quick_attempts = 5
attempt = 0

# 🔄 محاولة جلب بروكسيات صالحة مع الفحص السريع وتعويض الفاشلة
while len(final_proxies) < agent_count and attempt < max_quick_attempts:
    needed = agent_count - len(final_proxies)
    print(f"\n🔄 Fetching {needed} proxies (Attempt {attempt + 1})...")
    
    new_proxies = get_required_proxies(required_count=needed)
    
    for proxy in new_proxies:
        print(f"⚡ Quick check for proxy: {proxy}")
        if is_proxy_working(proxy, timeout=5):
            final_proxies.append(proxy)
        else:
            print(f"❌ Proxy {proxy} failed quick check.")
    
    attempt += 1
    if len(final_proxies) < agent_count:
        print("♻️ Retrying to complete proxy list...")
        time.sleep(1)

# التأكد من وجود العدد الكافي من البروكسيات بعد الفحص السريع
if len(final_proxies) < agent_count:
    print(f"❌ Could only get {len(final_proxies)} working proxies after retries. Exiting.")
    exit()

# ✅ إنشاء وتشغيل كل Agent بتأخير عشوائي بين كل واحد
for i in range(agent_count):
    proxy = final_proxies[i]
    print(f"\n🚀 Starting Agent #{i+1} with proxy: {proxy}")
    
    try:
        agent = Agent(proxy)
        agent.run()
    except Exception as e:
        print(f"❌ Error in Agent #{i+1}: {e}")
    
    sleep_time = random.randint(60, 180)
    print(f"⏳ Sleeping {sleep_time} seconds before next agent...")
    time.sleep(sleep_time)

print("✅ All agents completed.")
