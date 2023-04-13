import customtkinter

from PIL import Image
from tts import *


class DialogBox(customtkinter.CTkFrame):
    """ 
    This class describes a Dialog Box, with both a user and response variant instances. The Dialog Box 
    contains a frame that wraps a label, textbox and a button together. 
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master
        self.id = 0   # Used by the ReplayAudio Class to determine which text to read

    def user_dialog(self, row, message):
        """ Creates a User Dialog textbox for conversation brevity. """

        print("Creating user_dialog box")

        self.dialogbox_frame = customtkinter.CTkFrame(master=self.master, fg_color=("#f7f7f8", "#343540"))
        self.dialogbox_frame.grid(row=row, column=0, columnspan=3, padx=(50,0), pady=(5,5))

        self.user = customtkinter.CTkButton(master=self.dialogbox_frame, 
                                            text="You",
                                            font=("SF Display", 14),  
                                            fg_color="transparent")
        self.user.grid(row=0, column=0, padx=(0,75), pady=(5,0))
        self.user.configure(state='disabled')

        self.textbox = customtkinter.CTkLabel(
            master=self.dialogbox_frame, 
            text=message,
            width=800,
            wraplength=800,
            anchor="w",
            justify="left",
            font=("SF Display", 14),  
            fg_color=("#ffffff", "#40414e"),
            text_color=("#000000", "#cbcbcb"),
            corner_radius=8
        )
        self.textbox.grid(row=1, column=0, ipady=10, padx=(30,100), pady=(5,5))

    def response_dialog(self, row, response):
        """ 
        Recieves the response back from the OpenAI API as messsage and displays it in the text frame. 
        This message will then be read out using the TextToSpeech Class. It can be replayed using the
        Replay Audio button calling the ReplayAudio Class. 
        """
        
        print("response_dialog Function")
        
        self.dialogbox_frame = customtkinter.CTkFrame(master=self.master, fg_color=("#f7f7f8", "#343540"))
        self.dialogbox_frame.grid(row=row, column=0, columnspan=3, padx=(50,0), pady=(5,5))

        icon_image = customtkinter.CTkImage(
            light_image=Image.open("assets/img/response_icon.png"),
            dark_image=Image.open("assets/img/response_icon.png"),
            size=(30, 30)
        )

        self.icon = customtkinter.CTkButton(
            master=self.dialogbox_frame, 
            text="ChatGPT",
            image=icon_image,
            font=("SF Display", 12),  
            fg_color="transparent"
        )
        self.icon.grid(row=0, column=0, padx=(0,75), pady=(5,0))
        self.icon.configure(state='disabled')

        self.textbox = customtkinter.CTkLabel(
            master=self.dialogbox_frame, 
            text=response,
            width=800,
            wraplength=800,
            anchor="w",
            justify="left",
            font=("SF Display", 14),  
            fg_color=("#ffffff", "#40414e"),
            text_color=("#000000", "#cbcbcb"),
            corner_radius=8
        )
        self.textbox.grid(row=1, column=0, ipady=10, padx=(30,100), pady=(5,5))

        self.replay_button = customtkinter.CTkButton(
            master=self.dialogbox_frame, 
            width=50,
            command=self.replay_audio,
            text="Replay Response", 
            font=("SF Display", 10), 
            text_color="#ffffff", 
            fg_color="#0e8568", 
            hover_color="#095140",
            corner_radius=5
        )
        self.replay_button.grid(row=2, column=0, ipady=5, ipadx=10, padx=(0,75), pady=(5,5))

    def error_dialog(self, row):
        """ 
        Displays the error message: "An error occured. If this issue persists please contact OpenAI at help.openai.com."
        If an error is thrown back from the OpenAI API.
        """
        
        print("error_dialog Function")
        
        self.dialogbox_frame = customtkinter.CTkFrame(master=self.master, fg_color=("#f7f7f8", "#343540"))
        self.dialogbox_frame.grid(row=row, column=0, columnspan=3, padx=(50,0), pady=(5,5))

        icon_image = customtkinter.CTkImage(
            light_image=Image.open("assets/img/error_icon_light.png"),
            dark_image=Image.open("assets/img/error_icon_dark.png"),
            size=(30, 30)
        )

        self.icon = customtkinter.CTkButton(
            master=self.dialogbox_frame, 
            text="ChatGPT",
            image=icon_image,
            font=("SF Display", 12),  
            fg_color="transparent"
        )
        self.icon.grid(row=0, column=0, padx=(30,20), pady=(5,0))
        self.icon.configure(state='disabled')

        self.textbox = customtkinter.CTkTextbox(
            master=self.dialogbox_frame, 
            height=10,  # set the height of the textbox to the lines entered in Entry
            font=("SF Display", 14),  
            fg_color=("#534450", "#534450"),
            text_color=("#000000", "#cbcbcb"),
            border_color=("#ae4348", "#ae4348"),
            border_width=2,
            activate_scrollbars=False,
            yscrollcommand=None,
            xscrollcommand=None,
            wrap="word",
            corner_radius=8
        )
        self.textbox.grid(row=1, column=0, ipadx=260, ipady=10, padx=(80,80), pady=(5,5))

        # Add the text from the Entry widget to the dialog box textbox
        self.textbox.insert(index="0.0", text="An error occured. If this issue persists please contact OpenAI at help.openai.com.")

        # Make the Text widget read-only
        self.textbox.configure(state='disabled')

    def replay_audio(self):
        print("replay_audio Function")
        # Get the message from the textbox for replay_audio
        message = self.textbox.cget("text")
        print(f"replay_audio: {message}")
        replay = TextToSpeech()
        replay.play_response(message)
