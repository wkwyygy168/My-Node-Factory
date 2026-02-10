import requests
import re

def collector():
    # 这一组源是全球目前最稳、量最大、且包含你想要的 SS/Vless 的原始库
    SOURCES = [
        'https://raw.githubusercontent.com/freefq/free/master/v2ray',
        'https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt',
        'https://raw.githubusercontent.com/LonUp/NodeList/main/NodeList',
        'https://raw.githubusercontent.com/nodefree/free-nodes/main/nodes/nodes.txt',
        'https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt',
        'https://raw.githubusercontent.com/mianfeifq/share/main/data.txt'
    ]
    
    nodes = []
    # 模拟真实浏览器请求
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                # 关键：全协议正则，抓取 ss, ssr, vmess, vless, trojan
                found = re.findall(r'(?:ss|ssr|vmess|vless|trojan)://[^\s<>"]+', r.text, re.I)
                nodes.extend(found)
        except:
            continue

    # 深度去重
    unique_nodes = list(set(nodes))
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_nodes))
    
    print(f"✅ 收割完成！已为你准备好 {len(unique_nodes)} 个全网节点。")

if __name__ == "__main__":
    collector()
