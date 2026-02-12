import requests
import re
import base64
import json
from urllib.parse import quote

def fetch_and_assemble_nodes(url):
    """
    终极方案：不再找现成的，而是手动‘组装’零件。
    针对 all.yaml 里的 92 个节点，把散装参数拼成标准 VMESS 链接。
    """
    headers = {'User-Agent': 'ClashMeta'}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code != 200: return []
        
        raw_text = r.text
        # 1. 抓取原本就有的 17 条成品
        found_nodes = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"\',;]+', raw_text, re.I)

        # 2. 核心：暴力提取散装参数（针对剩下 75 个节点）
        # 匹配每一组 proxy 定义块
        proxy_blocks = re.findall(r'-\s*{[^}]+}', raw_text)
        if not proxy_blocks:
            # 如果是换行格式，匹配多行参数
            proxy_blocks = re.split(r'-\s*name:', raw_text)[1:]

        for block in proxy_blocks:
            try:
                # 提取关键零件
                name = re.search(r'name:\s*"?([^"\n,]+)"?', block)
                server = re.search(r'server:\s*"?([^"\n,]+)"?', block)
                port = re.search(r'port:\s*(\d+)', block)
                uuid = re.search(r'uuid:\s*"?([^"\n,]+)"?', block)
                aid = re.search(r'alterId:\s*(\d+)', block)
                
                if server and port and uuid:
                    # 组装 VMESS 标准 JSON 格式
                    vmess_obj = {
                        "v": "2", "ps": name.group(1).strip() if name else "Node",
                        "add": server.group(1).strip(), "port": port.group(1),
                        "id": uuid.group(1).strip(), "aid": aid.group(1) if aid else "0",
                        "scy": "auto", "net": "ws", "type": "none", "host": "", "path": "", "tls": ""
                    }
                    # 转成 Base64 链接
                    vmess_json = json.dumps(vmess_obj)
                    vmess_b64 = base64.b64encode(vmess_json.encode('utf-8')).decode('utf-8')
                    found_nodes.append(f"vmess://{vmess_b64}")
            except: continue

        # 3. 如果还是不够，直接动用‘订阅转换’接口作为最终保底（全网最稳方案）
        if len(found_nodes) < 50:
            api_url = f"https://api.v1.mk/sub?target=v2ray&url={url}"
            res = requests.get(api_url, timeout=20)
            if res.status_code == 200:
                decoded = base64.b64decode(res.text).decode('utf-8', errors='ignore')
                found_nodes.extend(re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"\',;]+', decoded, re.I))

        return found_nodes
    except: return []

def collector():
    target = "https://gist.githubusercontent.com/shuaidaoya/9e5cf2749c0ce79932dd9229d9b4162b/raw/all.yaml"
    nodes = fetch_and_assemble_nodes(target)
    
    unique_nodes = []
    seen = set()
    for n in nodes:
        if n and n not in seen:
            unique_nodes.append(n)
            seen.add(n)
            
    with open("nodes.txt", "w", encoding="utf-8", newline='\n') as f:
        f.write("\n".join(unique_nodes))
        print(f"✅ 提取任务完成！总数：{len(unique_nodes)}")

if __name__ == "__main__":
    collector()
