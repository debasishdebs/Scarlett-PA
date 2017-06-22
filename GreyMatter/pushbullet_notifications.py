from pushbullet import Pushbullet
import requests
import json
import websocket
import threading
import time
from GreyMatter.SenseCells.tts import tts
import creds as cr


def backup():
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
                                no_msg = eval(sender[i:i + 1])
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


class GetNotifications(object):
    """
    This class used Pushbullet API to read notification from my phone. 
    """
    def __init__(self):
        self.API_key = cr.PUSHBULLET_API_KEY
        self.url = cr.PUSHBULLET_URL
        self.websocket_url = cr.PUSHBULLET_WEBSOCKET_URL

        self.headers = {'Access-Token': self.API_key}
        pass

    def start(self):
        self.ws = self.__create_connection()
        self.pb = self.__create_pb_object()

        self.__mirror_notifications()

        pass

    def mirror(self):
        self.ws = self.__create_connection()
        self.pb = self.__create_pb_object()

        thread = threading.Thread(target=self.__mirror_notifications, args=())
        thread.daemon = True
        thread.start()
        i = 0
        while True:
            print(i)
            time.sleep(0.5)
            i += 1

    def __create_connection(self):
        ws = websocket.create_connection(self.websocket_url.format(self.API_key))
        return ws

    def __create_pb_object(self):
        pb = Pushbullet(self.API_key)
        return pb

    def __speak_(self, msg):
        tts(msg)
        pass

    def __mirror_notifications(self):
        while True:
            result = self.ws.recv()

            result = json.loads(result)

            if result["type"] == "tickle":
                r = requests.get(self.url, headers=self.headers)
                re = r.json()

                push = re['pushes']
                text = push[0]['body']
                name = push[0]['sender_name']
                msg = "You have a new notification from {}. {} sent {}".format(name, name, text)
                self.__speak_(msg)

            elif result['type'] == 'push' and result['push']['type'] != 'dismissal':
                push = result['push']
                application = push['application_name']
                text = push['body']
                sender = push['title']

                # Clean title
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
                                no_msg = eval(sender[i:i + 1])
                            except:
                                no_msg = eval(sender[i])
                            break
                    else:
                        name += sender[i]
                if no_msg == 0:
                    no_msg = 1
                # print(name, no_msg, text, application)

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
                self.__speak_(msg)
                pass


if __name__ == '__main__':

    # thread = threading.Thread(target=mirror, args=())
    # thread.daemon = True
    # thread.start()
    # for i in range(500):
    #     print(i*5)
    #     time.sleep(0.5)
    obj = GetNotifications()
    obj.mirror()
