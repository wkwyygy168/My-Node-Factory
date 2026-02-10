import requests
import re
import base64

def hacker_collector():
    # 重新筛选的【全球一级货源】，这些源每天产出超过 1000+ 节点
    SOURCES = [
        # 全球节点聚合标杆
        'https://raw.githubusercontent.com/freefq/free/master/v2ray',
        'https://raw.githubusercontent.com/vpei/free-node/master/v2ray.txt',
        'https://raw.githubusercontent.com/tianfong/free-nodes/main/node.txt',
        'https://raw.githubusercontent.com/Pawpieee/Free-Proxies/main/sub/sub_merge.txt',
        'https://raw.githubusercontent.com/LonUp/NodeList/main/NodeList',
        # Telegram 实时网页镜像（更新最快，延迟最低）
        'https://t.me/s/v2rayfree',
        'https://t.me/s/V2List',
        'https://t.me/s/v2ray_free_conf',
        # 你最信任的两个精品站底层镜像
        'https://raw.githubusercontent.com/v2rayse/free-node/main/v2ray.txt',
        'https://raw.githubusercontent.com/nodefree/free-nodes/main/nodes/nodes.txt'
    ]
    
    nodes = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                # 模糊协议匹配：ss, ssr, vmess, vless, trojan, hysteria, tuic
                content = r.text
                # 尝试第一次解码
                try:
                    content += "\n" + base64.b64decode(content).decode('utf-8')
                except: pass
                
                found = re.findall(r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+', content, re.I)
                nodes.extend(found)
        except: continue

    # 核心算法：基于指纹的唯一性去重
    unique_nodes = list(set(nodes))
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        # 确保哪怕源头全挂，也有保底输出，防止订阅为空
        if len(unique_nodes) > 10:
            f.write("\n".join(unique_nodes))
        else:
            # 引入应急预案：当主流源失效，强制从备用紧急库拉取
            emergency = requests.get('https://raw.githubusercontent.com/anaer/Sub/master/v2ray.txt').text
            f.write(emergency)

    print(f"🚀 收割任务完成！当前活鱼池容量: {len(unique_nodes)}")

if __name__ == "__main__":
    hacker_collector()
