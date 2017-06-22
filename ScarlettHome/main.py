from AlwaysOnSpeaker import AlwaysOnSpeaker
from AlwaysOnKeyboard import AlwaysOnKeyboard
from ScarlettFunctionality import ScarlettFunctionality
from GreyMatter.pushbullet_notifications import GetNotifications

import threading


class ScarlettHome(object):
    def __init__(self):
        pass

    def start_home(self):
        prompt = raw_input("Enter 1 to interact using voice, else 2 for keyboard!")
        prompt = int(prompt)
        if prompt == 1:
            aos = AlwaysOnSpeaker()
        else:
            aos = AlwaysOnKeyboard()

        sf = ScarlettFunctionality()

        flag = True
        while flag:
            r1 = aos.start()

            if r1 is not False:
                sf.execute_message(r1)
                r2 = sf.execute()

            flag = r1 & r2

        # threading.Thread(target=aos.start).start(a)
        # threading.Thread(target=sf.execute).start()
        pass

    def start_notification_mirror(self):
        notif = GetNotifications()
        notif.start()
        pass

    def start(self):
        try:
            threading.Thread(target=self.start_notification_mirror).start()
            threading.Thread(target=self.start_home).start()
        except Exception as e:
            raise Exception("Error occured as {}".format(eval(str(e))))
        pass

if __name__ == '__main__':
    obj = ScarlettHome()
    obj.start()
