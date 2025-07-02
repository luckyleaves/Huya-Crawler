import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    # 假设弹幕消息结构如下（需抓包确认实际字段）
    print(data)
    if data.get('type') == 'chat':
        user = data['user']
        comment = {
            'nickname': user.get('nick', ''),
            'avatar': user.get('avatar', ''),
            'noble_type': user.get('nobleName', ''),
            'noble_level': user.get('nobleLevel', 0),
            'is_noble': user.get('nobleLevel', 0) > 0,
            'user_level': user.get('level', 0),
            'gender': user.get('gender', ''),
            'desc': user.get('intro', ''),
            'location': user.get('province', ''),
            'fans': user.get('fansCount', 0),
            'content': data.get('content', '')
        }
        print(comment)

def start_ws(room_id):
    # 伪地址，需用F12抓包获得真实ws地址和协议
    ws_url = f"wss://chat-ws.huya.com/{room_id}"
    ws = websocket.WebSocketApp(ws_url, on_message=on_message)
    ws.run_forever()

if __name__ == '__main__':
    start_ws('captainmo')