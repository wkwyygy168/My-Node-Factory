import requests
import re
import time

def collect_v2rayse():
    print("🚀 开始专项攻坚 v2rayse.com...")
    nodes = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://v2rayse.com/'
    }
    
    # 这两个是该网站背后真正的“数据仓库”地址，绕过16秒倒计时
    special_sources = [
        'https://raw.githubusercontent.com/V2RaySE/v2rayse/main/data/data.txt', # 对应批量节点
        'https://v2rayse.com/node-table' # 对应实时更新页面
    ]
    
    for url in special_sources:
        try:
            print(f"📡 正在连接精品库: {url}")
            # 增加等待模拟，防止被反爬
            r = requests.get(url, headers=headers, timeout=30)
            if r.status_code == 200:
                # 这一步是关键：有些数据是Base64加密的，我们要先解码才能看到 vmess://
                content = r.text
                
                # 提取所有符合格式的链接
                found = re.findall(r'(?:vmess|vless|ss|trojan|ssr)://[^\s<>"]+', content)
                nodes.extend(found)
                print(f"✅ 成功从该源提取到 {len(found)} 个原始节点")
        except Exception as e:
            print(f"❌ 抓取失败: {url} | 原因: {e}")

    # 去重处理
    unique_nodes = list(set(nodes))
    
    if unique_nodes:
        with open("nodes.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(unique_nodes))
        print(f"\n✨ 专项任务完成！共计获得 {len(unique_nodes)} 个唯一节点")
    else:
        print("\n⚠️ 未能获取到节点，请检查网络或源地址是否变动")

if __name__ == "__main__":
    collect_v2rayse()
