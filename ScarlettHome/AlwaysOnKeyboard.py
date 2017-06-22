from brain import brain

name = "Debasish"


class AlwaysOnKeyboard(object):
    def __init__(self):
        pass

    def listen_keyboard(self):
        message = raw_input("Hi {}. How can I help you?")
        return message

    def start(self):
        msg = self.listen_keyboard()
        ret = brain(name, msg)

        if not ret:
            return ret

        return msg