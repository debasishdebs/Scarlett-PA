import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
	print("Say something!")
	audio = r.listen(source)

try:
	recognized_speech = r.recognize_google(audio)
except sr.UnknownValueError:
	print("Couldn't recognize audio")
except sr.RequestError as e:
	print("Couldn't request resuls from Google speech service : {}".format(e))

print("Google recognized the speech you said as : {} ".format(recognized_speech))


with open("recording.wav", "wb") as f:
	f.write(audio.get_wav_data())
