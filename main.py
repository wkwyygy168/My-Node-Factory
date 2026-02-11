import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_raw_nodes(url):
    """最原始的抓取：不解码、不改名、不准动任何一个字符"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200: return []
        
        raw_content = r.text
        # 宽容模式正则：只要包含 :// 且后面不是空格、引号、逗号的全部抓走
        # 这样能保住带 ² 符号和特殊参数的所有节点
        pattern = r'[a-zA-Z0-9]+://[^\s<>"\',;]+'
        found = re.findall(pattern, raw_content, re.I)
        
        # 针对 Base64 区域的‘局部’处理
        # 很多源会把节点藏在 Base64 块里，我们只在提取失败时才尝试全局解码
        try:
            # 自动清理干扰，尝试整体解密
            clean_b64 = re.sub(r'[^A-Za-z0-9+/=]', '', raw_content)
            missing = len(clean_b64) % 4
            if missing: clean_b64 += "=" * (4 - missing)
            decoded = base64.b64decode(clean_b64).decode('utf-8', errors='ignore')
            found.extend(re.findall(pattern, decoded, re.I))
        except: pass
        return found
    except: return []

def collector():
    print("🚀 [TRUE-ORIGIN] 正在执行零损耗搬运，力保 120 个节点全部归位...")
    
    # 锁定黄金双源
    targets = [
        "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    ]

    all_found = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_raw_nodes, targets)
        for res in results:
            if res: all_found.extend(res)

    # 深度去重：保留最原始的字符，不做任何 strip 之外的动作
    unique_nodes = []
    seen = set()
    for node in all_found:
        # 只去掉最外层的空格或换行符，内部参数（包括 % 编码）绝对不动
        n = node.strip()
        if n and n not in seen:
            unique_nodes.append(n)
            seen.add(n)
    
    # 强制以 UTF-8 编码写入，确保那个 平方² 不会乱码
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 搬运成功！nodes.txt 已更新，总数：{len(unique_nodes)}。")
        else:
            print("❌ 警告：未发现有效节点。")

if __name__ == "__main__":
    collector()
