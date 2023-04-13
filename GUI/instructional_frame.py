import customtkinter 

class InstructionalFrame(customtkinter.CTkFrame):
    """ This Class defines the Dialog Window for the UI. It displays the Entry widget, a Record
        button and the initial instruction message for the user, prompting to go to the Settings 
        menu and enter in the required data. 
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.row = 0 # Used for dialog box positioning
        self.message_count = 0
        
        # Holds the dialog_box instances to create the message flow
        self.dialog_frame = customtkinter.CTkScrollableFrame(master=self.master, fg_color=("#f7f7f8", "#343540"), width=1000, height=600)
        self.dialog_frame.grid(row=0, column=0, columnspan=3, rowspan=3, padx=(0,0), pady=(0,0))

    def body(self):
        """ This function creates the Insructional Frame to prompt the user to enter their 
            OpenAI Key path and Organization ID in the Settings menu. This frame will be deleted
            after the user sends the first message. """
        
        self.instruction_frame = customtkinter.CTkFrame(
            master=self.dialog_frame, 
            fg_color=("#ffffff", "#40414e"),
            border_color=("#e5e5e5", "#303138"),
            border_width=2,
            corner_radius=10
        )
        self.instruction_frame.grid(row=0, column=0, ipady=50, padx=(180,0), pady=(130,5))

        self.ChatGPT_Label = customtkinter.CTkLabel(
            master=self.instruction_frame, 
            text="ChatGPT",
            text_color=("#000000", "#cbcbcb"),
            font=("SF Display", 28),  
            corner_radius=10
        )
        self.ChatGPT_Label.grid(row=2, column=0, padx=(100,100), pady=(100,20))

        self.instruction1 = customtkinter.CTkLabel(
            master=self.instruction_frame, 
            text="- Press the Settings button and enter your OpenAI API Key Path and Organization ID",
            text_color="grey",
            font=("SF Display", 13),  
            corner_radius=10
        )
        self.instruction1.grid(row=3, column=0, padx=(50,50), pady=(20,0))

        self.instruction2 = customtkinter.CTkLabel(
            master=self.instruction_frame, 
            text="- Select your Audio API and Device",
            text_color="grey",
            font=("SF Display", 13),  
            corner_radius=10
        )
        self.instruction2.grid(row=4, column=0, padx=(50,50), pady=(5,0))

        self.instruction3 = customtkinter.CTkLabel(
            master=self.instruction_frame, 
            text="- Type or Record a question for ChatGPT",
            text_color="grey",
            font=("SF Display", 13),  
            corner_radius=10
        )
        self.instruction3.grid(row=5, column=0, padx=(50,50), pady=(5,0))