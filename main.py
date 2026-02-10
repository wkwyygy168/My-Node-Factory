import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_content(url):
    # 自动转换 GitHub 链接为镜像链接，防止被拦截
    if "raw.githubusercontent.com" in url:
        url = url.replace("raw.githubusercontent.com", "fastly.jsdelivr.net/gh").replace("/master/", "@master/").replace("/main/", "@main/")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            content = r.text.strip()
            # 协议指纹
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
            
            # 1. 直接提取明文
            nodes = re.findall(pattern, content, re.I)
            
            # 2. 暴力 Base64 解码逻辑
            try:
                # 补全填充符并清洗非法字符
                b64_str = re.sub(r'[^a-zA-Z0-9+/=]', '', content)
                padding = len(b64_str) % 4
                if padding: b64_str += "=" * (4 - padding)
                decoded = base64.b64decode(b64_str).decode('utf-8', errors='ignore')
                nodes.extend(re.findall(pattern, decoded, re.I))
            except: pass
            
            return nodes
    except: return []

def collector():
    print("🚀 [SYSTEM] 引擎 V10.0：正在通过 CDN 镜像进行全量爆破...")
    
    # 这里的 targets 建议先用你最信任的 10 个试试，如果通了再加到 80 个
    targets = [
        "https://raw.githubusercontent.com/freefq/free/master/v2ray",
        "https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt",
        "https://raw.githubusercontent.com/Pawpieee/Free-Proxies/main/sub/sub_merge.txt",
        "https://raw.githubusercontent.com/anaer/Sub/master/v2ray.txt"
        # ... (此处保持你原本的 80 条列表即可)
    ]

    all_found = []
    # 降低并发到 10，细水长流防止被封
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_content, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if len(unique_nodes) > 1:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 爆破完成！成功收割节点: {len(unique_nodes)} 个")
        else:
            # 修改保底信息，确保不让 Karing 报空
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#云端收割机正在全力作业_请稍后刷新")

if __name__ == "__main__":
    collector()
