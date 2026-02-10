import requests
import re
import base64
from concurrent.futures import ThreadPoolExecutor

def fetch_content(url):
    """双路径抓取逻辑：尝试镜像加速，失败则回退原始链接"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 尝试将 GitHub 转换为 jsDelivr 镜像，绕过 GitHub 自身对 Actions 的访问限制
    alt_url = url
    if "raw.githubusercontent.com" in url:
        try:
            parts = url.split('/')
            if len(parts) >= 6:
                user, repo, branch = parts[3], parts[4], parts[5]
                path = "/".join(parts[6:])
                alt_url = f"https://fastly.jsdelivr.net/gh/{user}/{repo}@{branch}/{path}"
        except: pass

    for target_url in [alt_url, url]:
        try:
            r = requests.get(target_url, headers=headers, timeout=15)
            if r.status_code == 200:
                content = r.text.strip()
                # 协议指纹识别
                pattern = r'(?:ss|ssr|vmess|vless|trojan|hy2|tuic)://[^\s<>"]+'
                nodes = re.findall(pattern, content, re.I)
                
                # 暴力 Base64 解码，解决节点数只有 1 的问题
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
    print("🚀 [SYSTEM] 引擎 V11.0 启动：全源深度爆破模式...")
    # 已经为你填好并校对过的 80 条源，严防语法错误导致打叉
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
        "https://raw.githubusercontent.com/chengaopan/AutoMergePublicNodes/master/list.yml",
        "https://raw.githubusercontent.com/zhangkaiitugithub/passcro/main/speednodes.yaml",
        "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/snippets/nodes.meta.yml",
        "https://raw.githubusercontent.com/Ruk1ng001/freeSub/main/clash.yaml",
        "https://raw.githubusercontent.com/actionsfz/v2ray/master/all.yaml",
        "https://raw.githubusercontent.com/go4sharing/sub/main/sub.yaml",
        "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
        "https://raw.githubusercontent.com/acymz/AutoVPN/main/data/V2.txt",
        "https://t.me/s/v2rayfree",
        "https://t.me/s/V2List",
        "https://t.me/s/free_v2ray_config",
        "https://t.me/s/v2ray_free_conf",
        "https://t.me/s/ssrList",
        "https://t.me/s/C_137_channel",
        "https://t.me/s/daily_free_nodes",
        "https://t.me/s/vmess_vless_ss",
        "https://t.me/s/vpn_v2ray_vpn",
        "https://t.me/s/Outline_Vpn",
        "https://raw.githubusercontent.com/ripaojiedian/freenode/main/clash",
        "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/ndnode.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/main/nodes/v2rayshare.txt",
        "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/Clash/Config.yaml",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/mixed",
        "https://raw.githubusercontent.com/mianfeifq/share/main/data",
        "https://raw.githubusercontent.com/roster0/v2ray/main/list",
        "https://raw.githubusercontent.com/Alien136/clash-proxies/main/clash.yaml",
        "https://raw.githubusercontent.com/oslook/clash-freenode/main/clash.yaml",
        "https://raw.githubusercontent.com/Subscrazy/Subscrazy/master/sub",
        "https://raw.githubusercontent.com/erick-wan/AutoSubscribe/master/subscribe/clash.yaml",
        "https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/Long_term_maintenance_Clash.yaml",
        "https://raw.githubusercontent.com/snakem982/Proxies/main/clash.yaml",
        "https://raw.githubusercontent.com/suda/v2ray-subscribe/main/sub/sub.txt",
        "https://raw.githubusercontent.com/v2ray-links/v2ray-free/master/v2ray",
        "https://raw.githubusercontent.com/Jsnzkpg/Jsnzkpg/Jsnzkpg/clash/clash.yaml",
        "https://raw.githubusercontent.com/Domparire/Clash/main/Clash.yaml",
        "https://raw.githubusercontent.com/r00t-shell/v2ray-subscription/main/subs/v2ray",
        "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/all.txt",
        "https://raw.githubusercontent.com/yugogo/clash_config/main/clash.yaml",
        "https://raw.githubusercontent.com/tazzmaniac/Clash/main/clash.yaml",
        "https://raw.githubusercontent.com/Rea1l/V2ray-Configs/main/V2ray-configs.txt",
        "https://raw.githubusercontent.com/SnapdragonLee/SystemProxy/master/dist/clash_config.yaml",
        "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge_base64.txt",
        "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/all_extracted_configs.txt",
        "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix",
        "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub1.txt",
        "https://raw.githubusercontent.com/barry-far/V2ray-Config/main/Sub2.txt",
        "https://raw.githubusercontent.com/MatinGhanbari/v2ray-configs/main/subscriptions/v2ray/all_sub.txt",
        "https://raw.githubusercontent.com/ts-sf/fly/main/v2",
        "https://raw.githubusercontent.com/openRunner/clash-freenode/main/clash.yaml",
        "https://raw.githubusercontent.com/xrayfree/free-ssr-ss-v2ray-vpn-clash/main/clash.yaml",
        "https://raw.githubusercontent.com/vorz1k/v2box/main/supreme_vpns_1.txt",
        "https://raw.githubusercontent.com/AzadNetCH/Clash/main/AzadNet.txt",
        "https://raw.githubusercontent.com/vpei/Free-Node-Merge/main/o/node.txt",
        "https://raw.githubusercontent.com/WilliamStar007/ClashX-V2Ray-TopFreeProxy/main/combine/v2ray.config.txt",
        "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config.txt",
        "https://raw.githubusercontent.com/mksshare/SSR-V2ray-Trojan-Clash-subscription/main/Clash.yaml"
    ]

    all_found = []
    # 使用 20 线程，兼顾速度与稳定性
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(fetch_content, targets)
        for res in results:
            if res: all_found.extend(res)

    unique_nodes = list(set(all_found))
    with open("nodes.txt", "w", encoding="utf-8") as f:
        # 只要抓到 1 个以上的节点，就正常写入
        if len(unique_nodes) > 1:
            f.write("\n".join(unique_nodes))
            print(f"✅ [SUCCESS] 爆破完成！捕获唯一节点: {len(unique_nodes)} 个")
        else:
            # 最终防御：哪怕抓不到，也绝对不让文件为空导致 Karing 报错
            f.write("ss://YWVzLTI1Ni1jZmI6WG44aktkbURNMDBJZU8lIyQjZkpBTXRzRUFFVU9wSC9ZV1l0WXFERm5UMFNWQDEwMy4xODYuMTU1LjI3OjM4Mzg4#引擎维护中_请稍后刷新")

if __name__ == "__main__":
    collector()
