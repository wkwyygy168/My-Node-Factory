import requests
import re
import base64
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

def fetch_and_decode(url):
    """全平台暴力收割：支持明文、Base64、订阅格式"""
    headers = {'User-Agent': 'clash.meta'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            content = r.text.strip()
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
            found = re.findall(pattern, content, re.I)
            try:
                for _ in range(2):
                    missing_padding = len(content) % 4
                    if missing_padding: content += "=" * (4 - missing_padding)
                    content = base64.b64decode(content).decode('utf-8', errors='ignore')
                    found.extend(re.findall(pattern, content, re.I))
            except: pass
            return found
    except: return []

def get_dynamic_urls():
    """动态日期收割逻辑"""
    dynamic_list = []
    today = datetime.now()
    for i in range(5):
        t = today - timedelta(days=i)
        d_str, m_str, y_str = t.strftime("%Y%m%d"), t.strftime("%m"), t.strftime("%Y")
        dynamic_list.append(f"https://node.nodefree.me/{y_str}/{m_str}/{d_str}.txt")
        dynamic_list.append(f"https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/{d_str}.txt")
    return dynamic_list

def collector():
    print("🚀 [FACTORY] 开启工业化收割模式，正在注入自定义后缀...")
    targets = [
        *get_dynamic_urls(),
        "https://raw.githubusercontent.com/shuaidaoya/FreeNodes/main/nodes.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodes.txt",
        "https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/o/node.txt",
        "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/snippets/nodes.txt",
        "https://t.me/s/v2rayfree",
        "https://t.me/s/V2List",
        "https://raw.githubusercontent.com/awesome-vpn/vpn/master/free.txt",
        "https://raw.githubusercontent.com/mianfeifq/share/main/data.txt"
    ]

    all_found = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(fetch_and_decode, list(set(targets)))
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    
    # --- 核心改进：批量注入后缀 ---
    tagged_nodes = []
    suffix = "youtube@免费开源"
    for node in unique_nodes:
        # 如果节点原本就有备注（带#），我们把它替换掉或加在后面
        if "#" in node:
            # 这里的逻辑是：去掉原有的备注，换成老大的专属备注
            clean_node = node.split("#")[0]
            tagged_nodes.append(f"{clean_node}#{suffix}")
        else:
            tagged_nodes.append(f"{node}#{suffix}")

    with open("nodes.txt", "w", encoding="utf-8") as f:
        if len(tagged_nodes) > 100:
            f.write("\n".join(tagged_nodes))
            print(f"✅ [SUCCESS] 全网收割完毕！已为 {len(tagged_nodes)} 个节点注入专属后缀。")
        else:
            f.write(f"ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#{suffix}")

if __name__ == "__main__":
    collector()
