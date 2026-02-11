import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_pure_nodes(url):
    """最强搬运逻辑：支持上标、下标及所有特殊编码字符"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code == 200:
            raw_data = r.text.strip()
            # 【核心进化】正则表达式：
            # 1. 允许协议头包含特殊字体
            # 2. 匹配范围扩大到非空字符集，确保不被上标“2”等特殊符号截断
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks|wireguard)://[^\s<>"]+'
            
            # 直接提取原始明文
            found = re.findall(pattern, raw_data, re.I)
            
            # 针对 Base64 的深度清洗提取
            try:
                # 只保留 Base64 合法字符用于解码
                b64_only = re.sub(r'[^A-Za-z0-9+/=]', '', raw_data)
                missing_padding = len(b64_only) % 4
                if missing_padding:
                    b64_only += "=" * (4 - missing_padding)
                decoded = base64.b64decode(b64_only).decode('utf-8', errors='ignore')
                # 在解码后的内容里再次进行全量扫描
                found.extend(re.findall(pattern, decoded, re.I))
            except:
                pass
            return found
    except:
        return []

def collector():
    print("🚀 [ULTIMATE-RADAR] 正在通过‘全字符识别’找回失踪的台湾节点...")
    
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

    # 深度去重：保留最原始的编码，不进行任何字符转换
    unique_nodes = []
    seen = set()
    for node in all_found:
        # 使用 strip() 清除可能存在的换行干扰，但保留协议内的所有特殊符号
        node_clean = node.strip()
        if node_clean and node_clean not in seen:
            unique_nodes.append(node_clean)
            seen.add(node_clean)
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            # 关键：以 UTF-8 编码写入，确保 $TW^2$ 等特殊符号不乱码
            f.write("\n".join(unique_nodes))
            print(f"✅ [DONE] 搬运成功！当前共计：{len(unique_nodes)} 个节点。")
            print(f"📊 提示：已针对上标字符（如 TW^2）完成编码优化。")
        else:
            print("❌ 未发现节点。")

if __name__ == "__main__":
    collector()
