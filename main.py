import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_and_extract(url):
    """极致兼容抓取：尝试镜像加速 + 暴力解码"""
    # 模拟真实浏览器请求头，防止被源站拉黑
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    # 自动将 GitHub 链接转换为 CDN 镜像，绕过 GitHub Actions 的访问墙
    alt_url = url
    if "raw.githubusercontent.com" in url:
        try:
            parts = url.split('/')
            if len(parts) >= 6:
                user, repo, branch, path = parts[3], parts[4], parts[5], "/".join(parts[6:])
                alt_url = f"https://fastly.jsdelivr.net/gh/{user}/{repo}@{branch}/{path}"
        except: pass

    # 尝试双路抓取：先镜像，后原始
    for target in [alt_url, url]:
        try:
            r = requests.get(target, headers=headers, timeout=15)
            if r.status_code == 200 and len(r.text) > 10:
                content = r.text.strip()
                # 协议指纹识别
                pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
                
                # 1. 抓取明文
                nodes = re.findall(pattern, content, re.I)
                
                # 2. 暴力 Base64 解码 (补全填充符并忽略非标准字符)
                try:
                    b64_str = re.sub(r'[^a-zA-Z0-9+/=]', '', content)
                    missing_padding = len(b64_str) % 4
                    if missing_padding: b64_str += "=" * (4 - missing_padding)
                    decoded = base64.b64decode(b64_str).decode('utf-8', errors='ignore')
                    nodes.extend(re.findall(pattern, decoded, re.I))
                except: pass
                
                if nodes: return nodes
        except: continue
    return []

def collector():
    print("🚀 [SYSTEM] 引擎 V13.0：启动全球 CDN 镜像爆破模式...")
    # 这里保持你那 80 条 targets 不变
    targets = [
        # ... 请保持你代码中那 80 条源链接 ...
    ]

    all_found = []
    # 使用 25 线程，兼顾抓取效率与稳定性
    with ThreadPoolExecutor(max_workers=25) as executor:
        results = executor.map(fetch_and_extract, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    with open("nodes.txt", "w", encoding="utf-8") as f:
        # 如果抓到 1 个以上的节点，就正常写入
        if len(unique_nodes) > 1:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 爆破完成！成功收割节点: {len(unique_nodes)} 个")
        else:
            # 修改保底节点，明确提示
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#云端收割机正在全力作业_请稍后刷新")

if __name__ == "__main__":
    collector()
