""" 
A Conversation with ChatGPT

This application provides the user and ChatGPT an interface for audible interaction. 
"""

import sounddevice as sd
import soundfile as sf

from GUI.gui import *


class Controller(): 
    def __init__(self):
        app = App()
        app.mainloop()

if __name__ == "__main__":
    controller = Controller()
