import queue
import customtkinter 
import tkinter as tk

from main import *
from GUI.dialog_window_frame import *
from GUI.sidebar_frame import *
from GUI.settings_frame import *


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("A Conversation with ChatGPT")
        self.geometry(f"{1300}x{700}")
        self.minsize(1300, 750)

        # Set the app icon
        img = tk.Image("photo", file="assets/img/appicon.png")
        self.tk.call('wm','iconphoto', self._w, img)

        # Adds a slight alpha/transparency to the background
        self.attributes("-alpha", 0.99) 

        # Sets the default appearance
        self.load_appearance()

        # Configures the entire UI grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Content
        self.content_frame = customtkinter.CTkFrame(master=self.master, fg_color=("#f7f7f8", "#343540"))
        self.content_frame.grid(row=0, rowspan= 3, column=1, padx=(0,0), pady=(0, 0), sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_propagate(True)

        # Create Class Instances 
        self.settings = SettingsWindow(master=self)
        self.content = DialogWindow(self.content_frame)
        self.sidebar = Sidebar(master=self)
        
        self.build_dialog()  # Create the Dialog Window
        self.build_sidebar() # Create the Sidebar

    def build_sidebar(self):
        self.sidebar.build_sidebar()

    def build_settings(self):
        self.settings.build_settings()

    def build_dialog(self):
        self.content.mainloop()

    def get_api_key(self):
        openai_api_keypath = self.settings.api_key.get()
        return openai_api_keypath
        
    def get_org_id(self):
        openai_organizationid = self.settings.organization.get()
        return openai_organizationid

    def load_appearance(self):
        try:
            print("GUI - Loading Settings from settings.json")
            # This reads the settings.json files
            with open("Data/settings.json", "r") as openfile:
                # Reading from json file
                json_object = json.load(openfile)

                customtkinter.set_appearance_mode(json_object['Appearance'])
                openfile.close()

        except Exception as e:
            print(e)
            logging.error(e)
            customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"

if __name__ == "__main__":
    app = App()
    app.focus_set()
    app.mainloop()