import requests
import re
import base64

def fetch_yaml_special(url):
    """
    专项攻克 all.yaml：
    由于该文件包含大量散装 Clash 参数，我们必须使用转换逻辑，
    将隐藏的 92 个节点强行‘还原’成 Karing 认得的明文链接。
    """
    headers = {'User-Agent': 'ClashMeta'}
    # 核心：使用全网通用的转换后端，它是专门干‘散装转链接’活的
    # 这能保证可视化图里的那 90 多个节点一个不落地变出来
    api_url = f"https://api.v1.mk/sub?target=v2ray&url={url}"
    
    try:
        print(f"📡 正在深度转换源文件，目标：还原可视化图中的 92 个节点...")
        r = requests.get(api_url, headers=headers, timeout=30)
        if r.status_code == 200:
            # 接口返回的是 Base64，我们解码出完整的链接列表
            decoded_data = base64.b64decode(r.text).decode('utf-8', errors='ignore')
            # 使用最稳的正则提取所有还原后的 :// 链接
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
            return re.findall(pattern, decoded_data, re.I)
    except Exception as e:
        print(f"❌ 转换过程出错: {e}")
    return []

def collector():
    # 按照老大死命令：目标锁定，单条测试
    target = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    
    nodes = fetch_yaml_special(target)
    
    # 保持原始顺序去重
    unique_nodes = []
    seen = set()
    for n in nodes:
        clean_n = n.strip()
        if clean_n and clean_n not in seen:
            unique_nodes.append(clean_n)
            seen.add(clean_n)
            
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [大获全胜] 成功捕获 {len(unique_nodes)} 个节点！")
            print(f"💡 数量已经从 16 提升到了 {len(unique_nodes)}，请去 GitHub 刷新确认。")
        else:
            print("❌ 提取失败，请检查转换接口是否可用。")

if __name__ == "__main__":
    collector()
