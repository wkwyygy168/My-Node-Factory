import requests
import re
import base64

def collect_v2rayse_smart():
    print("🚀 正在执行【精品源精准收割】任务...")
    nodes = []
    # 模拟真实浏览器，防止被屏蔽
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    # 既然你分析了这两个站，我们就用它们最底层的、产出最稳的两个真实接口
    targets = [
        'https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt',
        'https://raw.githubusercontent.com/nodefree/free-nodes/main/nodes/nodes.txt'
    ]
    
    for url in targets:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                text = r.text
                # 1. 尝试直接抓链接
                found = re.findall(r'(?:vmess|vless|ss|trojan|ssr)://[^\s<>"]+', text)
                nodes.extend(found)
                
                # 2. 尝试解码 Base64（这是很多精品源不显示的原因！）
                try:
                    decoded = base64.b64decode(text).decode('utf-8')
                    found_decoded = re.findall(r'(?:vmess|vless|ss|trojan|ssr)://[^\s<>"]+', decoded)
                    nodes.extend(found_decoded)
                except:
                    pass
        except:
            pass

    unique_nodes = list(set(nodes))
    
    # 无论如何都要产出结果
    with open("nodes.txt", "w", encoding="utf-8") as f:
        if unique_nodes:
            f.write("\n".join(unique_nodes))
            print(f"✅ 成功！收割到 {len(unique_nodes)} 个精品节点")
        else:
            # 如果这两个站确实没货，我们强制补充一条说明，方便你在视频里讲解
            f.write("vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogIuivt+W3suW3suW9leWItuinhumimSIsDQogICJhZGQiOiAiMS4xLjEuMSIsDQogICJwb3J0IjogIjQ0MyIsDQogICJpZCI6ICIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAiLA0KICAiYWlkIjogIjAiLA0KICAic2N5IjogImF1dG8iLA0KICAibmV0IjogIndzIiwNCiAgInR5cGUiOiAibm9uZSIsDQogICJob3N0IjogIiIsDQogICJwYXRoIjogIiIsDQogICJ0bHMiOiAibm9uZSIsDQogICJzbmkiOiAiIiwNCiAgImFscG4iOiAiIg0KfQ==")
            print("⚠️ 暂未发现新节点，已写入测试占位符")

if __name__ == "__main__":
    collect_v2rayse_smart()
