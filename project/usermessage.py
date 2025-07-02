#!/usr/bin/env python3
# coding=utf-8
# author:sakuyo
#----------------------------------

import csv, time, sys, signal
import re
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Huya(object):
    def SaveToCSV(self, fileName, headers, contents):
        with open(fileName + '.csv', 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(contents)
            print('写入完成！')

def get_user_info_from_username_elem(driver, username_elem):
    try:
        driver.set_window_size(1400, 900)
        # 滚动到弹幕区并激活
        try:
            chatRoomList = driver.find_element(By.ID, "chat-room__list")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", chatRoomList)
            chatRoomList.click()
            time.sleep(0.2)
        except Exception:
            pass

        # 滚动到用户名
        for _ in range(2):
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", username_elem)
            time.sleep(0.3)

        # 确保元素可见且可点击
        WebDriverWait(driver, 5).until(EC.visibility_of(username_elem))
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".name.J_userMenu")))
            username_elem.click()
        except Exception:
            # 如果常规点击失败，尝试JS点击
            driver.execute_script("arguments[0].click();", username_elem)
        time.sleep(2)

        user_card = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[class*='ucard-normal']"))
        )
        user_info = {}

        # 用户名
        try:
            user_info['用户名'] = user_card.find_element(By.CSS_SELECTOR, "[class*='ucard-name']").get_attribute("title")
        except Exception:
            user_info['用户名'] = ""

        # 性别
        try:
            if user_card.find_elements(By.CSS_SELECTOR, "[class*='ucard-boy']"):
                user_info['性别'] = "男"
            elif user_card.find_elements(By.CSS_SELECTOR, "[class*='ucard-girl']"):
                user_info['性别'] = "女"
            else:
                user_info['性别'] = ""
        except Exception:
            user_info['性别'] = ""

        # 等级
        try:
            lv_elem = user_card.find_element(By.CSS_SELECTOR, "[class*='Lv-']")
            lv_class = lv_elem.get_attribute("class")
            # 匹配 Lv-数字-- 这种格式
            match = re.search(r'Lv-(\d+)--', lv_class)
            if match:
                user_info['等级'] = match.group(1)
            else:
                user_info['等级'] = ""
        except Exception:
            user_info['等级'] = ""

        # 年龄
        try:
            age_elem = user_card.find_element(By.CSS_SELECTOR, "[class*='ucard-age']")
            user_info['年龄'] = age_elem.text
        except Exception:
            user_info['年龄'] = ""

        # 地理位置
        try:
            location_elem = user_card.find_element(By.CSS_SELECTOR, "[class*='ucard-location'] + span")
            user_info['地理位置'] = location_elem.text
        except Exception:
            user_info['地理位置'] = ""

        # 粉丝数
        try:
            fans_elem = user_card.find_element(By.CSS_SELECTOR, "[class*='ucard-fans']")
            user_info['粉丝数'] = fans_elem.text
        except Exception:
            user_info['粉丝数'] = ""

        # 贵族（如有）
        try:
            noble_elem = user_card.find_element(By.CSS_SELECTOR, "[class*='ucard-mounts']")
            user_info['贵族'] = noble_elem.text
        except Exception:
            user_info['贵族'] = ""

        # 关闭弹窗（点击页面空白处或ESC，视虎牙实际情况而定）
        driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(0.2)

        return user_info
    except Exception as e:
        print("[DEBUG] username_elem outerHTML:", username_elem.get_attribute('outerHTML'))
        driver.save_screenshot("debug_userinfo.png")
        print("用户信息弹窗未出现或解析失败:", e)
        return None

def collect_user_info(driver, chatMsgs, userInfoDict):
    for idx, chatMsg in enumerate(chatMsgs):
        try:
            # 兼容所有用户名样式
            try:
                username_elem = chatMsg.find_element(By.CSS_SELECTOR, "[title='点击查看个人信息']")
                username = username_elem.text.strip()
            except Exception as e:
                print(f"[WARN] 弹幕{idx}未找到用户名元素: {e}")
                print("[DEBUG] chatMsg outerHTML:", chatMsg.get_attribute('outerHTML'))
                continue

            if username and username not in userInfoDict:
                print(f"[INFO] 采集用户：{username}")
                user_info = get_user_info_from_username_elem(driver, username_elem)
                if user_info and user_info.get('用户名'):
                    userInfoDict[username] = user_info
                    print(user_info)
                time.sleep(1)
        except Exception as e:
            print(f"[WARN] 采集单个用户异常: {e}")
            print("[DEBUG] chatMsg outerHTML:", chatMsg.get_attribute('outerHTML'))
            continue

