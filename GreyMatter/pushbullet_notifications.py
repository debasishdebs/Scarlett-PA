from pushbullet import Pushbullet
import requests
import ast
from pprint import pprint


API_key = "o.0uXY4V8zygueZLziiZcaXA18ldTldaSl"
url = "https://api.pushbullet.com/v2/pushes?limit=1"
url_2 = "https://api.pushbullet.com/v2/pushes?modified_after=0"
headers = {'Access-Token': API_key}

params = {'header': {
    'Access-Token': API_key,
    'content': 'application/json'
}}

pb = Pushbullet(API_key)

print(pb.devices)
motog = pb.devices[0]
push = motog.push_note("Hello! This is sample note", "We are using API")

pushes = pb.get_pushes()
print(pushes)

import websocket

ws = websocket.create_connection("wss://stream.pushbullet.com/websocket/{}".format(API_key))

while True:
    result = ws.recv()
    print(result, type(result))
    result = ast.literal_eval(result)
    print(result, type(result))
    print(50*"-")
    if result["type"] == "tickle":
        print("Something recived!")
        r = requests.get(url, headers=headers)
        re = r.json()
        pprint(re)