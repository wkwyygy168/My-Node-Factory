import requests
import re

SOURCES = [
    # 1. 针对 nodefree.me 的原始同步源 (直接抓取它背后的数据库，跳过日期标题)
    'https://raw.githubusercontent.com/nodefree/free-nodes/main/nodes/nodes.txt',
    
    # 2. 针对 v2rayse.com 的核心采集源 (这些是该站节点的主要来源)
    'https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt',
    'https://raw.githubusercontent.com/V2RaySE/v2rayse/main/data/data.txt',
    
    # 3. 补充两个高质量的精英源，确保“保底”
    'https://raw.githubusercontent.com/freefq/free/master/v2ray',
    'https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt'
]

def collect():
    nodes = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for url in SOURCES:
        try:
            print(f"正在收割精品源: {url}")
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                # 增强正则：精准匹配 vmess/vless/ss/trojan 完整链接
                found = re.findall(r'(?:vmess|vless|ss|trojan)://[^\s<>"]+', r.text)
                nodes.extend(found)
                print(f"--- 成功提取 {len(found)} 个节点")
        except Exception as e:
            print(f"--- 抓取失败: {url} 原因: {e}")
            
    # 彻底去重
    unique_nodes = list(set(nodes))
    raw_text = "\n".join(unique_nodes)
    
    # 写入结果
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)
    
    print(f"\n✅ 全部收割完成！总计获得唯一精品节点: {len(unique_nodes)} 个")

if __name__ == "__main__":
    collect()
