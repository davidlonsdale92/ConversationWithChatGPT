<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/documentation/App_icon_dark.png">
    <img src="./assets/documentation/App_icon_light.png">
  </picture>
</p>

---
This is a Text-To-Speech and Speech-To-Text interface for ChatGPT, capable of communicating via text or voice input!

<p align="center">
  <picture> 
    <img src="./assets/documentation/app.png" width="1400", height="500">
  </picture>
</p>

## Installation
Install the required packages with pip:
```
python -m pip install -r requirements.txt
```
Then run:
```
python3 main.py
```

## Setup
This app relies on the OpenAI API and ElevenLabs Voice API for full functionality.

Sign up for an OpenAI Account and register for the API [here](https://openai.com/blog/openai-api)

Sign up for an ElevenLabs Account and register for the API [here](https://beta.elevenlabs.io/sign-up)

Right now, the ElevenLabs API key must be declared directly from within the sst.py and tts.py files. This will be changed in a future update.

---
Go check out the official repo for [customtkinter](https://github.com/TomSchimansky/CustomTkinter#readme) and see what else the package can do.
