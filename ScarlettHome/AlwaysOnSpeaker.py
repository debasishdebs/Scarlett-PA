import speech_recognition as sr

from GreyMatter.SenseCells.tts import tts
from brain import brain


name = "Debasish"


class AlwaysOnSpeaker(object):
    def __init__(self):
        pass

    def listen_audio(self):
        r = sr.Recognizer()

        with sr.Microphone() as source:
            audio = r.listen(source)

        # threading.Thread(target=aos.start).start(a)
        # threading.Thread(target=sf.execute).start()

        try:
            recognized_audio = r.recognize_google(audio)

            return recognized_audio

        except sr.UnknownValueError:
            print("Couldn't recognize audio")

        except sr.RequestError as e:
            print("Couldn't request results from Google speech service : {}".format(e))

    def driver(self):
        tts("Hi. I'm Scarlett. How can I help you today?")

        recognized_audio = self.listen_audio()

        if "scarlett" or "Scarlett" in recognized_audio:
            tts("Yes {}, how can I help you?".format(name))

        recognized_audio = self.listen_audio()

        return recognized_audio

    def start(self):
        while True:
            recognized_audio = self.driver()

            ret = brain("Debasish", recognized_audio)
            if not ret:
                return ret

            return recognized_audio
        pass
