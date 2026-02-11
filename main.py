import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_pure_nodes(url):
    """终极收割逻辑：全协议支持，极致兼容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code == 200:
            raw_data = r.text.strip()
            # 【核心修正】正则表达式进化：
            # 1. 加入 http/https/socks5/ssr/ss/vmess/vless/trojan/hy2/tuic 全协议支持
            # 2. 优化末尾匹配，确保带参数的超长链接不被截断
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"]+'
            
            # 1. 尝试直接从网页原文中提取
            found = re.findall(pattern, raw_data, re.I)
            
            # 2. 针对 Base64 深度挖掘
            try:
                # 剔除干扰，只留 Base64 核心字符
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
    print("🚀 [GOD-MODE] 正在执行全协议零损耗收割，对齐所有截图节点...")
    
    # 依然锁定你验证过的两条黄金源
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

    # 严格去重：保持最原始格式
    unique_nodes = []
    seen = set()
    for node in all_found:
        node_clean = node.strip()
        if node_clean and node_clean not in seen:
            unique_nodes.append(node_clean)
            seen.add(node_clean)
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [DONE] 搬运成功！总计捕获 {len(unique_nodes)} 个节点。")
            print(f"💡 老大，请去 Karing 刷新验证那个 66ms 的台湾节点！")
        else:
            print("❌ 警告：未发现有效节点。")

if __name__ == "__main__":
    collector()
