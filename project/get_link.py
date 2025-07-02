import requests
from bs4 import BeautifulSoup
import json
import re

def get_all_game_links():
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'Referer': 'https://www.huya.com/'
    }
    
    # 获取游戏分类页面
    main_url = 'https://www.huya.com/g'
    
    try:
        # 发送请求
        response = requests.get(main_url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        # print(response.url)
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        filename = 'test.html'
        with open(filename, 'w', encoding='utf-8') as f:
            # for link in soup:
                f.write(str(soup))
        # print(f"成功保存 {len(links)} 个游戏链接到 {filename}")
        f.close()
        
        
    except Exception as e:
        print(f"获取游戏链接失败: {e}")
        return []
def extract_links_from_html(filename='test.html'):
    """从本地HTML文件中提取所有有效的游戏链接"""

    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    game_links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        # print(href)
        # 只提取/g/xxx格式的链接
        if '/g/' in href and len(href) > 3:
            game_links.add(href)
    print(f"提取到 {len(game_links)} 个游戏链接")
    return list(game_links)
def save_links_to_file(links, filename='link.txt'):
    """将链接保存到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for link in links:
                f.write(link + '\n')
        print(f"成功保存 {len(links)} 个游戏链接到 {filename}")
    except Exception as e:
        print(f"保存文件失败: {e}")
def work():
    get_all_game_links()
    game_links = extract_links_from_html()
    if game_links:
        # 去重
        unique_links = list(set(game_links))
        print(f"共获取 {len(unique_links)} 个游戏链接")
        
        # 保存到文件
        save_links_to_file(unique_links)
    else:
        print("未获取到任何游戏链接")

if __name__ == '__main__':
    # 获取所有游戏链接
    get_all_game_links()
    game_links = extract_links_from_html()
    if game_links:
        # 去重
        unique_links = list(set(game_links))
        print(f"共获取 {len(unique_links)} 个游戏链接")
        
        # 保存到文件
        save_links_to_file(unique_links)
    else:
        print("未获取到任何游戏链接")