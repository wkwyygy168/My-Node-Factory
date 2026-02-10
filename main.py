import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def check_and_fetch(url):
    """借鉴 subs-check：增加超时控制与状态检查，跳过无效源"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        # 核心借鉴：设置 10秒超时，防止脚本卡死导致 Actions 报错
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200 and len(r.text) > 50:
            content = r.text
            # 全协议识别指纹
            pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
            found = re.findall(pattern, content, re.I)
            
            # 尝试深度 Base64 解码 (处理加密订阅源)
            try:
                decoded = base64.b64decode(content.strip()).decode('utf-8')
                found.extend(re.findall(pattern, decoded, re.I))
            except: pass
            return found
    except:
        return []

def collector():
    print("🛰️ [SYSTEM] 正在启动全球 80+ 源并行收割引擎 (借鉴质量探针逻辑)...")
    
    # --- 已为你填好的 80+ 条源列表，严格校对标点符号 ---
    targets = [
        "https://raw.githubusercontent.com/freefq/free/master/v2ray",
        "https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt",
        "https://raw.githubusercontent.com/Pawpieee/Free-Proxies/main/sub/sub_merge.txt",
        "https://raw.githubusercontent.com/anaer/Sub/master/v2ray.txt",
        "https://raw.githubusercontent.com/LonUp/NodeList/main/NodeList",
        "https://raw.githubusercontent.com/ssrsub/ssr/master/v2ray",
        "https://raw.githubusercontent.com/tianfong/free-nodes/main/node.txt",
        "https://raw.githubusercontent.com/ermaozi/get_node/main/subscribe/v2ray.txt",
        "https://raw.githubusercontent.com/mianfeifq/share/main/data.txt",
        "https://raw.githubusercontent.com/w1770946466/Auto_Node/main/node.txt",
        "https://raw.githubusercontent.com/vless-js/v2ray-free/main/v2ray",
        "https://raw.githubusercontent.com/colatiger/v2ray-nodes/master/updates/v2ray.txt",
        "https://raw.githubusercontent.com/FMYX/FreeNode/main/node.txt",
        "https://raw.githubusercontent.com/snakem982/proxypool/main/source/all.txt",
        "https://raw.githubusercontent.com/mahdibland/SSAggregator/master/sub/sub_merge.txt",
        "https://raw.githubusercontent.com/nodefree/free-nodes/main/nodes/nodes.txt",
        "https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/nodefree.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/wenode.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/clashmeta.txt",
        "https://raw.githubusercontent.com/xiaoji235/airport-free/main/v2ray.txt",
        "https://raw.githubusercontent.com/openit/freenode/master/v2ray.txt",
        "https://raw.githubusercontent.com/learnhard-cn/free_nodes/master/v2ray.txt",
        "https://raw.githubusercontent.com/yuandongying/free-nodes/main/v2ray.txt",
        "https://raw.githubusercontent.com/Fndroid/clash_config/master/v2ray.txt",
        "https://raw.githubusercontent.com/firefoxmmx2/v2rayshare_subcription/main/subscription/clash_sub.yaml",
        "https://raw.githubusercontent.com/Q3dlaXpoaQ/V2rayN_Clash_Node_Getter/main/APIs/sc0.yaml",
        "https://raw.github
