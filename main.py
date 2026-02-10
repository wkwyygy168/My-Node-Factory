import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def deep_decode(text):
    """极致递归解码：解决只有1个节点的问题"""
    current = text.strip()
    # 协议指纹识别
    pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
    all_nodes = re.findall(pattern, current, re.I)
    
    # 尝试深度解密 3 层
    for _ in range(3):
        try:
            # 清洗非法字符并补齐填充符
            b64_str = re.sub(r'[^a-zA-Z0-9+/=]', '', current)
            missing_padding = len(b64_str) % 4
            if missing_padding: b64_str += "=" * (4 - missing_padding)
            
            decoded = base64.b64decode(b64_str).decode('utf-8', errors='ignore')
            new_nodes = re.findall(pattern, decoded, re.I)
            if new_nodes:
                all_nodes.extend(new_nodes)
                current = decoded # 继续对解开的内容深度扫描
            else:
                break
        except: break
    return all_nodes

def fetch_content(url):
    # 自动转换 GitHub 链接为 jsDelivr 镜像，绕过云端封锁
    target = url
    if "raw.githubusercontent.com" in url:
        target = url.replace("raw.githubusercontent.com", "fastly.jsdelivr.net/gh").replace("/master/", "@master/").replace("/main/", "@main/")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(target, headers=headers, timeout=15)
        if r.status_code == 200:
            return deep_decode(r.text)
    except: pass
    return []

def collector():
    print("🚀 [SYSTEM] 引擎 V13.0：全量递归爆破模式启动...")
    # 这里保持你那 80 条源列表不变
    targets = [ "你的80条链接..." ] 

    all_found = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(fetch_content, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if len(unique_nodes) > 1:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 爆破完成！捕获节点: {len(unique_nodes)} 个")
        else:
            # 修改保底信息，明确标注是抓不到源
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#云端源失效_请更换80个源链接")

if __name__ == "__main__":
    collector()
