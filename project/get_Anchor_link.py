import requests
from bs4 import BeautifulSoup
import time

def extract_room_links(game_url):
    """提取某个游戏页面下所有直播间链接"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'Referer': 'https://www.huya.com/'
    }
    room_links = set()
    try:
        response = requests.get(game_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # filename = 'fuck.html'
        # with open(filename, 'w', encoding='utf-8') as f:
        #     # for link in soup:
        #         f.write(str(soup))
        for a in soup.find_all('a', href=True):
            href = a['href']
            # 只提取类似 /1234567 这样的直播间链接
            if href.startswith('https://www.huya.com/') and href[21:].isdigit():
                room_links.add(href)
    except Exception as e:
        print(f"提取 {game_url} 失败: {e}")
    return room_links

def main():
    all_room_links = set()
    with open('link.txt', 'r', encoding='utf-8') as f:
        game_links = [line.strip() for line in f if line.strip()]
    for game_url in game_links:
        print(f"正在处理: {game_url}")
        room_links = extract_room_links(game_url)
        print(f"  提取到 {len(room_links)} 个直播间")
        all_room_links.update(room_links)
        time.sleep(1)  # 防止请求过快被封
        if len(all_room_links) > 10:
            break
    # 保存所有直播间链接
    with open('room_links.txt', 'w', encoding='utf-8') as f:
        for link in all_room_links:
            f.write(link + '\n')
    print(f"共提取到 {len(all_room_links)} 个直播间链接，已保存到 room_links.txt")

if __name__ == '__main__':
    main()
