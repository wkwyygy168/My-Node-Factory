import requests
import re
import base64

def fetch_nodes():
    # 锁定那条让你头疼的 all.yaml
    target_url = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    
    # 策略 A：利用专业后端转换（这是找回那 75 个散装节点的唯一办法）
    # 我们借用公共转换 API，把 YAML 翻译成 vmess:// 链接
    api_url = f"https://api.v1.mk/sub?target=v2ray&url={target_url}"
    
    nodes = []
    try:
        print("📡 正在尝试专业通道还原散装节点...")
        r = requests.get(api_url, timeout=30)
        if r.status_code == 200:
            decoded = base64.b64decode(r.text).decode('utf-8', errors='ignore')
            nodes.extend(re.findall(r'(?:ss|vmess|vless|trojan|hy2)://[^\s<>"\',;]+', decoded, re.I))
    except:
        print("⚠️ 转换接口暂时不可用，尝试策略 B...")

    # 策略 B：暴力明文提取（保底逻辑，防止接口挂掉）
    try:
        r = requests.get(target_url, timeout=20)
        if r.status_code == 200:
            nodes.extend(re.findall(r'(?:ss|vmess|vless|trojan|hy2)://[^\s<>"\',;]+', r.text, re.I))
    except:
        pass

    return nodes

def main():
    all_nodes = fetch_nodes()
    
    # 深度去重：利用 set 自动去重，确保 nodes.txt 干净
    unique_nodes = []
    seen = set()
    for n in all_nodes:
        clean_n = n.strip()
        if clean_n and clean_n not in seen:
            unique_nodes.append(clean_n)
            seen.add(clean_n)
    
    # 写入文件，强制使用 UTF-8 确保台湾节点²不乱码
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        f.write("\n".join(unique_nodes))
    
    print(f"📊 任务完成！总共提取并去重后获得 {len(unique_nodes)} 个节点。")

if __name__ == "__main__":
    main()
