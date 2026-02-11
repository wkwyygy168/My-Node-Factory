import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_raw_nodes(url):
    """最原始的抓取：保住 base64.txt 完美兼容，同时强力穿透 all.yaml"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200: return []
        
        raw_content = r.text.strip()
        # 协议指纹正则
        pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
        
        # --- 1. 核心明文提取 (这是你验证过完全好用的 base64.txt 逻辑) ---
        found = re.findall(pattern, raw_content, re.I)
        
        # --- 2. 深度识别逻辑 (解决 all.yaml 这种混合格式) ---
        # 如果第一步没抓全，我们通过识别网页中的 Base64 块进行碎片化解码
        # 这样即便节点被包在 YAML 的字段引号里，也能被抠出来
        b64_blocks = re.findall(r'[A-Za-z0-9+/=]{64,}', raw_content)
        
        # 如果网页本身就是一段 Base64 (如 base64.txt)，我们也要保底处理
        if not found and not b64_blocks:
            b64_blocks = [re.sub(r'[^A-Za-z0-9+/=]', '', raw_content)]

        for block in b64_blocks:
            try:
                # 自动补全填充符
                missing = len(block) % 4
                if missing: block += "=" * (4 - missing)
                decoded = base64.b64decode(block).decode('utf-8', errors='ignore')
                # 在解码后的内容里二次搜索 :// 节点
                found.extend(re.findall(pattern, decoded, re.I))
            except:
                continue
                
        return found
    except:
        return []

def collector():
    print("🚀 [TRUE-ORIGIN] 正在收割：保住 base64.txt 胜货，强力解析 all.yaml...")
    
    # 按照你的要求，目标锁定在 all.yaml。
    # 跑通后，请自行将 base64.txt 链接加回此处进行合并。
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_found = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_raw_nodes, targets)
        for res in results:
            if res:
                all_found.extend(res)

    # 深度去重：保留最原始的字符，不做任何改动
    unique_nodes = []
    seen = set()
    for node in all_found:
        n = node.strip()
        if n and n not in seen:
            unique_nodes.append(n)
            seen.add(n)
    
    # 以 UTF-8 编码写入 nodes.txt
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 任务成功！共收集到 {len(unique_nodes)} 个节点。")
        else:
            print("❌ [FAILED] all.yaml 依然无法识别，建议检查源文件格式。")

if __name__ == "__main__":
    collector()
