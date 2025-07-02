import sys
import subprocess
from usermessage import collect_huya_users

def get_room_info():
    # 先获取房间链接
    print("[INFO] 正在获取房间链接...")
    subprocess.run([sys.executable, "get_link.py"])
    # 获取主播信息
    print("[INFO] 正在获取主播链接...")
    subprocess.run([sys.executable, "get_Anchor_link.py"])
    print("[INFO] 正在获取主播信息...")
    subprocess.run([sys.executable, "get_Anchor.py"])
    # 获取房间详细信息
    print("[INFO] 正在获取房间详细信息...")
    subprocess.run([sys.executable, "huya_room_info_crawler.py"])
    subprocess.run([sys.executable, "csv_to_db1.py"])
def get_single_room_info(room_url):
    print(f"[INFO] 正在采集单个房间信息: {room_url}")
    subprocess.run([sys.executable, "huya_room_info_crawler.py", room_url])
    subprocess.run([sys.executable, "csv_to_db1.py"])
def listen_bulletscreen(room_id):
    print(f"[INFO] 正在监听房间 {room_id} 的弹幕...")
    subprocess.run([sys.executable, "huya_Bulletscreen.py", room_id])
    subprocess.run([sys.executable, "csv_to_db2.py"])
    subprocess.run([sys.executable, "csv_to_db3.py"])
def visualized_sqlite():
    subprocess.run([sys.executable, "data_visualizer.py"])
if __name__ == "__main__":
    while(1):
        print("请选择操作：")
        print("1. 获取全部房间信息")
        print("2. 获取所有房间10000条弹幕信息")
        print("3. 监听单个房间弹幕")
        print("4. 采集弹幕用户信息")
        print("5. 获取单个房间主播信息")
        print("6. 启动交互式可视化SQLite数据库")
        print("7. 退出")
        choice = input("输入数字选择功能：").strip()
        if choice == "1":
            get_room_info()
        elif choice == "3":
            room_url = input("请输入房间URL或房间ID：").strip()
            # 从URL中提取房间ID（假设URL格式为 https://www.huya.com/房间号）
            if room_url.startswith("http"):
                room_id = room_url.rstrip('/').split('/')[-1]
            else:
                room_id = room_url
            listen_bulletscreen(room_id)
        elif choice == "5":
            room_url = input("请输入房间URL：").strip()
            get_single_room_info(room_url)
        elif choice == "4":
            room_url = input("请输入房间URL或房间ID：").strip()
            if room_url.startswith("http"):
                room_id = room_url.rstrip('/').split('/')[-1]
            else:
                room_id = room_url
            duration = input("请输入采集时长（秒，默认30）：").strip()
            duration = int(duration) if duration.isdigit() else 30
            users = collect_huya_users(room_id, duration)
            print(f"[INFO] 共采集到 {len(users)} 个用户信息")
            for user in users:
                print(user)
        elif choice == "2":
            with open('room_links.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    room_url = line.strip()
                    if room_url:
                        print(f"[INFO] 正在采集房间 {room_url} 的10000条弹幕信息...")
                        listen_bulletscreen(room_url)
        elif choice == "6":
            visualized_sqlite()
        elif choice == "7":
            print("退出程序。")
            sys.exit(0)
        else:
            print("无效选择。")
