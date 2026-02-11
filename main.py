import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def universal_extractor(url):
    """像吸尘器一样，无视格式，只吸取有效的节点指纹"""
    headers = {'User-Agent': 'clash.meta'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200: return []
        
        raw_text = r.text
        # 第一步：暴力提取所有可见的节点链接
        # 允许包含所有非空白字符，直到遇到引号、尖括号或空格结束，确保不截断参数
        pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\']+'
        found = re.findall(pattern, raw_text, re.I)
        
        # 第二步：对全文进行“断点式”Base64 尝试
        # 很多 YAML 会把 Base64 节点包在特定字段里，我们直接扫描全文本中可能的 B64 块
        b64_blocks = re.findall(r'[A-Za-z0-9+/]{40,}', raw_text)
        for block in b64_blocks:
            try:
                # 补全填充并尝试解码
                missing_padding = len(block) % 4
                if missing_padding: block += "=" * (4 - missing_padding)
                decoded = base64.b64decode(block).decode('utf-8', errors='ignore')
                found.extend(re.findall(pattern, decoded, re.I))
            except:
                continue
        return found
    except:
        return []

def collector():
    print("🚀 [GOD-COLLECTOR] 正在执行全网最强暴力收割，目标 92+ 节点...")
    
    # 锁定你的核心黄金源
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_raw_found = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(universal_extractor, targets)
        for res in results:
            if res: all_raw_found.extend(res)

    # 重点：去重时必须保留原始编码，防止 TW² 等特殊符号被破坏
    unique_nodes = []
    seen = set()
    for node in all_raw_found:
        # 去掉末尾可能被误抓的标点符号
        clean_node = node.strip().rstrip(',').rstrip(';').rstrip('}')
        if clean_node and clean_node not in seen:
            unique_nodes.append(clean_node)
            seen.add(clean_node)
    
    # 按照你的需求，合并并输出到 nodes.txt
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 任务完成！共计准确收集 {len(unique_nodes)} 个节点。")
        else:
            print("❌ 警告：未发现有效节点。")

if __name__ == "__main__":
    collector()
