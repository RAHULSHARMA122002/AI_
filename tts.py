# tts.py
import pyttsx3

class SimpleTTS:
    def __init__(self):
        self.engine = pyttsx3.init()

    def say(self, text):  
        print(f"[TTS] Speaking: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

