import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_raw_nodes(url):
    """最原始的抓取：保住 base64.txt 的完美兼容，同时强力穿透 all.yaml"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200: return []
        
        raw_content = r.text.strip()
        # 协议指纹正则
        pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
        
        # --- 1. 核心明文提取 (这是你验证过完全好用的 base64.txt 逻辑) ---
        found = re.findall(pattern, raw_content, re.I)
        
        # --- 2. 深度穿透逻辑 (针对 base64.txt 的解密以及 all.yaml 的嵌套识别) ---
        try:
            # 无论网页长什么样，我们提取所有看起来像 Base64 的字符块进行碎片化解码
            # 这样即便是 YAML 里的 Base64 片段也能被抠出来
            b64_blocks = re.findall(r'[A-Za-z0-9+/=]{64,}', raw_content)
            if not b64_blocks: # 如果没找到长块，尝试对整个网页进行保底清洗解码
                b64_blocks = [re.sub(r'[^A-Za-z0-9+/=]', '', raw_content)]
            
            for block in b64_blocks:
                try:
                    missing = len(block) % 4
                    if missing: block += "=" * (4 - missing)
                    decoded = base64.b64decode(block).decode('utf-8', errors='ignore')
                    found.extend(re.findall(pattern, decoded, re.I))
                except: continue
        except: pass
        
        return found
    except: return []

def collector():
    print("🚀 [TRUE-ORIGIN] 正在执行全量收割，保住 base64.txt 胜果，收复 all.yaml...")
    
    # 按照你的要求，目标锁定在 all.yaml，同时请自行在运行成功后把 base64.txt 加回此处
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_found = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_raw_nodes, targets)
        for res in results:
            if res: all_found.extend(res)

    # 深度去重：保留最原始字符
    unique_nodes = []
    seen = set()
    for node in all_found:
        n = node.strip()
        if n and n not in seen:
            unique_nodes.append(n)
            seen.add(n)
    
    # 写入文件
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 任务成功！共收集到 {len(unique_nodes)} 个节点。")
        else:
            print("❌ [FAILED] 依然未能从 all.yaml 中识别出节点，请确认该文件是否包含标准节点。")

if __name__ == "__main__":
    collector()
