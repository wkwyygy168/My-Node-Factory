import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_raw_nodes(url):
    """最原始抓取：保住 base64.txt 的完美兼容，同时强攻 all.yaml"""
    headers = {'User-Agent': 'clash.meta'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200: return []
        
        raw_content = r.text.strip()
        # --- 1. 这是你要求的‘绝对不动’的原始逻辑 (针对 base64.txt) ---
        pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
        found = re.findall(pattern, raw_content, re.I)
        
        try:
            clean_b64 = re.sub(r'[^A-Za-z0-9+/=]', '', raw_content)
            missing = len(clean_b64) % 4
            if missing: clean_b64 += "=" * (4 - missing)
            decoded = base64.b64decode(clean_b64).decode('utf-8', errors='ignore')
            found.extend(re.findall(pattern, decoded, re.I))
        except: pass
        
        # --- 2. 专门针对 all.yaml 的‘强行抓取’逻辑 (如果不改动上面，必须加这一段) ---
        # 如果是 YAML 格式，里面没有 ://，我们要把这些参数拼凑起来
        if "proxies:" in raw_content or "server:" in raw_content:
            # 这种方法不改动原有 pattern，而是利用订阅转换的原理，
            # 直接把 YAML 链接交给后端处理，确保出来的就是 Karing 能认的 :// 格式
            convert_url = f"https://sub.id9.cc/sub?target=v2ray&url={url}"
            try:
                res = requests.get(convert_url, timeout=15)
                if res.status_code == 200:
                    converted_decoded = base64.b64decode(res.text).decode('utf-8', errors='ignore')
                    found.extend(re.findall(pattern, converted_decoded, re.I))
            except: pass

        return found
    except:
        return []

def collector():
    print("🚀 [TRUE-ORIGIN] 保持 base64.txt 兼容性，强化 all.yaml 提取...")
    
    # 这里你可以根据测试需求，放一条或两条
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_found = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_raw_nodes, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = []
    seen = set()
    for node in all_found:
        n = node.strip()
        if n and n not in seen:
            unique_nodes.append(n)
            seen.add(n)
    
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 提取成功！共捕获 {len(unique_nodes)} 个节点。")
        else:
            print("❌ [FAILED] all.yaml 依然无法直接提取明文节点。")

if __name__ == "__main__":
    collector()
