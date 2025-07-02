import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_room_info(room_url, driver, screenshot_dir='screenshots'):
    info = {
        'room_url': room_url,
        'title': '',
        'screenshot': '',
        'heat': '',
        'anchor_name': '',
        'anchor_level': '',
        'anchor_avatar': '',
        'subscribers': ''
    }
    try:
        driver.get(room_url)
        # 等待页面主要元素加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1, .host-title, .host-name'))
        )
        time.sleep(2)  # 额外等待动态内容加载

        # 标题
        try:
            # 多种选择器尝试
            selectors = [
                '.host-title',
                '.room-title',
                '.room-info-title',
                '.host-content .title',
                'h1'
            ]
            for sel in selectors:
                elems = driver.find_elements(By.CSS_SELECTOR, sel)
                if elems and elems[0].text.strip():
                    info['title'] = elems[0].text.strip()
                    break
            # 兜底：meta标签
            if not info['title']:
                metas = driver.find_elements(By.CSS_SELECTOR, 'meta[name="description"]')
                if metas:
                    info['title'] = metas[0].get_attribute('content')
            # 兜底：页面title
            if not info['title']:
                info['title'] = driver.title
        except Exception:
            info['title'] = ''

        # 截图
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        screenshot_path = os.path.join(screenshot_dir, f"{room_url.split('/')[-1]}.png")
        driver.save_screenshot(screenshot_path)
        info['screenshot'] = screenshot_path

        # 主播昵称
        try:
            selectors = [
                '.host-name',
                '.host-info .name',
                '.host-nickname',
                '.host-name__text',
                '.host-info-nickname',
                '.host-info__name',
            ]
            for sel in selectors:
                elems = driver.find_elements(By.CSS_SELECTOR, sel)
                if elems and elems[0].text.strip():
                    info['anchor_name'] = elems[0].text.strip()
                    break
        except Exception:
            info['anchor_name'] = ''

        # 主播头像
        try:
            selectors = [
                '.host-avatar img',
                '.host-pic img',
                '.host-avatar__img',
                '.host-info-avatar img',
            ]
            for sel in selectors:
                elems = driver.find_elements(By.CSS_SELECTOR, sel)
                if elems:
                    src = elems[0].get_attribute('src') or elems[0].get_attribute('data-original')
                    if src:
                        info['anchor_avatar'] = src
                        break
        except Exception:
            info['anchor_avatar'] = ''

        # 主播等级
        try:
            selectors = [
                '.host-level .level',
                '.host-info .level',
                '.host-level',
                '.host-info-level',
                '.host-level-icon',
                '.host-spectator'
            ]
            for sel in selectors:
                elems = driver.find_elements(By.CSS_SELECTOR, sel)
                if elems and elems[0].text.strip():
                    info['anchor_level'] = elems[0].text.strip()
                    break
        except Exception:
            info['anchor_level'] = ''

        # 热度（参与人数）
        try:
            selectors = [
                '#live-count',
                '.host-spectator em',
                '.host-rank .host-rank-num',
                '.host-info .num',
                '.host-rank-num',
                '.host-info-num',
                '.room-view-count',
                '.player-view-count',
                '.host-view-count',
            ]
            for sel in selectors:
                elems = driver.find_elements(By.CSS_SELECTOR, sel)
                if elems and elems[0].text.strip():
                    info['heat'] = elems[0].text.strip()
                    break
        except Exception:
            info['heat'] = ''

        # 订阅者人数
        try:
            selectors = [
                '.subscribe-num .num',
                '.subscribe .num',
                '.subscribe-num',
                '.subscribe-count',
            ]
            for sel in selectors:
                elems = driver.find_elements(By.CSS_SELECTOR, sel)
                if elems and elems[0].text.strip():
                    info['subscribers'] = elems[0].text.strip()
                    break
        except Exception:
            info['subscribers'] = ''

    except Exception as e:
        print(f"{room_url} 获取失败: {e}")
    return info

def main():
    edgedriver_path = r'C:\Users\24090\Desktop\project最终版3.0\msedgedriver.exe'  # 修改为你的EdgeDriver实际路径
    edge_options = EdgeOptions()
    edge_options.add_argument('--headless')
    edge_options.add_argument('--disable-gpu')
    service = EdgeService(executable_path=edgedriver_path)
    driver = webdriver.Edge(service=service, options=edge_options)

    results = []
    # 判断是否有命令行参数
    if len(sys.argv) > 1:
        # 单个房间
        links = [sys.argv[1]]
    else:
        # 批量
        with open('room_links.txt', 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f if line.strip()]
    for url in links:
        print(f'正在采集: {url}')
        info = get_room_info(url, driver)
        print(info)
        results.append(info)
        time.sleep(2)  # 防止过快被封

    driver.quit()

    # 保存结果到csv
    import csv
    with open('room_info.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print('采集完成，结果已保存到 room_info.csv')

if __name__ == '__main__':
    main()
