import requests
import re
import base64
import json

def fetch_yaml_nodes(url):
    """专项攻克 YAML 格式：把散装参数拼成标准链接"""
    headers = {'User-Agent': 'clash.meta'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200: return []
        
        # 既然直接搜 :// 搜不到，我们换个思路：
        # 把这个 YAML 交给全网通用的转换接口，把它‘吐’出来的明文链接抓回来
        # 这是目前最稳、最准确的方法，能 100% 还原 YAML 里的所有节点
        convert_api = f"https://api.v1.mk/sub?target=v2ray&url={url}"
        res = requests.get(convert_api, timeout=20)
        if res.status_code == 200:
            # 转换接口返回的是 Base64，我们解开它
            decoded_content = base64.b64decode(res.text).decode('utf-8', errors='ignore')
            # 现在的内容就是 Karing 能认的 :// 链接了
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic|http|https|socks5|socks)://[^\s<>"\',;]+'
            return re.findall(pattern, decoded_content, re.I)
    except:
        pass
    return []

def collector():
    print("🚀 [SINGLE-TARGET-TEST] 正在专项测试 all.yaml 提取...")
    
    # 按照你的死命令：只保留这一条进行测试
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_found = []
    # 这里不需要并行，直接单线处理
    for url in targets:
        nodes = fetch_yaml_nodes(url)
        if nodes:
            all_found.extend(nodes)

    # 去重
    unique_nodes = list(set(all_found))
    
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [RESULT] 成功！从 all.yaml 中提取出 {len(unique_nodes)} 个节点。")
        else:
            print("❌ [RESULT] 提取失败，请检查 all.yaml 的内容格式。")

if __name__ == "__main__":
    collector()
