import requests
import re

SOURCES = [
    # 精选订阅池（这些链接里通常包含成百上千个节点）
    'https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt',
    'https://raw.githubusercontent.com/LonUp/NodeList/main/NodeList',
    'https://raw.githubusercontent.com/tianfong/free-nodes/main/node.txt',
    'https://raw.githubusercontent.com/ermaozi/get_node/main/subscribe/v2ray.txt',
    # 保持几个更新极快的电报源
    'https://t.me/s/v2rayfree',
    'https://t.me/s/V2List',
    'https://t.me/s/free_v2ray_config'
]

def collect():
    nodes = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            # 这个正则专门抓取完整的节点链接，不会只抓到协议头
            found = re.findall(r'(?:vmess|vless|ss|trojan)://[^\s<>"]+', r.text)
            nodes.extend(found)
        except:
            pass
            
    unique_nodes = list(set(nodes))
    # 只要原始节点，一行一个，方便手动转换
    raw_text = "\n".join(unique_nodes)
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)
    
    print(f"Total nodes found: {len(unique_nodes)}")

if __name__ == "__main__":
    collect()
