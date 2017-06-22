from brain import brain


class ScarlettFunctionality(object):
    def __init__(self, message=None):
        self.message = message
        pass

    def execute_message(self, message):
        self.message = message
        pass

    def execute(self):
        msg = self.message
        try:
            brain("Debasish", msg)
            return True
        except:
            return False
        pass
