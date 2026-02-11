import requests
import re
import base64
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

def fetch_nodes(url):
    """最强兼容抓取：只要有流量，统统抓回来"""
    # 模拟多种 UA，防止被源站屏蔽
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*'
    }
    # 加入 GitHub 镜像加速，提高 Actions 抓取成功率
    mirrors = [url, f"https://ghproxy.net/{url}", f"https://mirror.ghproxy.com/{url}"]
    
    for target in mirrors:
        try:
            r = requests.get(target, headers=headers, timeout=12)
            if r.status_code == 200:
                content = r.text.strip()
                # 覆盖所有主流协议：SS, SSR, Vmess, Vless, Trojan, Hysteria2, Tuic
                pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
                found = re.findall(pattern, content, re.I)
                
                # 尝试 3 层 Base64 深度解码，压榨隐藏节点
                tmp = content
                for _ in range(3):
                    try:
                        missing = len(tmp) % 4
                        if missing: tmp += "=" * (4 - missing)
                        decoded = base64.b64decode(tmp).decode('utf-8', errors='ignore')
                        found.extend(re.findall(pattern, decoded, re.I))
                        tmp = decoded
                    except: break
                return found
        except: continue
    return []

def get_huge_sources():
    """海量源列表：结合 Barabama, shuaidaoya 及全网聚合"""
    sources = []
    today = datetime.now()
    # 动态抓取最近 7 天的归档，保证数量够大
    for i in range(7):
        t = today - timedelta(days=i)
        d, m, y = t.strftime("%Y%m%d"), t.strftime("%m"), t.strftime("%Y")
        sources.append(f"https://node.nodefree.me/{y}/{m}/{d}.txt")
        sources.append(f"https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/{d}.txt")
    
    # 加入更多高产量的聚合源
    extras = [
        "https://raw.githubusercontent.com/shuaidaoya/FreeNodes/main/nodes.txt",
        "https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/o/node.txt",
        "https://raw.githubusercontent.com/snakem982/proxypool/main/source/all.txt",
        "https://raw.githubusercontent.com/mizero/FreeNode/main/nodes.txt",
        "https://raw.githubusercontent.com/tjm022/Free-Node-Merge/main/node.txt",
        "https://raw.githubusercontent.com/Anaer/Sub/master/v2ray.txt",
        "https://raw.githubusercontent.com/LonUp/NodeList/main/NodeList",
        "https://t.me/s/v2rayfree",
        "https://t.me/s/V2List",
        "https://t.me/s/free_v2ray_config"
    ]
    return list(set(sources + extras))

def collector():
    print("🚀 [MASSIVE-COLLECTOR] 开启全量收割，只求数量，后缀注入中...")
    targets = get_huge_sources()
    all_found = []
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(fetch_nodes, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    suffix = "youtube@免费开源"
    
    # 打标：不管好坏，全部贴上老大的标
    final_nodes = [f"{n.split('#')[0]}#{suffix}" for n in unique_nodes]

    if final_nodes:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_nodes))
        print(f"✅ [DONE] 战报：捕获 {len(final_nodes)} 个节点，仓库已更新。")
    else:
        print("❌ 警告：未发现节点，请检查网络。")

if __name__ == "__main__":
    collector()