def safe_get_user_info(driver, chatMsg):
    for _ in range(2):  # 最多尝试2次
        try:
            username_elem = chatMsg.find_element(By.CSS_SELECTOR, ".name.J_userMenu")
            return get_user_info_from_username_elem(driver, username_elem)
        except Exception:
            time.sleep(0.5)
    return None

class HuyaLive(Huya):
    def __init__(self, target):
        self.target = target
        self.userInfoDict = {}  # 用于去重，key为用户名

    def Connect(self):
        edge_options = Options()
        # edge_options.add_argument('--headless')
        edge_options.add_experimental_option("detach", True)
        print("[INFO] 启动Edge浏览器...")
        driver = webdriver.Edge(options=edge_options)
        url = 'https://www.huya.com/' + self.target
        print(f"[INFO] 打开直播间：{url}")
        driver.get(url)
        time.sleep(5)
        print("[INFO] 页面加载完成，开始采集用户信息...")

        while True:
            time.sleep(1)
            try:
                chatRoomList = driver.find_element(By.ID, "chat-room__list")
                chatMsgs = chatRoomList.find_elements(By.CSS_SELECTOR, '[data-cmid]')
                print(f"[DEBUG] 本轮检测到弹幕数：{len(chatMsgs)}")
                collect_user_info(driver, chatMsgs, self.userInfoDict)
            except Exception as e:
                print(f"[ERROR] 获取弹幕列表异常: {e}")

def QuitAndSave(signum, frame):
    print('catched singal: %d' % signum)
    # 保存所有用户信息
    if hyObj.userInfoDict:
        headers = ['用户名', '性别', '等级', '年龄', '地理位置', '粉丝数', '贵族']
        hyObj.SaveToCSV('user_info', headers, list(hyObj.userInfoDict.values()))
    sys.exit(0)

def collect_huya_users(room_id, duration=30):
    """
    采集指定虎牙房间弹幕用户信息，采集时长为duration秒，返回用户信息列表，并保存到 user_info.csv
    :param room_id: 房间号或URL
    :param duration: 采集时长（秒）
    :return: 用户信息列表（list of dict）
    """
    edge_options = Options()
    # edge_options.add_argument('--headless')  # 如需无头模式可打开
    edge_options.add_experimental_option("detach", True)
    driver = webdriver.Edge(options=edge_options)
    if room_id.startswith("http"):
        room_id = room_id.rstrip('/').split('/')[-1]
    url = 'https://www.huya.com/' + room_id
    print(f"[INFO] 打开直播间：{url}")
    driver.get(url)
    time.sleep(5)
    print("[INFO] 页面加载完成，开始采集用户信息...")

    userInfoDict = {}
    start_time = time.time()
    try:
        while time.time() - start_time < duration:
            time.sleep(1)
            try:
                chatRoomList = driver.find_element(By.ID, "chat-room__list")
                chatMsgs = chatRoomList.find_elements(By.CSS_SELECTOR, '[data-cmid]')
                print(f"[DEBUG] 本轮检测到弹幕数：{len(chatMsgs)}")
                collect_user_info(driver, chatMsgs, userInfoDict)
            except Exception as e:
                print(f"[ERROR] 获取弹幕列表异常: {e}")
    finally:
        driver.quit()

    # 保存到 user_info.csv
    if userInfoDict:
        headers = ['用户名', '性别', '等级', '年龄', '地理位置', '粉丝数', '贵族']
        Huya().SaveToCSV('user_info', headers, list(userInfoDict.values()))
        print(f"[INFO] 已保存 {len(userInfoDict)} 条用户信息到 user_info.csv")
    else:
        print("[INFO] 未采集到任何用户信息")
    return list(userInfoDict.values())

if __name__ == '__main__':
    # 信号监听
    signal.signal(signal.SIGTERM, QuitAndSave)
    signal.signal(signal.SIGINT, QuitAndSave)

    if len(sys.argv) > 1:
        room_id = sys.argv[1]
    else:
        room_id = input("请输入房间ID或URL：").strip()
    if room_id.startswith("http"):
        room_id = room_id.rstrip('/').split('/')[-1]

    # 监听前清空csv文件内容
    open('user_info.csv', 'w', encoding='utf-8-sig').close()

    hyObj = HuyaLive(room_id)
    hyObj.Connect()
# 333003