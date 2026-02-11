import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_raw_nodes(url):
    """
    终极识别逻辑：
    1. 保持对 base64.txt 的 100% 完美提取（你验证过好用的逻辑）。
    2. 引入‘订阅转换隧道’，强行把 all.yaml 这种硬骨头‘翻译’成 Karing 能认的链接。
    """
    # 模拟真实浏览器
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # --- 逻辑 A: 你的‘保命’逻辑 (针对 base64.txt 这种明文或纯 B64 订阅) ---
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            raw_text = r.text.strip()
            # 协议识别指纹
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
            
            # 尝试直接抓取明文
            found = re.findall(pattern, raw_text, re.I)
            
            # 尝试整体解密 (base64.txt 逻辑)
            try:
                clean_b64 = re.sub(r'[^A-Za-z0-9+/=]', '', raw_text)
                missing = len(clean_b64) % 4
                if missing: clean_b64 += "=" * (4 - missing)
                decoded = base64.b64decode(clean_b64).decode('utf-8', errors='ignore')
                found.extend(re.findall(pattern, decoded, re.I))
            except: pass
            
            # 如果上面抓到了东西，直接返回 (比如 base64.txt 场景)
            if len(found) > 10: return found

        # --- 逻辑 B: 强制转换逻辑 (针对 all.yaml 这种没有 :// 的硬骨头) ---
        # 如果是 YAML 格式，我们借用‘翻译官’(在线后端) 把配置转成标准链接
        # 这也是全网处理这类文件的通用标准方案
        convert_api = f"https://api.v1.mk/sub?target=v2ray&url={url}&insert=false"
        res = requests.get(convert_api, timeout=20)
        if res.status_code == 200:
            # 转换后的内容通常是 Base64 加密的链接列表
            decoded_api = base64.b64decode(res.text).decode('utf-8', errors='ignore')
            # 再次使用正则提取出 :// 节点
            return re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+', decoded_api, re.I)
            
    except: pass
    return []

def collector():
    print("🚀 [GOD-LEVEL] 正在执行全协议兼容收割，力保 all.yaml 不再‘失踪’...")
    
    # 把两个黄金链接都放进去，脚本会自动识别并采用不同逻辑处理
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_found = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_raw_nodes, targets)
        for res in results:
            if res: all_found.extend(res)

    # 严格去重：保留最原始字符
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
            print(f"✅ [DONE] 任务大获全胜！共捕获 {len(unique_nodes)} 个原始节点。")
        else:
            print("❌ 警告：依然未能发现有效节点。")

if __name__ == "__main__":
    collector()
