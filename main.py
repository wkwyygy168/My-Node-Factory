import requests
import re
import base64
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

def fetch_and_decode(url):
    """工业级收割引擎：伪装、强取、解码"""
    # 模拟真实浏览器，防止被源站拦截
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            content = r.text.strip()
            # 协议识别正则：更全面地匹配各类格式
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
            
            # 1. 提取明文
            found = re.findall(pattern, content, re.I)
            
            # 2. 尝试多层 Base64 解码提取
            temp_content = content
            for _ in range(3): # 增加到3层深度，彻底吸干隐藏节点
                try:
                    missing_padding = len(temp_content) % 4
                    if missing_padding: temp_content += "=" * (4 - missing_padding)
                    decoded = base64.b64decode(temp_content).decode('utf-8', errors='ignore')
                    found.extend(re.findall(pattern, decoded, re.I))
                    temp_content = decoded # 递归向下
                except: break
            return found
    except: return []

def get_dynamic_urls():
    """全自动日期推算：对齐 Barabama 逻辑"""
    dynamic_list = []
    today = datetime.now()
    for i in range(10): # 扩大到最近10天，确保每天都有新货
        t = today - timedelta(days=i)
        d_str, m_str, y_str = t.strftime("%Y%m%d"), t.strftime("%m"), t.strftime("%Y")
        dynamic_list.append(f"https://node.nodefree.me/{y_str}/{m_str}/{d_str}.txt")
        dynamic_list.append(f"https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/{d_str}.txt")
    return dynamic_list

def collector():
    print("🚀 [POWER-FACTORY] 引擎全功率开启，正在横扫全网资源...")
    
    # 精选两大家最强源 + 你的 80+ 基础源
    targets = list(set([
        *get_dynamic_urls(),
        "https://raw.githubusercontent.com/shuaidaoya/FreeNodes/main/nodes.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodes.txt",
        "https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/o/node.txt",
        "https://raw.githubusercontent.com/tjm022/Free-Node-Merge/main/node.txt",
        "https://raw.githubusercontent.com/mizero/FreeNode/main/nodes.txt",
        "https://t.me/s/v2rayfree",
        "https://t.me/s/V2List",
        "https://t.me/s/daily_free_nodes",
        # 这里建议继续保留你原本好用的那几十个链接
    ]))

    all_found = []
    # 50 线程极速突围
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(fetch_and_decode, targets)
        for res in results:
            if res: all_found.extend(res)

    # 深度去重
    unique_nodes = list(set(all_found))
    
    # --- 核心打标逻辑 ---
    final_nodes = []
    suffix = "youtube@免费开源"
    for node in unique_nodes:
        # 清理旧备注，注入老大专属标
        base_node = node.split("#")[0]
        final_nodes.append(f"{base_node}#{suffix}")

    # --- 改进后的写入逻辑：移除保底机制，抓到多少写多少 ---
    if final_nodes:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_nodes))
        print(f"✅ [SUCCESS] 战果：捕获 {len(final_nodes)} 个节点，后缀已注入。")
    else:
        print("❌ [FAILED] 本次未抓到有效节点，请检查网络环境。")

if __name__ == "__main__":
    collector()
