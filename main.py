import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_pure_nodes(url):
    """像吸尘器一样，只吸取最原始的协议链接，绝不改动任何字符"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            raw_data = r.text.strip()
            # 强化版正则：确保完整捕获从协议头到末尾的所有参数
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
            
            # 1. 尝试直接从网页原文中吸取 (针对 all.yaml)
            found = re.findall(pattern, raw_data, re.I)
            
            # 2. 针对 Base64 链接的特殊处理 (针对 base64.txt)
            # 重点：不再尝试整体解码，而是先清洗掉所有非 Base64 干扰字符
            try:
                # 只保留 Base64 字符，剔除换行、空格等所有干扰
                b64_only = re.sub(r'[^A-Za-z0-9+/=]', '', raw_data)
                missing_padding = len(b64_only) % 4
                if missing_padding:
                    b64_only += "=" * (4 - missing_padding)
                decoded = base64.b64decode(b64_only).decode('utf-8', errors='ignore')
                found.extend(re.findall(pattern, decoded, re.I))
            except:
                pass
            return found
    except:
        return []

def collector():
    print("🚀 [CRITICAL-FIX] 正在执行零损耗搬运逻辑，全力追回高质量节点...")
    
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_found = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_pure_nodes, targets)
        for res in results:
            if res:
                all_found.extend(res)

    # 深度去重：保留最原始的字符
    unique_nodes = []
    seen = set()
    for node in all_found:
        node_clean = node.strip()
        if node_clean not in seen:
            unique_nodes.append(node_clean)
            seen.add(node_clean)
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            # 使用换行符连接，确保每个节点独立一行
            f.write("\n".join(unique_nodes))
            print(f"✅ [DONE] 搬运成功！总计捕获 {len(unique_nodes)} 个百分百原始节点。")
        else:
            print("❌ 警告：未发现有效节点。")

if __name__ == "__main__":
    collector()
