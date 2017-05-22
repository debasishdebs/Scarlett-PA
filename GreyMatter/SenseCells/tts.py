import os
import sys

def tts(message):
	tts_engine = "espeak"
	return os.system(tts_engine + ' "' + message + '" ')

tts("Hi, my name is Scarlett! How can I help you today?")
