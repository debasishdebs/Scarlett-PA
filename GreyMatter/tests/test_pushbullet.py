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
    tts_command = "espeak -ven-us+f3"
    return os.system(tts_command + ' "' + message + '" ')


def mirror():
    import json
    API_key = "o.0uXY4V8zygueZLziiZcaXA18ldTldaSl"
    url = "https://api.pushbullet.com/v2/pushes?limit=1"
    headers = {'Access-Token': API_key}

    # pb = Pushbullet(API_key)

    ws = websocket.create_connection("wss://stream.pushbullet.com/websocket/{}".format(API_key))

    while True:
        result = ws.recv()

        # print(result)
        # print(type(result))
        # result = ast.literal_eval(result)
        result = json.loads(result)
        # print(result)
        pprint(result)
        print(type(result))

        if result["type"] == "tickle":
            r = requests.get(url, headers=headers)
            re = r.json()
            pprint(re)
            push = re['pushes']
            text = push[0]['body']
            name = push[0]['sender_name']
            tts("You have a new notification from {}. {} sent {}".format(name, name, text))

        elif result['type'] == 'push' and result['push']['type'] != 'dismissal':
            push = result['push']
            application = push['application_name']
            text = push['body']
            sender = push['title']

            # Clear title
            no_msg = 0
            name = ''
            for i in range(len(sender)):
                if sender[i] == '(' or sender[i] == ':':
                    if sender[i] == ':':
                        no_msg = 1
                        break
                    else:
                        i += 1
                        try:
                            no_msg = eval(sender[i:i+1])
                        except:
                            no_msg = eval(sender[i])
                        break
                else:
                    name += sender[i]
            if no_msg == 0:
                no_msg = 1
            print(name, no_msg, text, application)

            if 'call' in sender:
                # Incoming call handling
                by = push['body']
                msg = "You have an {} by {}".format(sender, by)
            else:
                # Incoming message handling. Tested for the following apps:
                # Whatsapp
                # Messenger
                msg = "You have {} new notification from {} by {}. {}".format(no_msg, application, name, text)
            print(msg)
            tts(msg)
            pass


if __name__ == '__main__':

    thread = threading.Thread(target=mirror, args=())
    thread.daemon = True
    thread.start()
    for i in range(500):
        print(i*5)
        time.sleep(0.5)
