from pushbullet import Pushbullet
import requests
import ast
import websocket
from pprint import pprint
import threading
import time

def tts(message):
    import os
    print("Recognized speech by Google is {}".format(message))
    tts_command = "espeak -ven-uk+f3"
    return os.system(tts_command + ' "' + message + '" ')

class PushBulletNotifications(object):
    def __init__(self):
        pass

    def mirror(self):
        return

def mirror():
    API_key = "o.0uXY4V8zygueZLziiZcaXA18ldTldaSl"
    url = "https://api.pushbullet.com/v2/pushes?limit=1"
    headers = {'Access-Token': API_key}

    pb = Pushbullet(API_key)

    ws = websocket.create_connection("wss://stream.pushbullet.com/websocket/{}".format(API_key))

    while True:
        result = ws.recv()

        print(result)
        print(type(result))
        result = ast.literal_eval(result)

        if result["type"] == "tickle":
            print("Something recived!")
            r = requests.get(url, headers=headers)
            re = r.json()
            pprint(re)
            push = re['pushes']
            text = push[0]['body']
            name = push[0]['sender_name']
            tts("You have a new notification from {}. {} sent {}".format(name, name, text))

if __name__ == '__main__':

    thread = threading.Thread(target=mirror, args=())
    thread.daemon = True
    thread.start()
    for i in range(500):
        print(i*5)
        time.sleep(0.5)
