import requests
import base64
import re
import os
import random

# --- CONFIGURATION ---
# 1. Configs per file
SPLIT_SIZE = 500 

# 2. Maximum number of Sub files (Sub1.txt to Sub40.txt)
MAX_SUB_FILES = 40

SOURCES = [
    "https://bypass.shayshayblack.dpdns.org/fb226b97-8410-41b0-ab28-121d4ab9c7c1/sub",
    
 
]

PROTOCOLS = ['vmess://', 'vless://', 'trojan://', 'ss://', 'ssr://', 'hysteria://', 'hysteria2://', 'tuic://']

def decode_base64(data):
    data = data.strip().replace('\n', '').replace('\r', '')
    try:
        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)
        return base64.b64decode(data).decode('utf-8', errors='ignore')
    except:
        return data

def fetch_and_parse():
    unique_configs = set()
    print(f"[-] Fetching from {len(SOURCES)} sources...")

    for url in SOURCES:
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code != 200:
                continue
            
            content = resp.text.strip()
            
            if not any(p in content for p in PROTOCOLS):
                decoded = decode_base64(content)
                if any(p in decoded for p in PROTOCOLS):
                    content = decoded
            
            for line in content.splitlines():
                line = line.strip()
                if not line: continue
                if any(line.startswith(p) for p in PROTOCOLS):
                    unique_configs.add(line)
                        
        except Exception as e:
            print(f"   [!] Error: {e}")

    return list(unique_configs)

def save_configs(configs):
    random.shuffle(configs)

    if not os.path.exists('splitted'):
        os.makedirs('splitted')

    # --- PART 1: Protocol Files (Saved in 'splitted' folder) ---
    categorized = {
        'vmess': [], 'vless': [], 'trojan': [], 'ss': [], 'ssr': [], 'hysteria': [], 'tuic': []
    }
    
    for conf in configs:
        for proto in categorized.keys():
            if conf.startswith(f"{proto}://"):
                categorized[proto].append(conf)
                break

    for proto, items in categorized.items():
        if items:
            text = '\n'.join(items)
            b64 = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            # Keeping names short in splitted folder too
            with open(f'splitted/{proto}.txt', 'w', encoding='utf-8') as f: f.write(b64)

    # --- PART 2: Short Subscription Files (Sub1.txt, Sub2.txt...) ---
    total_configs = len(configs)
    files_needed = (total_configs // SPLIT_SIZE) + (1 if total_configs % SPLIT_SIZE != 0 else 0)
    actual_files = min(files_needed, MAX_SUB_FILES)

    print(f"\n[-] Generating {actual_files} Short Subscription Files...")

    for i in range(actual_files):
        chunk = configs[i * SPLIT_SIZE : (i + 1) * SPLIT_SIZE]
        chunk_text = '\n'.join(chunk)
        chunk_b64 = base64.b64encode(chunk_text.encode('utf-8')).decode('utf-8')
        
        filename = f"Sub{i+1}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(chunk_b64)
        print(f"    -> {filename}")

    # --- PART 3: The "All" File (Renamed to be short) ---
    all_text = '\n'.join(configs)
    all_b64 = base64.b64encode(all_text.encode('utf-8')).decode('utf-8')
    
    with open('All.txt', 'w', encoding='utf-8') as f: 
        f.write(all_b64)

if __name__ == "__main__":
    configs = fetch_and_parse()
    save_configs(configs)
