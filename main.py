import requests
import re
import base64

def fetch_and_deduplicate():
    # --- 在这里填入你 Karing 里的所有订阅链接 ---
    sources = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
        # 老大，如果你还有别的链接，直接按格式加在下面
    ]
    
    all_nodes = []
    seen_hashes = set() # 用于去重的核心仓库
    
    headers = {'User-Agent': 'ClashMeta'}
    pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"\',;]+'

    for url in sources:
        try:
            # 统一通过转换接口，确保 YAML 和 Base64 都能变成标准的 :// 链接
            api_url = f"https://api.v1.mk/sub?target=v2ray&url={url}"
            r = requests.get(api_url, headers=headers, timeout=30)
            
            if r.status_code == 200:
                decoded = base64.b64decode(r.text).decode('utf-8', errors='ignore')
                found = re.findall(pattern, decoded, re.I)
                
                for node in found:
                    # 关键去重逻辑：去掉节点名字(#后面部分)，只根据服务器配置内容去重
                    core_config = node.split('#')[0] if '#' in node else node
                    if core_config not in seen_hashes:
                        all_nodes.append(node.strip())
                        seen_hashes.add(core_config)
        except:
            continue

    return all_nodes

def main():
    print("🚀 开始筛选 Karing 订阅源中的有用节点...")
    final_nodes = fetch_and_deduplicate()
    
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        f.write("\n".join(final_nodes))
    
    print(f"✅ 筛选去重完成！共保留 {len(final_nodes)} 个唯一节点。")

if __name__ == "__main__":
    main()
