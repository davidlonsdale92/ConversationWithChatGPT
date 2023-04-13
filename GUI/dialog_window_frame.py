import time
import queue
import threading
import contextlib
import numpy as np
import customtkinter
import sounddevice as sd
import soundfile as sf
import tkinter as tk

from PIL import Image
from GUI.dialog_box_widget import *
from GUI.instructional_frame import *
from GUI.settings_frame import *
from stt import *


class DialogWindow(customtkinter.CTkFrame):
    """ 
    This Class defines the Dialog Window for the UI. It displays the Entry widget, a Record
    button and the initial instruction message for the user, prompting to go to the Settings 
    menu and enter in the required data. 
    """

    stream = None

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.row = 0            # Used for dialog box positioning
        self.message_count = 0  # Used for determining if the instructional frame needs to be destroyed
        self.line_height = 0    # Used for setting line height of the entry widget while typing
        
        # Holds the dialog_box instances to create the message flow
        self.dialog_frame = customtkinter.CTkScrollableFrame(master=self.master, fg_color=("#f7f7f8", "#343540"), width=1000, height=650)
        self.dialog_frame.grid(row=0, column=0, columnspan=3, rowspan=3, padx=(0,0), pady=(0,0))

        # Create Class instances
        self.message_box = DialogBox(self.dialog_frame)
        self.stt = SpeechToText()
        
        # Create the Message Entry widget
        self.message_entry() 

        # Create the Instructional Frame
        self.instructions = InstructionalFrame(self.dialog_frame)
        self.instructions.body()

        # Variables needed for recording audio
        self.create_stream()
        self.filename = ''
        self.input_overflows = 0
        self.recording = self.previously_recording = False
        self.audio_q = queue.Queue()
        self.peak = 0
        self.metering_q = queue.Queue(maxsize=1)
        
    def message_entry(self):
        self.rec_icon = customtkinter.CTkImage(
            light_image=Image.open("assets/img/record_icon.png"),
            dark_image=Image.open("assets/img/record_icon.png"),
            size=(22, 22)
        )
        
        self.record_button = customtkinter.CTkButton(
            master=self.master, 
            text=None,
            image=self.rec_icon, 
            font=("SF Display", 10), 
            command=self.on_rec,
            fg_color="#0e8568", 
            hover_color="#095140",
            corner_radius=10
        )
        self.record_button.grid(row=3, column=0, ipady=12, ipadx=20, padx=(85,10), pady=(20,0))

        # TODO: Add scrollbar functionality to the entry widget
        self.entry = customtkinter.CTkTextbox(
            master=self.master, 
            height=10,
            font=("SF Display", 14), 
            fg_color=("#ffffff", "#40414e"),
            text_color=("#000000", "#cbcbcb"),
            border_color=("#e5e5e5", "#303138"),
            border_width=2,
            corner_radius=10,
            wrap="word"
        )
        self.entry.grid(row=3, column=1, columnspan=2, ipadx=320, ipady=10, padx=(0, 85), pady=(20, 0))
        self.entry.insert(0.0, "Send a message...") # Placeholder text
            
        self.send_icon = customtkinter.CTkImage(
            light_image=Image.open("assets/img/send_icon_light.png"),
            dark_image=Image.open("assets/img/send_icon_dark.png"),
            size=(20, 20)
        )

        self.icon_label = customtkinter.CTkLabel(
            text=None,
            master=self.entry,
            image=self.send_icon,
        )
        # self.icon_label.place(relx=1.0, rely=0.2, x=-20, y=3, anchor='ne')
        self.icon_label.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=(5,0))

        # Bind keys to entry widget
        self.entry.bind('<Return>', self.get_text_message)
        self.entry.bind('<Key>', lambda event: self.change_entry_height(event))
        self.entry.bind('<BackSpace>', lambda event: self.change_entry_height(event))
        self.entry.bind('<Shift-Return>', lambda event: self.new_line(event))
        self.entry.bind('<FocusIn>', lambda event: self.clear_textbox(event))

        self.label = customtkinter.CTkButton(
            master=self.master, 
            text="This application is in no way affiliated with OpenAI and is intended only "
                 "as a third party interface using the OpenAI API.",
            font=("SF Display", 10),  
            fg_color="transparent"
        )
        self.label.grid(row=4, column=0, columnspan=3, padx=(5,20), pady=(5,5))
        self.label.configure(state='disabled')

    def clear_textbox(self, event):
        """ 
        Used to clear the placeholder text as bind events are currently broken in customtkinter.
        """
        # FIXME: Prevent this from firing when focus is lost on the application
        self.entry.delete("0.0", tk.END)
        self.entry.configure(height=10)
        self.entry.unbind('<FocusIn>')
    
    # TODO: THIS DOES NOT WORK AS IT SHOULD 
    def change_entry_height(self, event):
        line_width = 121  
        message = self.entry.get(0.0, "end-1c")  # Get the value from self.entry, minus the newline character at the end
        num_lines = (len(message) // line_width) + 1  # Calculate the number of lines based on the line width
        current_ipady = int(self.entry.grid_info()['ipady'])  # Get the current value of ipady

        entry_height = int(num_lines) + int(current_ipady)

        if num_lines == 1:
            # Decrease the number of lines by decreasing the value of ipady
            print("num_lines == 1")
            self.entry.grid_configure(ipady=10)

        elif num_lines > self.line_height and current_ipady <= 140:
            # Increase the number of lines by increasing the value of ipady
            print(f"num_lines {num_lines} > self.line_height {self.line_height}")
            self.line_height += 1
            self.entry.grid_configure(ipady=entry_height)

        elif num_lines < self.line_height and current_ipady >= 10:
            # Decrease the number of lines by decreasing the value of ipady
            print("num_lines < current_ipady")
            print(f"num_lines {num_lines} > current_ipady {current_ipady}")
            self.entry.grid_configure(ipady=current_ipady - 1)
    
    def new_line(self, *args):
        """ Used to prevent the <Return> event from firing if the Shift key is pressed """
        pass

    def get_text_message(self, event):
        message = self.entry.get(0.0, "end") # Get the value from self.entry
        print(f"get_text_message: {message}")
        self.create_user_message(message)

    def create_user_message(self, message):
        try:
            print(f"\ncreate_user_message: {message} \n")
             # Delete the InstructionalFrame after the first message is sent. 
            if self.message_count == 0:
                self.message_count += 1
                for widget in self.dialog_frame.winfo_children():
                    widget.destroy()
                self.instructions.destroy()

            # TODO: Check if the OpenAI Key/OrgID are entered, if not, auto respond back with a DialogBox explaining what to do 
            # if self.master.get_api_key() == '' and self.master.get_org_id() == '':
            #     print("This works!")

            message = message.strip("\n") # Remove any trailing whitespace
            lines =  len(message) 
            num_lines = (lines // 60) + 1 # adjust based on your desired line width

            # FIXME: Marker goes to the second line of the textbox after entry.delete()
            # Clear the message in self.entry 
            print("Deleting entry contents")
            self.entry.delete("0.0", tk.END)
            self.entry.mark_set(tk.INSERT, "0.0")
            self.entry.see("0.0")

            current_index = self.entry.index(tk.INSERT)
            print(f"current_index: {current_index}")
            self.entry.configure(height=10)

            # FIXME: This is a temporary fix for the row counter not 
            # FIXME: incrementing after the self.after functions below.
            row = self.row
            self.row += 1

            # Initialize flags for thread completion status
            self.user_dialog_complete = False
            self.stt_complete = False
            self.display_response_complete = False 
            self.response_complete = False
            
            # Delayed execution of the user_dialog, stt and response_message functions
            self.after(0, lambda: self.message_box.user_dialog(row, message))
            self.after(100, lambda: self.call_stt_thread(message))

            # FIXME: Application will crash during this execution
            try:
                self.after(200, lambda: self.response_dialog_thread())
            except Exception as e:
                self.message_box.error_dialog(self.row)
                self.row += 1
                print(e)
                logging.error(e)

        except Exception as e:
            print(e)
            logging.error(e)
    
    def user_dialog_thread(self, message):
        try:
            print(f"user_dialog_thread - sending message: {message}")
            self.message_box.user_dialog(self.row, message)
            self.user_dialog_complete = True

        except Exception as e:
            self.message_box.error_dialog(self.row)
            self.row += 1
            print(e)
            logging.error(e)
    
    def call_stt_thread(self, message):
        try:
            self.stt.send_to_api(message)
            self.stt_complete = True
        except Exception as e:
            print(e)
            logging.error(e)

    def response_dialog_thread(self):
        try:
            message = self.stt.get_response()
            self.message_box.response_dialog(self.row, message)
            self.display_response_complete = True

            self.row += 1 # Increase the row count for the next DialogBox instance

            # FIXME: Marker goes to the second line of the textbox after entry.delete()
            self.entry.delete("0.0", tk.END)
            self.entry.configure(height=10)

            # self.after(100, lambda: self.play_response_thread())
        except Exception as e:
            self.message_box.error_dialog(self.row)
            self.row += 1
            print(e)
            logging.error(e)
    
    def play_response_thread(self):
        try:
            self.stt.play_response()
        except Exception as e:
            self.message_box.error_dialog(self.row)
            self.row += 1
            print(e)
            logging.error(e)

    def wait_for_threads(self):
        # Use update() and idle() to allow the main thread to process events
        # and prevent the GUI from freezing while waiting for the functions to complete
        while not (self.user_dialog_complete and self.stt_complete):
            self.update()
            self.idle()

    # Record button function
    def on_rec(self):
        """ 
        This function is called when the Record button is pressed. The Entry widget is destroyed and replaced
        with an input monitor widget and the Record button text changes to "Send Message". 
        """
        self.recording = True

        # Replace the Entry Widget with the Input Monitor Widget
        self.entry.destroy()
        self.record_button.destroy()

        self.button_frame = customtkinter.CTkFrame(master=self.master, fg_color="transparent")
        self.button_frame.grid(row=3, column=0, padx=(0,10), pady=(20,0))

        self.stop_button = customtkinter.CTkButton(master=self.button_frame, 
                                            text="Back to Text",
                                            font=("SF Display", 10), 
                                            width=8,
                                            command=self.switch_to_text,
                                            fg_color="#0e8568", 
                                            hover_color="#095140",
                                            corner_radius=10)
        self.stop_button.grid(row=0, column=0, ipady=5, ipadx=10, padx=(100,10), pady=(20,20))

        self.record_button = customtkinter.CTkButton(master=self.button_frame, 
                                                    text="Send Message",
                                                    font=("SF Display", 10), 
                                                    width=8,
                                                    command=self.on_stop,
                                                    fg_color="#0e8568", 
                                                    hover_color="#095140",
                                                    corner_radius=10)
        self.record_button.grid(row=0, column=1, ipady=5, ipadx=7, padx=(0,0), pady=(20,20))

        # Input Monitor
        progress_var = customtkinter.DoubleVar()   

        self.input_monitor = customtkinter.CTkProgressBar(self.master, 
                                                        orientation="horizontal", 
                                                        mode='determinate', 
                                                        variable=progress_var, width=00,
                                                        progress_color="#0e8568")
        self.input_monitor.grid(row=3, column=1, columnspan=2, ipadx=280, ipady=5, padx=(0,150), pady=(20,0))

        # Callback function to update the Input Monitor
        self.update_gui()  

        self.filename = 'Data/Audio/message.wav'

        if os.path.exists(self.filename):
            os.remove('Data/Audio/message.wav')

        if self.audio_q.qsize() != 0:
            print('WARNING: Queue not empty!')
            print(f"self.audio_q Size: {self.audio_q.qsize()}")

        print(f"self.audio_q Size: {self.audio_q.qsize()}")
        self.file_thread = threading.Thread(
            target=self.file_writing_thread,
            kwargs=dict(
                file=self.filename,
                mode='x',
                samplerate=int(self.stream.samplerate),
                channels=self.stream.channels,
                q=self.audio_q,
            )
        )
        self.file_thread.start()

    def update_gui(self):
        """ 
        This function is used to update the input_monitor widget to display microphone input.
        """
        try: 
            peak = self.metering_q.get_nowait()
        except queue.Empty:
            pass
        else:
            if self.input_monitor.winfo_exists():
                self.input_monitor.set(peak)
        self.after(50, self.update_gui)

    def switch_to_text(self, *args):
        """ 
        This function is used to destroy the recording thread, preventing message submission 
        to the OpenAI API and revert back to to the Text Entry UI. 
        """
        try:
            self.recording = False

            self.wait_for_thread()

            # Replace the Input Monitor back with the Entry Widget
            self.stop_button.destroy()
            self.record_button.destroy()
            self.input_monitor.destroy()

            self.message_entry()

        except Exception as e:
            logging.error("An error occurred in switch_to_text: {}".format(e))

    def on_stop(self, *args):
        try:
            self.recording = False

            self.wait_for_thread()

            # Replace the Input Monitor back with the Entry Widget
            self.stop_button.destroy()
            self.record_button.destroy()
            self.input_monitor.destroy()
            self.message_entry()

            try:
                message = self.stt.convert_audio() # Returns transcribed message
                print(f"\n on_stop - self.stt.convert_audio(): {message} \n")
                self.create_user_message(message)

            except Exception as e:
                print(f"Error: {e}")
                logging.error(f"An error occurred in on_stop on sending message to create_user_message:{e}")
            
        except Exception as e:
            logging.error(f"An error occurred in on_stop: {e}")
    
    def file_writing_thread(self, *, q, **kwargs):
        with sf.SoundFile(**kwargs) as f:
            while True:
                data = q.get()
                if data is None:
                    break
                f.write(data)

    def create_stream(self, device=None):
        if self.stream is not None:
            self.stream.close()
        self.stream = sd.InputStream(
            device=device, channels=1, callback=self.audio_callback)
        self.stream.start()

    def audio_callback(self, indata, frames, time, _):
        """This is called (from a separate thread) for each audio block."""
        if self.recording:
            self.audio_q.put(indata.copy())
            self.previously_recording = True
        else:
            if self.previously_recording:
                self.audio_q.put(None)
                self.previously_recording = False

        self.peak = max(self.peak, np.max(np.abs(indata)))

        try:
            self.metering_q.put_nowait(self.peak)
        except queue.Full:
            pass
        else:
            self.peak = 0

    def wait_for_thread(self):
        try:
            self.after(10, self._wait_for_thread)
        except Exception as e:
            logging.error("An error occurred in wait_for_thread: {}".format(e))

    def _wait_for_thread(self):
        try:
            if self.file_thread.is_alive():
                self.wait_for_thread()
                return
            self.file_thread.join()
        except Exception as e:
            logging.error("An error occurred in _wait_for_thread: {}".format(e))

    def close_window(self):
        if self.recording:
            self.on_stop()
        self.destroy()
    