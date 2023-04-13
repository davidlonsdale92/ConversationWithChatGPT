import os
import time
import json
import openai
import threading
import logging
import sounddevice as sd
import speech_recognition as sr

from elevenlabslib import *


user = ElevenLabsUser("bf3bd6be6e10215b39f8a5d2393a55cf")
voice = user.get_voices_by_name("Rachel")[0]  # This is a list because multiple voices can have the same name

message = "Hello Roy and Jack. This is the voice I'm using for my ChatGPT Conversation app."

voice.generate_and_play_audio(message, playInBackground=False)

for historyItem in user.get_history_items():
    if historyItem.text == "Test.":
        # The first items are the newest, so we can stop as soon as we find one.
        historyItem.delete()
        break
