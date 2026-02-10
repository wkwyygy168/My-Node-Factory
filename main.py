import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_raw(url):
    """最强兼容抓取逻辑：不放过任何一个字符"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            content = r.text.strip()
            # 协议正则：只要符合协议格式就抓取
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
            
            # 1. 抓取明文
            nodes = re.findall(pattern, content, re.I)
            
            # 2. 深度处理 Base64（解决解码失败导致 0 节点的问题）
            try:
                # 自动补全填充符，这是解决“空文件”的关键
                padding = len(content) % 4
                if padding: content += "=" * (4 - padding)
                decoded = base64.b64decode(content).decode('utf-8', errors='ignore')
                nodes.extend(re.findall(pattern, decoded, re.I))
            except:
                pass
            return nodes
    except:
        return []

def collector():
    print("🛰️ [SYSTEM] 引擎全开：正在进行 80+ 源全量深度爆破...")
    
    # 这里保持你那 80 条 targets 不变（务必确保每一行末尾有逗号）
    targets = [
        # ... 这里放你那 80 条源 ...
    ]

    all_found = []
    # 增加线程数到 40，暴力突破
    with ThreadPoolExecutor(max_workers=40) as executor:
        results = executor.map(fetch_raw, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        # 如果节点数量大于 1，说明抓取成功，不再只输出保底
        if len(unique_nodes) > 1:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 爆破完成！成功收割节点: {len(unique_nodes)} 个")
        else:
            # 修改保底信息，帮助排查
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#警告_80条源均未吐出数据_请检查源链接")

if __name__ == "__main__":
    collector()
