#!/usr/bin/env python3
# coding=utf-8
# author:sakuyo
#----------------------------------

import csv,time,sys,signal
from selenium import webdriver
from selenium.webdriver.edge.options import Options  # 修改为Edge
from selenium.webdriver.common.by import By

class Huya(object):
    def SaveToCSV(self,fileName,headers,contents):
        titles = headers
        data = contents
        #csv用utf-8-sig来保存
        contents = [item for item in contents if item]      # 去除空数据
        # 只保留包含除 time 外其它字段的数据
        contents = [item for item in contents if any(k != 'time' and v for k, v in item.items())]
        with open(fileName+'.csv','a',newline='',encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f,fieldnames=titles)
            writer.writeheader()
            writer.writerows(data)
            print('写入完成！')

class HuyaLive(Huya):

    def __init__(self,target):#初始化 输入值target为直播间ID
        self.target = target
        self.barrageList = {}
    
    def Connect(self):#连接直播间
        edge_options = Options()
        edge_options.add_argument('--headless')
        edge_options.add_experimental_option("detach", True)
        print("[INFO] 启动Edge浏览器...")
        driver = webdriver.Edge(options=edge_options)
        url  ='https://www.huya.com/'+self.target
        print(f"[INFO] 打开直播间：{url}")
        driver.get(url)
        time.sleep(5)
        print("[INFO] 页面加载完成，开始监听弹幕...")
        cnt = 0
        while True: #无限循环，伪监听
            time.sleep(1)
            try:
                chatRoomList = driver.find_element(By.ID, "chat-room__list")
                chatMsgs = chatRoomList.find_elements(By.CSS_SELECTOR, '[data-cmid]')
                print(f"[DEBUG] 本轮检测到弹幕数：{len(chatMsgs)}")
                for chatMsg in chatMsgs:
                    # print('enen')
                    # print(chatMsg.get_attribute('outerHTML'))
                    # print('duck')
                    print(f"[DEBUG] 解析弹幕: {chatMsg.text}")
                    try:
                        dataId = chatMsg.get_attribute('data-cmid')
                        content = {}
                        #尝试是否为礼物弹幕
                        try:
                            hSend = chatMsg.find_element(By.CLASS_NAME, "tit-h-send")
                            # print("是礼物，我们有救了")
                            # print(hSend.get_attribute('outerHTML'))
                            content['username'] = hSend.find_element(By.CSS_SELECTOR, ".cont-item.name.J_userMenu").get_attribute('textContent').strip()
                            content['gift'] = hSend.find_element(By.CSS_SELECTOR, ".cont-item.send-gift img").get_attribute("alt")
                            content['num'] = hSend.find_elements(By.CLASS_NAME, "cont-item")[3].get_attribute('textContent').strip()
                            cnt += 1
                            print(f"[INFO] 检测到礼物弹幕: {content}")
                        except Exception as e:
                            # print(f"[DEBUG] 礼物弹幕解析失败: {e}")
                            pass
                        #尝试是否为消息弹幕
                        try:
                            mSend = chatMsg.find_element(By.CLASS_NAME, "msg-normal")
                            username_elem = mSend.find_element(By.CSS_SELECTOR, ".name.J_userMenu")
                            msg_elem = mSend.find_element(By.CSS_SELECTOR, ".msg.J_msg")
                            # print("[DEBUG] username元素HTML:", username_elem.get_attribute('outerHTML'))
                            # print("[DEBUG] msg元素HTML:", msg_elem.get_attribute('outerHTML'))
                            # 尝试用 textContent
                            username = username_elem.get_attribute('textContent').strip()
                            msg = msg_elem.get_attribute('textContent').strip()
                            print(f"[DEBUG] username: '{username}', msg: '{msg}'")
                            content["username"] = username
                            content["msg"] = msg
                            cnt += 1
                            print(f"[INFO] 检测到普通弹幕: {content}")
                        except Exception as e:
                            # print(f"[DEBUG] 普通弹幕解析失败: {e}")
                            pass
                        self.SaveToBarrageList(cnt,content)
                    except Exception as e:
                        print(f"[WARN] 解析单条弹幕异常: {e}")
                        continue
            except Exception as e:
                print(f"[ERROR] 获取弹幕列表异常: {e}")
            if cnt >= 10000:
                print("[INFO] 已收集到10000条弹幕，退出监听。")
                print("[INFO] 正在保存弹幕数据到CSV文件...")
                normal_barrage = []
                gift_barrage = []
                for item in hyObj.barrageList.values():
                    if item.get('gift', ''):  # 有gift字段即为礼物弹幕
                        gift_barrage.append(item)
                    else:
                        normal_barrage.append(item)
                normal_barrage = [item for item in normal_barrage if item]  # 去除空数据
                gift_barrage = [item for item in gift_barrage if item]      # 去除空数据
                # 只保留包含除 time 外其它字段的数据
                normal_barrage = [item for item in normal_barrage if any(k != 'time' and v for k, v in item.items())]
                gift_barrage = [item for item in gift_barrage if any(k != 'time' and v for k, v in item.items())]
                hyObj.SaveToCSV('normal_barrage', ['username', 'time', 'msg'], normal_barrage)
                hyObj.SaveToCSV('gift_barrage', ['username', 'time', 'gift', 'num'], gift_barrage)
                print("[INFO] 弹幕数据保存完成。")
                sys.exit(0)

    def SaveToBarrageList(self,dataId,content):#弹幕列表存储
        if dataId in self.barrageList or not content: #去重、去空
            pass
        else:
            content['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            self.barrageList[dataId] = content
            print(dataId,content)

def QuitAndSave(signum, frame):  # 监听退出信号
    print('catched singal: %d' % signum)
    # 分别保存普通弹幕和礼物弹幕
    normal_barrage = []
    gift_barrage = []
    for item in hyObj.barrageList.values():
        if item.get('gift', ''):  # 有gift字段即为礼物弹幕
            gift_barrage.append(item)
        else:
            normal_barrage.append(item)
    normal_barrage = [item for item in normal_barrage if item]  # 去除空数据
    gift_barrage = [item for item in gift_barrage if item]      # 去除空数据
    hyObj.SaveToCSV('normal_barrage', ['username', 'time', 'msg'], normal_barrage)
    hyObj.SaveToCSV('gift_barrage', ['username', 'time', 'gift', 'num'], gift_barrage)
    sys.exit(0)

if __name__ == '__main__':  # 执行层
    # 信号监听
    signal.signal(signal.SIGTERM, QuitAndSave)
    signal.signal(signal.SIGINT, QuitAndSave)

    # 支持从命令行参数或交互输入房间号/URL
    if len(sys.argv) > 1:
        room_id = sys.argv[1]
    else:
        room_id = input("请输入房间ID或URL：").strip()
    # 支持输入完整URL或房间号
    if room_id.startswith("http"):
        room_id = room_id.rstrip('/').split('/')[-1]

    # 监听前清空csv文件内容（不保留表头）
    open('normal_barrage.csv', 'w', encoding='utf-8-sig').close()
    open('gift_barrage.csv', 'w', encoding='utf-8-sig').close()

    hyObj = HuyaLive(room_id)
    hyObj.Connect()
