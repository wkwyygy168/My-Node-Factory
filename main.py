import requests
import re
import base64
import time

# 精准打击目标与全球备选库
TARGETS = [
    # --- 核心目标：你指定的精品站镜像 ---
    'https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt',
    'https://raw.githubusercontent.com/nodefree/free-nodes/main/nodes/nodes.txt',
    
    # --- 全球实时同步池 (黑客级保底) ---
    'https://raw.githubusercontent.com/freefq/free/master/v2ray',
    'https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt',
    'https://raw.githubusercontent.com/LonUp/NodeList/main/NodeList',
    'https://raw.githubusercontent.com/mianfeifq/share/main/data.txt',
    
    # --- Telegram 动态网页解析 ---
    'https://t.me/s/v2rayfree',
    'https://t.me/s/V2List'
]

def smart_decode(content):
    """黑客级动态解码：自动识别并破解 Base64 加密"""
    try:
        # 尝试解码
        decoded = base64.b64decode(content).decode('utf-8')
        if "://" in decoded: return decoded
    except:
        pass
    return content

def collector():
    print("🛰️ [SYSTEM] 正在启动全球节点巡航扫描...")
    final_nodes = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    for url in TARGETS:
        try:
            print(f"📡 [SCANNING] 目标: {url}")
            r = requests.get(url, headers=headers, timeout=25)
            if r.status_code == 200:
                raw_data = r.text
                # 尝试对整个结果进行初步解码
                processed_data = smart_decode(raw_data)
                
                # 使用非贪婪匹配，精准锁定协议链接
                found = re.findall(r'(?:vmess|vless|ss|trojan|ssr)://[^\s<>"]+', processed_data)
                
                # 如果还是空的，尝试进行二次分段解码（针对部分混合加密源）
                if not found:
                    segments = re.findall(r'[A-Za-z0-9+/=]{50,}', raw_data)
                    for seg in segments:
                        found.extend(re.findall(r'(?:vmess|vless|ss|trojan|ssr)://[^\s<>"]+', smart_decode(seg)))
                
                final_nodes.extend(found)
                print(f"✅ [SUCCESS] 捕获数据流: {len(found)} 条")
        except Exception as e:
            print(f"⚠️ [ERROR] 连接中断: {url}")

    # 深度去重与清洗
    unique_nodes = sorted(list(set(final_nodes)))
    
    # 结果写入
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"\n🏆 [FINAL] 收割任务圆满完成！唯一精品资产: {len(unique_nodes)} 个")
        else:
            # 最后的保底：生成一条你的专属博主展示节点
            f.write("vmess://ew0KICAiYWRkIjogIjguOC44LjgiLCAiYWlkIjogIjAiLCAiaG9zdCI6ICIiLCAiaWQiOiAiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwIiwgIm5ldCI6ICJ3cyIsICJwYXRoIjogIiIsICJwb3J0IjogIjQ0MyIsICJwcyI6ICLkv67mlLnlrIzkv67ku6Plm67kuI3ot6_vvIzkvY3nva7mnKrmm7TmlrAiLCAic2N5IjogImF1dG8iLCAic25pIjogIiIsICJ0bHMiOiAibm9uZSIsICJ0eXBlIjogIm5vbmUiLCAidiI6ICIyIn0=")
            print("\n🚨 [ALERT] 全球源暂未产出新数据，已维持系统热度。")

if __name__ == "__main__":
    collector()
