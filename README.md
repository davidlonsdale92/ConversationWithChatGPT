<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/documentation/App_icon_dark.png">
    <img src="./assets/documentation/App_icon_light.png">
  </picture>
</p>

---
This is a Text-To-Speech and Speech-To-Text interface for ChatGPT, capable of communicating via text or voice input!

![](assets/documentation/app.png)
| _Light and Dark mode support_

## Installation
Install the required packages with pip:
```
python -m pip install -r Setup/requirements.txt
```
Then run:
```
python3 main.py
```

## Setup
This app relies on the OpenAI API and ElevenLabs Voice API for full functionality.

- Sign up for an OpenAI Account and register for the API [here](https://openai.com/blog/openai-api)

- Sign up for an ElevenLabs Account and register for the API [here](https://beta.elevenlabs.io/sign-up)

The OpenAI API keypath and Organization ID are delcared through the UI by selecting the settings button. Here you can also choose which audio device you'd prefer to use. 

Right now the ElevenLabs API key must be hardcoded directly in the stt.py and tts.py files. This will be changed in a future update.

## Support
This application has only been tested using macOS with Apple Silicon. CustomTKinter does support both MacOS and Windows, though some issues may occur through use on other platforms. 

---
Go check out the official repo for [CustomTKinter](https://github.com/TomSchimansky/CustomTkinter#readme) and see what else the package can do.
