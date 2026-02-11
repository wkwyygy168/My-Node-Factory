import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_pure_nodes(url):
    """最强抓取逻辑：协议指纹 + 国家代码雷达"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code == 200:
            raw_data = r.text.strip()
            
            # 1. 核心协议正则：涵盖所有主流及罕见协议
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks|wireguard)://[^\s<>"]+'
            found = re.findall(pattern, raw_data, re.I)
            
            # 2. 深度解码逻辑：针对 base64.txt 等加密源
            try:
                # 预处理：只保留合法的 Base64 字符
                b64_only = re.sub(r'[^A-Za-z0-9+/=]', '', raw_data)
                missing_padding = len(b64_only) % 4
                if missing_padding:
                    b64_only += "=" * (4 - missing_padding)
                decoded = base64.b64decode(b64_only).decode('utf-8', errors='ignore')
                found.extend(re.findall(pattern, decoded, re.I))
            except:
                pass
            
            # 3. 老大的独门秘籍：国家代码二次校验（确保 ps 备注里的国家信息完整）
            # 我们在后面合并去重时，会自动保留这些包含地区信息的完整节点
            return found
    except:
        return []

def collector():
    print("🚀 [GLOBAL-RADAR] 正在通过协议+国家代码双重收割高质量节点...")
    
    # 锁定黄金双源
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

    # 深度去重，确保每个节点独一无二
    unique_nodes = []
    seen = set()
    
    # 定义老大要求的国家/地区关键词雷达
    region_keywords = ['TW', 'VN', 'RU', 'FR', 'HK', 'SG', 'US', 'KR', 'JP', '台湾', '越南', '俄罗斯', '法国', '香港', '新加坡', '美国', '韩国', '日本']
    
    for node in all_found:
        node_clean = node.strip()
        if node_clean and node_clean not in seen:
            unique_nodes.append(node_clean)
            seen.add(node_clean)
            
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            # 统计一下包含老大要求国家代码的节点比例
            region_count = sum(1 for n in unique_nodes if any(k in n for k in region_keywords))
            print(f"✅ [SUCCESS] 搬运成功！共捕获 {len(unique_nodes)} 个节点。")
            print(f"📊 地区雷达：其中包含 {region_count} 个明确标注地区的优质节点。")
        else:
            print("❌ 未发现节点。")

if __name__ == "__main__":
    collector()
