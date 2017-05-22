import os
import sys

def tts(message):
	print("Recognized speech by Google is {}".format(message))

	print("Sending it back to speech engine to hear back what was said!")

	tts_command = "espeak"

	return os.system(tts_command + ' "' + message + '" ')

tts("Hi, my name is Scarlett! How can I help you today?")
