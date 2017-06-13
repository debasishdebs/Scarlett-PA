from datetime import datetime
from SenseCells.tts import tts


def what_is_time():
    tts("The time is {}".format(datetime.strftime(datetime.now(), "%H:%M")))
    pass