import requests
import re

def collect_v2rayse_depth():
    print("🚀 正在对 v2rayse.com 两个模块进行深度收割...")
    nodes = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Referer': 'https://v2rayse.com/'
    }
    
    # 这两个地址是该站数据最集中的“老巢”，绕过网页 16 秒等待
    targets = [
        # 模块1：批量免费节点（通常对应它背后的大型仓库）
        'https://raw.githubusercontent.com/V2RaySE/v2rayse/main/data/data.txt',
        # 模块2：实时节点更新（直接抓取它同步到公共空间的镜像）
        'https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt',
        # 备选：它在其他平台备份的实时池
        'https://raw.githubusercontent.com/anaer/Sub/master/v2ray.txt'
    ]
    
    for url in targets:
        try:
            print(f"📡 正在爆破模块数据: {url}")
            r = requests.get(url, headers=headers, timeout=30)
            if r.status_code == 200:
                # 尝试提取所有节点协议
                found = re.findall(r'(?:vmess|vless|ss|trojan|ssr)://[^\s<>"]+', r.text)
                nodes.extend(found)
                print(f"--- 成功提取到 {len(found)} 个节点")
        except Exception as e:
            print(f"--- 抓取失败: {url} 原因: {e}")

    # 彻底去重
    unique_nodes = list(set(nodes))
    
    # 写入结果
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_nodes))
    
    print(f"\n✅ 深度收割完成！总计获得唯一精品节点: {len(unique_nodes)} 个")

if __name__ == "__main__":
    collect_v2rayse_depth()
