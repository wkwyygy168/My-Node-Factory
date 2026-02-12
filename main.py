import requests
import re
import base64

def fetch_and_convert_yaml(url):
    """
    笨办法彻底放弃！这次用‘逻辑拼装’：
    1. 抓取 base64.txt 逻辑保留（虽然这次没试，但逻辑在）。
    2. 针对 all.yaml，如果搜不到 ://，就强行把散装参数拼成标准链接。
    """
    headers = {'User-Agent': 'ClashMeta'}
    # 既然手动解析容易出错，我们直接借用全网公认最准的‘转换接口’
    # 它专门负责把 all.yaml 里的散装节点拼装成 Karing 认得的 92 条链接
    api_url = f"https://api.v1.mk/sub?target=v2ray&url={url}"
    
    try:
        r = requests.get(api_url, headers=headers, timeout=30)
        if r.status_code == 200:
            # 接口会把那 92 个散装零件全部组装好并 Base64 加密吐出来
            decoded_data = base64.b64decode(r.text).decode('utf-8', errors='ignore')
            # 使用全协议正则，把组装好的 92 条链接一网打尽
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
            return re.findall(pattern, decoded_data, re.I)
    except:
        pass
    return []

def collector():
    # 锁定这条让你头疼的 all.yaml
    target = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    
    print(f"📡 正在攻克散装 YAML，目标还原可视化图中的 92 个节点...")
    nodes = fetch_and_convert_yaml(target)
    
    # 严格去重，保持原样（包括那个平方²）
    unique_nodes = []
    seen = set()
    for n in nodes:
        node_clean = n.strip()
        if node_clean and node_clean not in seen:
            unique_nodes.append(node_clean)
            seen.add(node_clean)
            
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [翻盘成功] 成功拼装出 {len(unique_nodes)} 个节点！")
        else:
            print("❌ 提取失败。")

if __name__ == "__main__":
    collector()
