from SenseCells.tts import tts
import random
import json, requests


def who_are_you():

    messages = ["Hi! I'm Scarlett, your own personal assistant! I'm self learning, and you to-do task list will keep on increasing!",
                "Scarlett! Didn't I tell you before?",
                "Scarlett! Didn't I tell you before? You are very forgetting!",
                "You ask that so many times! I'm Scarlett!"]

    tts(random.choice(messages))

    pass

def undefined(message):
    print("The text is {}".format(message))
    tts("I dont know what that means!")

    pass

def how_am_i():
    messages = ["You are very handsome!",
                "You look very good and smart",
                "My kneews go weak when I see you.",
                "Damn, I cant believe you are real, for you are that sexy!"]

    tts(random.choice(messages))

    pass

def tell_joke():
    messages = ["What happends to a frogs car when it breaks down? It gets toad away!",
                "No, I always forget the punch line!",
                "What do I look to you? A Joker! I'm no joker! Fuck off and don't ask for a joke! Haha just kidding, shoot right away another one!"]

    url = "http://api.icndb.com/jokes/random"

    resp = requests.get(url)
    # print(resp.content.decode())
    try:
        data = resp.json()
    except ValueError:
        data = random.choice(messages)
    # data = json.loads(resp.text)
    #
    # print(data)

    tts(data)

    pass

def who_am_i(name):
    message = "You are {}, my boss, and Scarlett is you own assistant!"
    tts(message)
    pass

def where_born():
    message = "I was created by Debasish, a magician who brought me to life, in India! While Smoking and chilling in Himalayas!"
    tts(message)
    pass

def how_are_you():
    message = "I'm fine. Thank you! And you?"
    tts(message)
    pass

def how_am_myself_if_fine():
    message = "That's great to hear you are doing fine! How can I help you today?"
    tts(message)
    pass

def how_am_myself_not_fine():
    message = "Aww! Thats so sad. Whats bothering you? Is there anything I can fulfill to make you day good?"
    tts(message)
    pass
