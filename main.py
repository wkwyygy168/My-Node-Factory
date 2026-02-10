import requests
import re
import base64

def collector():
    print("🛰️ [SYSTEM] 正在启动全协议精品节点收割模式...")
    final_nodes = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    # 这是你刚才验证过、确实有货的精品源地址
    TARGETS = [
        # 针对 v2rayse 的核心数据路径
        'https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt',
        'https://raw.githubusercontent.com/V2RaySE/v2rayse/main/data/data.txt',
        # 针对 nodefree 的原始同步库
        'https://raw.githubusercontent.com/nodefree/free-nodes/main/nodes/nodes.txt',
        # 顶级保底源 (包含大量 SS 节点)
        'https://raw.githubusercontent.com/freefq/free/master/v2ray',
        'https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt'
    ]

    for url in TARGETS:
        try:
            print(f"📡 [SCAN] 正在爆破: {url}")
            r = requests.get(url, headers=headers, timeout=25)
            if r.status_code == 200:
                raw_data = r.text
                
                # --- 核心改进：全协议识别正则 ---
                # 增加了对 ss, ssr, trojan, vmess, vless 的全量支持
                pattern = r'(?:ss|ssr|vmess|vless|trojan)://[^\s<>"]+'
                
                # 1. 尝试直接抓取明文
                found = re.findall(pattern, raw_data, re.IGNORECASE)
                final_nodes.extend(found)

                # 2. 尝试解码 Base64 后再次抓取 (很多 ss 节点藏在加密块里)
                try:
                    decoded = base64.b64decode(raw_data).decode('utf-8')
                    found_decoded = re.findall(pattern, decoded, re.IGNORECASE)
                    final_nodes.extend(found_decoded)
                except:
                    pass
        except:
            pass

    # 深度去重
    unique_nodes = list(set(final_nodes))
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"\n🏆 [FINAL] 任务圆满完成！共计捕获全协议节点: {len(unique_nodes)} 个")
        else:
            # 写入你刚提供的节点作为保底，确保 nodes.txt 绝对有内容可录制
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#博主实测SS精品")
            print("\n🚨 [ALERT] 暂未发现新数据，已手动注入精品备源。")

if __name__ == "__main__":
    collector()
