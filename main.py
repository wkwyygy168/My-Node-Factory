import requests
import re
import base64
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

def fetch_and_decode(url):
    """暴力收割模式：只要网页有东西，全部抓回来"""
    # 模拟真实浏览器，防止部分源（如 Gist）拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            content = r.text.strip()
            # 协议指纹识别：涵盖主流所有协议
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
            
            # 1. 抓取明文（针对 YAML 和 文本格式）
            found = re.findall(pattern, content, re.I)
            
            # 2. 尝试 Base64 暴力解码（针对 Base64.txt 这种纯密文格式）
            try:
                # 自动补全填充符
                missing_padding = len(content) % 4
                if missing_padding:
                    content += "=" * (4 - missing_padding)
                decoded = base64.b64decode(content).decode('utf-8', errors='ignore')
                found.extend(re.findall(pattern, decoded, re.I))
            except:
                pass
            return found
    except:
        return []

def get_dynamic_urls():
    """具备自动日期计算能力：生成最近 10 天的 nodefree 链接"""
    dynamic_list = []
    today = datetime.now()
    for i in range(10):
        target_date = today - timedelta(days=i)
        date_str = target_date.strftime("%Y%m%d")
        month_str = target_date.strftime("%m")
        year_str = target_date.strftime("%Y")
        url = f"https://node.nodefree.me/{year_str}/{month_str}/{date_str}.txt"
        dynamic_list.append(url)
    return dynamic_list

def collector():
    print("🚀 [SYSTEM] 引擎重启：正在合成动态日期源并开启并行收割...")
    
    # 1. 生成动态日期链接
    dynamic_targets = get_dynamic_urls()
    
    # 2. 核心源列表：整合你提供的最新高质量源
    base_targets = [
        # --- 老大新增：Barabama 系列 (含镜像加速) ---
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/yudou66.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/blues.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/ndnode.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodev2ray.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodefree.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/v2rayshare.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/wenode.txt",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/yudou66.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/blues.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/ndnode.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodev2ray.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodefree.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/v2rayshare.yaml",
        "https://gh-proxy.com/raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/wenode.yaml",
        
        # --- 老大新增：shuaidaoya Gist 系列 ---
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/base64.txt",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/mihomo.yaml",
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/history.yaml",

        # --- 原有基础源精选 ---
        "https://raw.githubusercontent.com/freefq/free/master/v2ray",
        "https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt",
        "https://raw.githubusercontent.com/ssrsub/ssr/master/v2ray",
        "https://raw.githubusercontent.com/snakem982/proxypool/main/source/all.txt",
        "https://raw.githubusercontent.com/mahdibland/SSAggregator/master/sub/sub_merge.txt",
        "https://t.me/s/v2rayfree",
        "https://t.me/s/V2List",
        "https://raw.githubusercontent.com/mianfeifq/share/main/data.txt",
        "https://raw.githubusercontent.com/mksshare/SSR-V2ray-Trojan-Clash-subscription/main/Clash.yaml"
    ]

    # 3. 合并所有目标源并去重 URL
    targets = list(set(base_targets + dynamic_targets))

    all_found = []
    # 增加到 40 线程，因为源多了不少，提速收割
    with ThreadPoolExecutor(max_workers=40) as executor:
        results = executor.map(fetch_and_decode, targets)
        for res in results:
            if res:
                all_found.extend(res)

    # 核心：给每个节点注入老大要求的专属后缀
    suffix = "youtube@免费开源"
    tagged_nodes = []
    for node in set(all_found):
        # 清理旧备注，打上新标签
        base_node = node.split('#')[0]
        tagged_nodes.append(f"{base_node}#{suffix}")

    # 4. 覆盖写入 nodes.txt
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if len(tagged_nodes) > 1:
            f.write("\n".join(tagged_nodes))
            print(f"✅ [SUCCESS] 捕获唯一节点: {len(tagged_nodes)} 个，已同步后缀并更新 nodes.txt")
        else:
            f.write(f"ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#{suffix}")

if __name__ == "__main__":
    collector()
