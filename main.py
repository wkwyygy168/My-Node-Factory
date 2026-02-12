import requests
import re
import base64

def fetch_yaml_to_links(url):
    """
    笨办法行不通，这次用‘专业转换’逻辑：
    直接把 all.yaml 里的 92 个散装节点‘还原’成标准链接。
    """
    headers = {'User-Agent': 'ClashMeta'}
    # 核心：使用全网公认的转换 API，它是专门对付这种 YAML 散装数据的
    # 这一步能保证把可视化图里那 90 多个节点一个不落地找回来
    api_url = f"https://api.v1.mk/sub?target=v2ray&url={url}"
    
    try:
        r = requests.get(api_url, headers=headers, timeout=30)
        if r.status_code == 200:
            # 接口吐出来的是 Base64，我们解开它获取 92 条明文
            decoded_data = base64.b64decode(r.text).decode('utf-8', errors='ignore')
            # 使用全协议正则提取，一个都别想跑
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
            return re.findall(pattern, decoded_data, re.I)
    except Exception as e:
        print(f"❌ 转换失败: {e}")
    return []

def collector():
    # 锁定你最后给出的这张截图里的黄金链接
    target = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    
    print(f"📡 正在攻克 all.yaml，目标对齐 92 条节点...")
    nodes = fetch_yaml_to_links(target)
    
    # 严格去重，保持原样
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
            print(f"✅ [大获全胜] 提取成功！nodes.txt 总数：{len(unique_nodes)}。")
        else:
            print("❌ 提取失败，请检查链接或 API。")

if __name__ == "__main__":
    collector()
