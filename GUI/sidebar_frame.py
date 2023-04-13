import json
import sounddevice as sd
import soundfile as sf
import customtkinter
import logging 

from PIL import Image


class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        
        self.appearance = "Light"
        self.appearance_text = "Dark Mode"

        self.build_sidebar()
        self.load_appearance()

    def build_sidebar(self):
        # Creates the settings menu bar
        self.sidebar_frame = customtkinter.CTkFrame(master=self.master, corner_radius=0, width=300, fg_color="#202123")
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6)

        # Appearance Options
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, 
                                                            text="Appearance Mode:", 
                                                            text_color="#cbcbcb",
                                                            anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=(20,20), pady=(30,0))

        icon_image = customtkinter.CTkImage(light_image=Image.open("assets/img/light_dark.png"),
                            dark_image=Image.open("assets/img/light_dark.png"),
                            size=(20, 20))

        self.appearance_button = customtkinter.CTkButton(master=self.sidebar_frame, 
                                                        image=icon_image,
                                                        text=self.appearance_text,
                                                        textvariable=self.appearance,
                                                        command=self.set_appearance,
                                                        font=("SF Display", 10), 
                                                        text_color="#ffffff", 
                                                        fg_color="#0e8568", 
                                                        hover_color="#095140")
        self.appearance_button.grid(row=10, column=0, ipadx=20, padx=(20,20), pady=(0,10), sticky="s")

        # Settings
        self.settings_button = customtkinter.CTkButton(master=self.sidebar_frame, 
                                                    text="Settings", 
                                                    command=self.on_settings,
                                                    font=("SF Display", 10), 
                                                    text_color="#ffffff", 
                                                    fg_color="#0e8568", 
                                                    hover_color="#095140")
        self.settings_button.grid(row=11, column=0, ipadx=20, padx=(20,20), pady=(0,10), sticky="s")

    def set_appearance(self):
        if self.appearance == "Dark":
            self.appearance_text = "Dark Mode"
            self.appearance = "Light"
            self.save_appearance("Light")
        else:
            self.appearance_text = "Light Mode"
            self.appearance = "Dark"
            self.save_appearance("Dark")
        
        # FIXME: Bug in CustomTkinter prevents Appearance Button text from updating with configure method
        self.sidebar_frame.destroy()
        self.build_sidebar()
        customtkinter.set_appearance_mode(self.appearance)
    
    def load_appearance(self):
        try:
            print("Sidebar - Loading Settings from settings.json")
            # This reads the settings.json files
            with open("Data/settings.json", "r") as openfile:
                # Reading from json file
                json_object = json.load(openfile)

                self.appearance =json_object['Appearance']
                if self.appearance == "Dark":
                    self.appearance_text = "Dark Mode"
                else:
                    self.appearance_text = "Light Mode"
                openfile.close()

        except Exception as e:
            print(e)
            logging.error(e)
            customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"

    def save_appearance(self, appearance):
        # Check if settings.json exists, else log the error
        try:
            try:
                with open("Data/settings.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = {}

            data['Appearance'] = appearance

            with open("Data/settings.json", 'w') as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(e)
            logging.error(e)
            self.update_device_list()
    
    def on_settings(self):
        """ Changes the sidebar over to the Settings tab """
        self.master.build_settings()

        # try:
        #     if self.settings.result is not None:
        #         self.create_stream(device=self.settings.result)
        #     else:
        #         print("Settings window load failed.")
        # except Exception as e:
        #     print(e)