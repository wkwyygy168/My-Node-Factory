import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_raw_nodes(url):
    """最原始的抓取：不改名、不准动任何一个字符"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200: return []
        
        raw_content = r.text.strip()
        # 协议提取正则：支持所有主流协议
        pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
        
        # 1. 直接提取明文节点
        found = re.findall(pattern, raw_content, re.I)
        
        # 2. 局部 Base64 解码提取（处理 YAML 中可能嵌套的 B64 块）
        try:
            # 自动清理非 B64 字符，尝试对整个网页进行解码扫描
            clean_b64 = re.sub(r'[^A-Za-z0-9+/=]', '', raw_content)
            missing = len(clean_b64) % 4
            if missing: clean_b64 += "=" * (4 - missing)
            decoded = base64.b64decode(clean_b64).decode('utf-8', errors='ignore')
            found.extend(re.findall(pattern, decoded, re.I))
        except:
            pass
        return found
    except:
        return []

def collector():
    print("🚀 [DEBUG-MODE] 正在测试单条链接收割能力...")
    
    # 按照老大要求：去掉了 base64.txt，仅保留 all.yaml 进行专项测试
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_found = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_raw_nodes, targets)
        for res in results:
            if res:
                all_found.extend(res)

    # 深度去重
    unique_nodes = []
    seen = set()
    for node in all_found:
        n = node.strip()
        if n and n not in seen:
            unique_nodes.append(n)
            seen.add(n)
    
    # 强制 UTF-8 写入
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [TEST-RESULT] 成功从 all.yaml 中捕获 {len(unique_nodes)} 个节点。")
        else:
            # 如果这里输出 0，就说明脚本目前的“://”提取逻辑无法处理 all.yaml 的结构
            print("❌ [TEST-RESULT] all.yaml 未能提取到任何节点！")

if __name__ == "__main__":
    collector()
