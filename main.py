import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_raw_nodes(url):
    """最原始的抓取：100%保住 base64.txt 逻辑，同时攻克 all.yaml 这种散装格式"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200: return []
        
        raw_content = r.text.strip()
        # 协议提取正则 (这是你验证过完全好用的 base64.txt 逻辑)
        pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
        
        # --- 1. 明文提取 (base64.txt 专用) ---
        found = re.findall(pattern, raw_content, re.I)
        
        # --- 2. 整体解码提取 (base64.txt 专用) ---
        try:
            clean_b64 = re.sub(r'[^A-Za-z0-9+/=]', '', raw_content)
            missing = len(clean_b64) % 4
            if missing: clean_b64 += "=" * (4 - missing)
            decoded = base64.b64decode(clean_b64).decode('utf-8', errors='ignore')
            found.extend(re.findall(pattern, decoded, re.I))
        except: pass

        # --- 3. 针对 all.yaml 的散装参数提取 (如果上面两招都落空) ---
        # 如果发现 proxies 关键字，说明是 Clash 格式，直接利用成熟的 API 转换
        if not found and ("proxies:" in raw_content or "server:" in raw_content):
            # 这种方法不改动你的本地逻辑，而是把“翻译”工作交给更专业的订阅转换后端
            # 出来的直接就是 Karing 能认的 :// 节点
            convert_url = f"https://sub.id9.cc/sub?target=v2ray&url={url}"
            try:
                res = requests.get(convert_url, timeout=15)
                if res.status_code == 200:
                    decoded_nodes = base64.b64decode(res.text).decode('utf-8', errors='ignore')
                    found.extend(re.findall(pattern, decoded_nodes, re.I))
            except: pass

        return found
    except:
        return []

def collector():
    print("🚀 [TRUE-ORIGIN] 正在收割：保住 base64.txt，强攻 all.yaml...")
    
    # 你目前想单测 all.yaml，请保持这里只有一条
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_found = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_raw_nodes, targets)
        for res in results:
            if res:
                all_found.extend(res)

    # 深度去重：保留最原始字符
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
            print(f"✅ [SUCCESS] 任务成功！共收集到 {len(unique_nodes)} 个节点。")
        else:
            print("❌ [FAILED] all.yaml 依然无法识别，请考虑源文件内容是否包含有效节点。")

if __name__ == "__main__":
    collector()
