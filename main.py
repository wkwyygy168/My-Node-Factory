import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def recursive_decode(text, depth=0):
    """像剥洋葱一样深度解码，解决只有1个节点的问题"""
    if depth > 5: return text # 防止死循环
    pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
    # 尝试清洗并解码
    try:
        clean_text = re.sub(r'[^a-zA-Z0-9+/=]', '', text)
        if len(clean_text) % 4: clean_text += "=" * (4 - len(clean_text) % 4)
        decoded = base64.b64decode(clean_text).decode('utf-8', errors='ignore')
        if any(p in decoded for p in ['://']):
            return recursive_decode(decoded, depth + 1)
    except: pass
    return text

def fetch_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    # 增加镜像备选路径
    alt_url = url.replace("raw.githubusercontent.com", "fastly.jsdelivr.net/gh").replace("/master/", "@master/").replace("/main/", "@main/") if "raw.githubusercontent.com" in url else url
    
    for target in [alt_url, url]:
        try:
            r = requests.get(target, headers=headers, timeout=15)
            if r.status_code == 200 and len(r.text) > 10:
                raw = r.text
                # 递归提取所有隐藏节点
                decoded_content = recursive_decode(raw)
                pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
                # 同时从原文和解密文中抓取
                return re.findall(pattern, raw + "\n" + decoded_content, re.I)
        except: continue
    return []

def collector():
    print("🚀 [SYSTEM] 引擎 V12.0：启动递归爆破模式...")
    # 这里的 targets 保持你那 80 条列表不变即可
    targets = [ "...你的80条链接..." ] 

    all_found = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(fetch_content, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if len(unique_nodes) > 1:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 爆破成功！捕获有效节点: {len(unique_nodes)} 个")
        else:
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#云端收割机正在全力作业_请稍后刷新")

if __name__ == "__main__":
    collector()
