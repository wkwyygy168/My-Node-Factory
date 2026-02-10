import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            text = r.text.strip()
            # 协议指纹
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
            
            # 第一步：直接找明文节点
            found = re.findall(pattern, text, re.I)
            
            # 第二步：尝试整体 Base64 解码（解决很多订阅源全加密的问题）
            try:
                # 补全 base64 填充符，防止报错
                missing_padding = len(text) % 4
                if missing_padding: text += '=' * (4 - missing_padding)
                decoded = base64.b64decode(text).decode('utf-8')
                found.extend(re.findall(pattern, decoded, re.I))
            except: pass
            
            # 第三步：按行扫描（针对混合格式）
            for line in text.splitlines():
                if len(line.strip()) > 30 and '://' not in line:
                    try:
                        line_dec = base64.b64decode(line.strip()).decode('utf-8')
                        found.extend(re.findall(pattern, line_dec, re.I))
                    except: pass
            return found
    except: return []

def collector():
    print("🛰️ [SYSTEM] 引擎全开：正在进行全量深度爆破...")
    # 保持你那 80 条源不变
    targets = [ "这里放你那80条源..." ] 
    
    all_found = []
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = executor.map(fetch_content, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if len(unique_nodes) > 5: # 只有超过5个才认为是成功收割
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 爆破完成！捕获节点: {len(unique_nodes)} 个")
        else:
            # 即使失败，保底节点也要带上说明，方便调试
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#节点捕获偏少_源可能在维护")

if __name__ == "__main__":
    collector()
