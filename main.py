import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def stream_extractor(url):
    """模仿客户端内核的流式扫描，确保 100% 还原每一个字节"""
    headers = {'User-Agent': 'clash.meta'}
    try:
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code != 200: return []
        
        raw_text = r.text
        # 第一步：收集所有可能的协议头位置
        # 不再用死板的正则，而是先定位 ://
        protocols = ["vmess://", "vless://", "ss://", "ssr://", "trojan://", "hy2://", "tuic://", "http://", "https://", "socks5://", "socks://"]
        nodes = []

        # 第二步：明文暴力扫描 (针对 YAML)
        # 扫描逻辑：找到协议头，向后提取，直到遇到引号、空格或非法字符
        for proto in protocols:
            start_idx = 0
            while True:
                start_idx = raw_text.find(proto, start_idx)
                if start_idx == -1: break
                
                # 提取逻辑：尽可能向后抓取，直到遇到明显的分界符
                end_match = re.search(r'[\s"\'<>\{\}\]\[]', raw_text[start_idx:])
                if end_match:
                    node = raw_text[start_idx : start_idx + end_match.start()]
                else:
                    node = raw_text[start_idx:]
                
                nodes.append(node.strip())
                start_idx += len(proto)

        # 第三步：Base64 碎片化提取 (针对 base64.txt)
        # 不再解整个页面，而是提取页面中所有可能的 Base64 块进行尝试
        b64_blocks = re.findall(r'[A-Za-z0-9+/=]{40,}', raw_text)
        for block in b64_blocks:
            try:
                # 尝试补齐并解码
                pad = len(block) % 4
                if pad: block += "=" * (4 - pad)
                decoded = base64.b64decode(block).decode('utf-8', errors='ignore')
                # 在解码后的内容里重复上述协议头扫描
                for proto in protocols:
                    s_idx = 0
                    while True:
                        s_idx = decoded.find(proto, s_idx)
                        if s_idx == -1: break
                        e_match = re.search(r'[\s"\'<>\{\}\]\[]', decoded[s_idx:])
                        node = decoded[s_idx : s_idx + e_match.start()] if e_match else decoded[s_idx:]
                        nodes.append(node.strip())
                        s_idx += len(proto)
            except:
                continue
                
        return nodes
    except:
        return []

def collector():
    print("🚀 [GHOST-SCAN] 正在执行全量流式扫描，找回失踪的极品节点...")
    
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(stream_extractor, targets)
        for res in results:
            if res: all_results.extend(res)

    # 深度去重：保留最原始的数据特征
    unique_nodes = []
    seen = set()
    for node in all_results:
        # 清除末尾可能的脏字符（如逗号、括号）
        clean_node = re.split(r'[,;\}]', node)[0]
        if clean_node and clean_node not in seen:
            unique_nodes.append(clean_node)
            seen.add(clean_node)
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [DONE] 最终收集到 {len(unique_nodes)} 个节点。")
        else:
            print("❌ 警告：未发现有效节点。")

if __name__ == "__main__":
    collector()
