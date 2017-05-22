from GreyMatter.SenseCells.tts import tts
import speech_recognition as sr
from brain import brain


def stt():
    tts("Hi! I'm Scarlett. How can I help you today?")
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        recognized_speech = r.recognize_google(audio)

        # tts(recognized_speech)

        return recognized_speech

    except sr.UnknownValueError:
        print("Couldn't recognize audio")
    except sr.RequestError as e:
        print("Couldn't request results from Google speech service : {}".format(e))


def main():
    speech = stt()
    brain("Debasish", speech)
    return

if __name__ == '__main__':
    main()
