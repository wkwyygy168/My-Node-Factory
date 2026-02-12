import requests
import re

def fetch_all_yaml_nodes(url):
    """
    原力提取逻辑：抛弃一切复杂的解码逻辑，
    直接在原始网页文本中扫描所有协议链接，一个都不能少。
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/plain'
    }
    try:
        # 获取网页原始文本
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200: return []
        
        raw_text = r.text
        
        # 1. 第一步：全协议正则（贪婪模式）
        # 允许包含所有非空白、非引号字符，确保长参数（如 sni, fp, 平方2）不被截断
        pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
        
        # 直接在原文里抓
        found_nodes = re.findall(pattern, raw_text, re.I)
        
        # 2. 第二步：如果抓到的不够多，说明剩下的藏在 Base64 里
        # 我们不再整体解，而是“分段”提取 Base64 进行尝试
        if len(found_nodes) < 50:
            # 找到文本中所有看起来像 Base64 的超长字符串块
            import base64
            potential_blocks = re.findall(r'[A-Za-z0-9+/=]{100,}', raw_text)
            for block in potential_blocks:
                try:
                    # 补齐位，尝试解码
                    missing = len(block) % 4
                    if missing: block += "=" * (4 - missing)
                    decoded = base64.b64decode(block).decode('utf-8', errors='ignore')
                    found_nodes.extend(re.findall(pattern, decoded, re.I))
                except: continue
                
        return found_nodes
    except Exception as e:
        print(f"❌ 运行报错: {e}")
        return []

def collector():
    print("🚀 [TRUE-FORCE] 正在执行全量暴力抓取，目标对齐 92 条节点...")
    
    # 精准锁定你最后确认的这条链接
    target = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    
    nodes = fetch_all_yaml_nodes(target)
    
    # 严格去重并保持原始顺序
    unique_nodes = []
    seen = set()
    for n in nodes:
        node_clean = n.strip()
        if node_clean and node_clean not in seen:
            unique_nodes.append(node_clean)
            seen.add(node_clean)
            
    # 写入文件
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 任务完成！")
            print(f"📊 最终结果：nodes.txt 已更新，总计捕获 {len(unique_nodes)} 个节点。")
        else:
            print("❌ 警告：未发现任何有效节点。")

if __name__ == "__main__":
    collector()
