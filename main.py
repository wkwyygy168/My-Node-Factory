import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_content(url):
    # 更加稳健的镜像转换，防止脚本因 URL 错误而打叉
    alt_url = url
    if "raw.githubusercontent.com" in url:
        try:
            # 兼容多种分支命名的转换逻辑
            parts = url.split('/')
            if len(parts) >= 5:
                user, repo = parts[3], parts[4]
                path = "/".join(parts[6:])
                branch = parts[5]
                alt_url = f"https://fastly.jsdelivr.net/gh/{user}/{repo}@{branch}/{path}"
        except: alt_url = url # 转换失败则用原链接

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 尝试双路径抓取：先镜像，后原始
    for target_url in [alt_url, url]:
        try:
            r = requests.get(target_url, headers=headers, timeout=12)
            if r.status_code == 200 and len(r.text) > 50:
                content = r.text.strip()
                pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
                
                # 1. 明文匹配
                nodes = re.findall(pattern, content, re.I)
                
                # 2. 暴力解码 (解决 1 个节点的核心)
                try:
                    b64_str = re.sub(r'[^a-zA-Z0-9+/=]', '', content)
                    missing_padding = len(b64_str) % 4
                    if missing_padding: b64_str += "=" * (4 - missing_padding)
                    decoded = base64.b64decode(b64_str).decode('utf-8', errors='ignore')
                    nodes.extend(re.findall(pattern, decoded, re.I))
                except: pass
                
                if nodes: return nodes
        except: continue
    return []

def collector():
    print("🚀 [SYSTEM] 引擎 V10.1：启动镜像+原始双路径爆破模式...")
    # 这里放你那 80 条源
    targets = [ "这里是你的80条链接列表..." ] 

    all_found = []
    # 保持中速并发，确保稳定性
    with ThreadPoolExecutor(max_workers=15) as executor:
        results = executor.map(fetch_content, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if len(unique_nodes) > 2:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 成功收割唯一节点: {len(unique_nodes)} 个")
        else:
            # 哪怕只有保底，也绝不让文件为空导致 Karing 报错
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#引擎双路尝试中_稍后刷新")

if __name__ == "__main__":
    collector()
