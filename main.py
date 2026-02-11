import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_pure_nodes(url):
    """像搬运工一样，只负责把节点从网页里抠出来"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            raw_data = r.text.strip()
            # 协议识别正则：这是目前最兼容的写法
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
            
            # 1. 尝试直接提取（如果网页里已经是明文）
            found = re.findall(pattern, raw_data, re.I)
            
            # 2. 暴力解码 Base64（针对 base64.txt 这种纯密文）
            # 我们先尝试对整个网页内容进行 Base64 解码
            try:
                # 自动清理可能存在的换行符或空格
                clean_b64 = re.sub(r'\s+', '', raw_data)
                missing_padding = len(clean_b64) % 4
                if missing_padding:
                    clean_b64 += "=" * (4 - missing_padding)
                decoded = base64.b64decode(clean_b64).decode('utf-8', errors='ignore')
                found.extend(re.findall(pattern, decoded, re.I))
            except:
                pass
            return found
    except:
        return []

def collector():
    print("🚀 [PURE-MODE] 纯净搬运模式启动：目标 shuaidaoya 黄金源...")
    
    # 按照你的要求，只写这两条你验证过最猛的链接
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_found = []
    # 依然使用并行，速度极快
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_pure_nodes, targets)
        for res in results:
            if res:
                all_found.extend(res)

    # 深度去重（防止两条链接里有重复节点）
    unique_nodes = list(set(all_found))
    
    # 直接写入，不加后缀，不切备注，保持原汁原味
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if len(unique_nodes) > 0:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 搬运完毕！共计 {len(unique_nodes)} 个原始节点已入库。")
        else:
            print("❌ [FAILED] 没抓到节点，请检查 GitHub 网络连通性。")

if __name__ == "__main__":
    collector()
