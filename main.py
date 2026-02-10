import requests
import re
import base64

SOURCES = [
    'https://t.me/s/v2rayfree',
    'https://t.me/s/v2ray_free_conf',
    'https://t.me/s/free_v2ray_config',
    'https://raw.githubusercontent.com/freefq/free/master/v2ray',
    'https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/mix',
    'https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity'
]

def collect():
    nodes = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            found = re.findall(r'(vmess|vless|ss|trojan)://[^\s<>"]+', r.text)
            nodes.extend(found)
        except:
            pass
            
    unique_nodes = list(set(nodes))
    raw_text = "\n".join(unique_nodes)
    
    with open("nodes.txt", "w", encoding="utf-8") as f:
        f.write(raw_text)
        
    with open("sub_base64.txt", "w", encoding="utf-8") as f:
        encoded = base64.b64encode(raw_text.encode("utf-8")).decode("utf-8")
        f.write(encoded)

if __name__ == "__main__":
    collect()
