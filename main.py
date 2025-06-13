import random
import time
from proxy_manager import get_required_proxies
from agent import Agent

# ✅ تحديد عدد الـ Agents عشوائيًا بين 10 و15
agent_count = random.randint(10, 15)
print(f"🔢 Running {agent_count} agents...")

# ✅ جلب بروكسيات أوروبية مختلفة وصالحة
proxies = get_required_proxies(required_count=agent_count)
if len(proxies) < agent_count:
    print("⚠️ Not enough proxies. Exiting.")
    exit()

# ✅ إنشاء وتشغيل كل Agent بتأخير عشوائي بين كل واحد
for i in range(agent_count):
    proxy = proxies[i]
    print(f"\n🚀 Starting Agent #{i+1} with proxy: {proxy}")
    
    try:
        agent = Agent(proxy)
        agent.run()
    except Exception as e:
        print(f"❌ Error in Agent #{i+1}: {e}")
    
    # ✅ تأخير عشوائي بين 1-3 دقائق لتجنب الحظر أو كشف الأنماط
    sleep_time = random.randint(60, 180)
    print(f"⏳ Sleeping {sleep_time} seconds before next agent...")
    time.sleep(sleep_time)

print("✅ All agents completed.")
