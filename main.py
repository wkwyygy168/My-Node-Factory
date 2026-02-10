import requests
import re
import base64

def collector():
    print("🛰️ [SYSTEM] 正在启动全球全协议聚合收割模式...")
    # 这一组是目前产出最稳、包含 SS/Vless 且支持 Base64 的原始库
    TARGETS = [
        'https://raw.githubusercontent.com/freefq/free/master/v2ray',
        'https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt',
        'https://raw.githubusercontent.com/nodefree/free-nodes/main/nodes/nodes.txt',
        'https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt',
        'https://raw.githubusercontent.com/LonUp/NodeList/main/NodeList',
        'https://t.me/s/v2rayfree',
        'https://t.me/s/V2List'
    ]
    
    final_nodes = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
    
    for url in TARGETS:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                text = r.text
                # 核心改进：全协议正则（ss, ssr, vmess, vless, trojan）
                pattern = r'(?:ss|ssr|vmess|vless|trojan)://[^\s<>"]+'
                
                # 1. 抓取明文
                final_nodes.extend(re.findall(pattern, text, re.I))
                
                # 2. 尝试全量解码抓取（针对加密源）
                try:
                    decoded = base64.b64decode(text).decode('utf-8')
                    final_nodes.extend(re.findall(pattern, decoded, re.I))
                except: pass
        except: continue

    unique_nodes = list(set(final_nodes))
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ 捕获成功！已聚合 {len(unique_nodes)} 个精品节点")
        else:
            # 写入你之前手动抓到的精品 SS 节点作为保底
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#精品保底节点")

if __name__ == "__main__":
    collector()
