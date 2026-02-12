import requests
import re
import base64

def fetch_all_nodes():
    # 锁定那条让你头疼的 all.yaml
    target_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    
    # 借用转换接口：这是把 YAML 里的散装零件（Server/Port/ID）还原成链接的唯一办法
    api_url = f"https://api.v1.mk/sub?target=v2ray&url={target_url}"
    
    nodes = []
    try:
        print("📡 正在还原 92 个节点...")
        r = requests.get(api_url, timeout=30)
        if r.status_code == 200:
            # 接口返回的是 Base64，我们解开它获取 92 条明文
            decoded = base64.b64decode(r.text).decode('utf-8', errors='ignore')
            # 匹配所有链接
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"\',;]+'
            nodes = re.findall(pattern, decoded, re.I)
    except Exception as e:
        print(f"❌ 还原出错: {e}")

    return nodes

def main():
    all_found = fetch_all_nodes()
    
    # 深度去重，确保你的 Karing 列表干干净净
    unique_nodes = []
    seen = set()
    for n in all_found:
        clean_n = n.strip()
        if clean_n and clean_n not in seen:
            unique_nodes.append(clean_n)
            seen.add(clean_n)
    
    # 写入 nodes.txt，强制 UTF-8 确保台湾节点²不乱码
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        f.write("\n".join(unique_nodes))
    
    print(f"📊 任务大获全胜！最终捕获并去重后获得 {len(unique_nodes)} 个节点。")

if __name__ == "__main__":
    main()
