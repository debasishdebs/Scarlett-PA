import os
import sys
import speech_recognition as sr


def tts(message):
    print("Recognized speech by Google is {}".format(message))

    print("Sending it back to speech engine to hear back what was said!")

    tts_command = "espeak"

    return os.system(tts_command + ' "' + message + '" ')

def stt():
    tts("Hi! I'm Scarlett. How can I help you today?")
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        recognized_speech = r.recognize_google(audio)

        tts(recognized_speech)

    except sr.UnknownValueError:
        print("Couldn't recognize audio")
    except sr.RequestError as e:
        print("Couldn't request results from Google speech service : {}".format(e))

    return True

def main():
    stt()
    return

if __name__ == '__main__':
    main()
