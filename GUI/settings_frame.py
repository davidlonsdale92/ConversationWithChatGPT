import os
import json
import contextlib
import sounddevice as sd
import soundfile as sf
import customtkinter
import logging


class SettingsWindow(customtkinter.CTkFrame):
    """ This is a Singleton class of the Settings Window. """
    __instance = None

    def __new__(cls, master=None, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

        self.filename = "Data/settings.json"

        self.hostapi_list_values = [hostapi['name'] for hostapi in sd.query_hostapis()]
        self.selected_device = customtkinter.StringVar()

        self.build_settings()

        self.hostapi_list_values = [hostapi['name'] for hostapi in sd.query_hostapis()]
        self.selected_device = customtkinter.StringVar()
        self.selected_device.trace('w', self.update_device_list)

  

    def build_settings(self):
        # Creates the settings menu bar
        self.sidebar_frame = customtkinter.CTkFrame(master=self.master, corner_radius=0, width=300, fg_color="#202123")
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6)

        self.back_button = customtkinter.CTkButton(master=self.sidebar_frame, 
                                                       text="Home", 
                                                       command=self.home,
                                                       font=("SF Display", 10), 
                                                       text_color="#ffffff", 
                                                       fg_color="#0e8568", 
                                                       hover_color="#095140")
        self.back_button.grid(row=0, column=0, ipadx=20, padx=(20,0), pady=(40,10), sticky="s")

        # OpenAI Organization Name
        self.api_org_label = customtkinter.CTkLabel(master=self.sidebar_frame, 
                                                    text='OpenAI Organization:', 
                                                    text_color=("#f7f7f8", "#343540"))
        self.api_org_label.grid(row=1, column=0, padx=(20,0), pady=(20,0))

        self.organization = customtkinter.CTkEntry(master=self.sidebar_frame, 
                                                   width=180,
                                                   placeholder_text="Enter your OpenAI Organization")
        self.organization.grid(row=2, column=0, padx=(20,0), pady=(5,0))

        # OpenAI API Key
        self.api_key_label = customtkinter.CTkLabel(master=self.sidebar_frame, 
                                                    text='OpenAI Key Path:',
                                                    text_color=("#f7f7f8", "#343540"))
        self.api_key_label.grid(row=3, column=0, padx=(20,0), pady=(10,0))

        self.api_key = customtkinter.CTkEntry(master=self.sidebar_frame,
                                              width=180,
                                              placeholder_text="Enter your OpenAI Key Path")
        self.api_key.grid(row=4, column=0, padx=(20,0), pady=(5,0))
    
        # Host Audio API
        self.hostapi = customtkinter.CTkLabel(master=self.sidebar_frame, 
                                              text='Select host API:',
                                              text_color=("#f7f7f8", "#343540"))
        self.hostapi.grid(row=5, column=0, padx=(20,0), pady=(20,0))

       
        self.hostapi_list = customtkinter.CTkComboBox(master=self.sidebar_frame, 
                                                      state='readonly', 
                                                      width=185, 
                                                      values= self.hostapi_list_values, 
                                                      variable=self.selected_device)
        self.hostapi_list.grid(row=6, column=0, padx=(20,0), pady=(5,5))

        with contextlib.suppress(sd.PortAudioError):
            self.hostapi_list.get()

        # Device
        self.device_ids = ['']
        self.device_settings = customtkinter.CTkLabel(master=self.sidebar_frame, 
                                                      text='Select sound device:',
                                                      text_color=("#f7f7f8", "#343540"))
        self.device_settings.grid(row=7, column=0, padx=(20,0), pady=(5,0))

        self.device_list = customtkinter.CTkComboBox(master=self.sidebar_frame, 
                                                     state='readonly', 
                                                     width=185, 
                                                     values=self.device_ids)
        self.device_list.grid(row=8, column=0, padx=(20,0), pady=(5,5))

        self.load_settings()

    def update_device_list(self, *args):
        print(f"update_device_list \n")

        # Query hostapis
        hostapis = sd.query_hostapis()

        # Create dictionary to store hostapi values
        hostapi_dict = {}

        # Populate hostapi_dict with key/values from hostapis
        for i, hostapi in enumerate(hostapis):
            name = hostapi['name']
            default_input_device = hostapi['default_input_device']
            default_output_device = hostapi['default_output_device']
            hostapi_dict[i] = {'name': name, 'default_input_device': default_input_device, 'default_output_device': default_output_device}

        logging.info(f"Host API Contents: {hostapi_dict}")

        self.hostapi_index = 0

        print(f"Host API Index: {self.hostapi_index}")
        logging.info(f"Host API Index: {self.hostapi_index}")

        hostapi = sd.query_hostapis(self.hostapi_index)

        self.device_ids = [
            idx
            for idx in hostapi['devices']
            if sd.query_devices(idx)['max_input_channels'] > 0]
        logging.info(f"device_ids {self.device_ids} \n")

        self.device_list.configure(values = [sd.query_devices(idx)['name'] for idx in self.device_ids])
        logging.info(f"device_list['values'] {self.device_list.get()} \n")

        default = hostapi['default_input_device']
        logging.info(f"default {default} \n")

    def validate(self):
        self.result = self.device_ids[int(self.device_list.cget())]
        return True
    
    def get_api_key(self):
        openai_api_keypath = self.api_key.get()
        return openai_api_keypath
        
    def get_org_id(self):
        openai_organizationid = self.organization.get()
        return openai_organizationid

    def load_settings(self):
        """ This should load the settings saved in the JSON file for repeated use. 
            To do this, the set method needs to be called against each CTk element that has a setting saved in the JSON file. 
        """
        # Check if settings.json exists, else log the error
        try:
            print("Settings - Loading Settings from settings.json")
            # This reads the settings.json file
            with open(self.filename, "r") as openfile:
                # Reading from json file
                data = json.load(openfile)
                app_settings = data.get('App Settings', {})
                
                self.api_key.insert(0, app_settings['openai_api_keypath'])
                self.organization.insert(0, app_settings['openai_organizationid'])
                self.hostapi_list.set(app_settings['hostapi'])
                self.device_list.set(app_settings['device_id'])

                openfile.close()

        except Exception as e:
            print(e)
            logging.error(e)
            self.update_device_list()

    def save_settings(self):
        """ This should save the settings to a JSON file for repeated use. """

        openai_api_keypath = self.api_key.get()
        openai_organizationid = self.organization.get()
        AudioAPI = self.hostapi_list.get()
        device_id = self.device_list.get()

        # Saves the users settings to be called back on next load.
        app_settings = {
            "openai_api_keypath": openai_api_keypath,
            "openai_organizationid": openai_organizationid,
            "hostapi": AudioAPI,
            "device_id": device_id
        }

        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                if app_settings is not None:
                    data['App Settings'].update(app_settings)
                return data
        except FileNotFoundError:
            data = {"App Settings": {}, "Appearance": "Dark"}
            if app_settings is not None:
                data['App Settings'].update(app_settings)
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)

    def home(self):
        """ Saves the settings and returns to the home menu. """
        self.save_settings()
        self.master.build_sidebar()
    