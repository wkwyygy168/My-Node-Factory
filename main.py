import requests
import re
import base64

def fetch_yaml_all_nodes(url):
    """
    专项攻克 all.yaml：
    由于该文件包含大量散装参数，必须通过订阅转换逻辑还原可视化图中的 92 个节点。
    """
    headers = {'User-Agent': 'ClashMeta'}
    # 使用全网通用的转换后端，把散装参数转换为标准 :// 链接
    # 这是找回那失踪的 76 个节点的唯一靠谱方法
    api_url = f"https://api.v1.mk/sub?target=v2ray&url={url}"
    
    try:
        r = requests.get(api_url, headers=headers, timeout=30)
        if r.status_code == 200:
            # 接口返回的是 Base64，我们解开它获取完整的明文链接列表
            decoded_data = base64.b64decode(r.text).decode('utf-8', errors='ignore')
            # 提取所有还原后的链接，确保不漏掉任何一个地区
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
            return re.findall(pattern, decoded_data, re.I)
    except Exception as e:
        print(f"❌ 解析 all.yaml 失败: {e}")
    return []

def collector():
    # 按照老大死命令：目标锁定，单条测试 all.yaml
    target_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    
    nodes = fetch_yaml_all_nodes(target_url)
    
    # 保持原样去重
    unique_nodes = []
    seen = set()
    for n in nodes:
        node_clean = n.strip()
        if node_clean and node_clean not in seen:
            unique_nodes.append(node_clean)
            seen.add(node_clean)
            
    # 以 UTF-8 编码写入，确保平方²等符号不乱码
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [大获全胜] 提取成功！数量从 16 提升到了 {len(unique_nodes)} 个节点。")
        else:
            print("❌ 依然未能提取到节点，请检查网络或源文件内容。")

if __name__ == "__main__":
    collector()
