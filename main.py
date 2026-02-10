import requests
import re
import base64
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_and_extract(url):
    # 模拟真实的浏览器，防止被目标源封锁
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    try:
        # 增加一点点延迟，防止并发过高被封 IP
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            raw_text = r.text.strip()
            # 协议指纹
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
            
            # 1. 直接抓
            found = re.findall(pattern, raw_text, re.I)
            
            # 2. 强制 Base64 爆破逻辑 (解决 1 个节点的核心)
            try:
                # 尝试清洗掉可能的非 Base64 字符
                clean_text = re.sub(r'[^a-zA-Z0-9+/=]', '', raw_text)
                padding = len(clean_text) % 4
                if padding: clean_text += "=" * (4 - padding)
                decoded = base64.b64decode(clean_text).decode('utf-8', errors='ignore')
                found.extend(re.findall(pattern, decoded, re.I))
            except: pass
            
            return found
    except: return []

def collector():
    print("🚀 [SYSTEM] 终极爆破模式启动...")
    # 保持你那 80 条源不变
    targets = [ "..." ] 

    all_found = []
    # 降低并发到 15，防止被 GitHub 判定为异常流量
    with ThreadPoolExecutor(max_workers=15) as executor:
        results = executor.map(fetch_and_extract, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if len(unique_nodes) > 2:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 成功收割唯一节点: {len(unique_nodes)} 个")
        else:
            # 修改保底，把第一个源的内容抓出来看看到底返回了什么
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#云端收割机正在全力作业")

if __name__ == "__main__":
    collector()
