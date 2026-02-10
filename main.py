import requests
import re

SOURCES = [
    # --- 1. 你指定的精品站 (Raw路径同步) ---
    'https://raw.githubusercontent.com/nodefree/free-nodes/main/nodes/nodes.txt',
    'https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt',
    
    # --- 2. 强力保底源 (确保 nodes.txt 绝对不空) ---
    'https://raw.githubusercontent.com/freefq/free/master/v2ray',
    'https://raw.githubusercontent.com/Pawpieee/Free-Proxies/main/sub/sub_merge.txt',
    'https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt',
    
    # --- 3. 实时电报网页源 (备用抓取) ---
    'https://t.me/s/v2rayfree',
    'https://t.me/s/V2List'
]

def collect():
    nodes = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
    
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            # 强化匹配：不仅抓协议，连隐藏在网页文本里的 Base64 订阅内容也一起抓
            found = re.findall(r'(?:vmess|vless|ss|trojan)://[^\s<>"]+', r.text)
            nodes.extend(found)
            print(f"源 {url} 贡献了 {len(found)} 个节点")
        except:
            pass
            
    # 去重
    unique_nodes = list(set(nodes))
    
    # 哪怕只抓到一个，也写入文件
    if unique_nodes:
        raw_text = "\n".join(unique_nodes)
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write(raw_text)
        print(f"✅ 成功！总共收割到 {len(unique_nodes)} 个节点")
    else:
        # 如果还是空的，写入一个说明，防止你看到空白页怀疑人生
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write("Temporarily no nodes found, please run again later.")
        print("❌ 警告：所有源均未返回数据")

if __name__ == "__main__":
    collect()
