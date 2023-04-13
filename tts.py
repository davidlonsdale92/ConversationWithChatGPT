import sounddevice as sd
import speech_recognition as sr

from elevenlabslib import *


class TextToSpeech():

    def __init__(self):
        pass

    def play_response(self, message):
        user = ElevenLabsUser("INSERTELEVENLABSAPIKEYHERE")
        voice = user.get_voices_by_name("Rachel")[0]  # This is a list because multiple voices can have the same name

        voice.generate_and_play_audio(message, playInBackground=False)

        for historyItem in user.get_history_items():
            if historyItem.text == "Test.":
                # The first items are the newest, so we can stop as soon as we find one.
                historyItem.delete()
                break
