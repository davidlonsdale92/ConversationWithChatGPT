import os
import time
import json
import openai
import threading
import logging
import sounddevice as sd
import speech_recognition as sr

from elevenlabslib import *


class SpeechToText():

    def __init__(self):

        self.message = '' # Message defines the text entry message 
        self.response_message = ''
        self.audio_file = 'Data/Audio/message.wav' # audio_file defines the audio file to be converted to text

        self.openai_api_keypath = ''
        self.openai_organizationid = ''

        try:
            print("SpeechToText - Loading Settings from settings.json")

            self.filename = "Data/settings.json"

            # This reads the settings.json file
            with open(self.filename, "r") as openfile:
                # Reading from json file
                data = json.load(openfile)
                app_settings = data.get('App Settings', {})
                
                self.openai_api_keypath = app_settings['openai_api_keypath']
                self.openai_organizationid = app_settings['openai_organizationid']
                openfile.close()

        except Exception as e:
            print(e)
            logging.error(e)
    
    def convert_audio(self):
        # Speech to Text Function
        r = sr.Recognizer()                              
        with sr.AudioFile(self.audio_file) as source:
            audio = r.record(source)            
        message = r.recognize_google(audio)
        self.message = message = str(message)
        print(message)
        return message

    def send_to_dialog(self):
        print("Returning message to Dialog Window...")
        return self.message
        
    def send_to_api(self, message):
        openai.organization = self.openai_organizationid
        openai.api_key_path = self.openai_api_keypath
        openai.Model.list()

        print("Creating model and packing message...")
        # Example OpenAI Python library request
        MODEL = "gpt-3.5-turbo"
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[{"role": "user", "content": message}]
        )

        # Extract just the reply from the response object
        self.response_message = response['choices'][0]['message']['content']
        print(f"send_to_api: {self.response_message}")

        # Return the Response ID, used for the replay_audio function. 
        return response['id']

    def play_response(self):
        user = ElevenLabsUser("bf3bd6be6e10215b39f8a5d2393a55cf")
        voice = user.get_voices_by_name("Rachel")[0]  # This is a list because multiple voices can have the same name

        # voice.play_preview(playInBackground=False)
        voice.generate_and_play_audio(self.response_message, playInBackground=False)

        for historyItem in user.get_history_items():
            if historyItem.text == "Test.":
                # The first items are the newest, so we can stop as soon as we find one.
                historyItem.delete()
                break

    def get_message(self):
        print("Sending message back to Dialog Window...")
        return self.message
    
    def get_response(self):
        print("Sending response_message to Dialog Window...")
        return str(self.response_message)
    
if __name__ == "__main__":
    stt = SpeechToText()