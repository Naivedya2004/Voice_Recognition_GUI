import tkinter as tk
from tkinter import ttk, scrolledtext
import speech_recognition as sr
import pyttsx3
import threading
import queue
from tkinter import font as tkfont

class VoiceRecognitionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recognition Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=10)
        self.text_font = tkfont.Font(family="Helvetica", size=10)
        
        
        self.create_widgets()
        
        
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
    def create_widgets(self):
        
        main_container = ttk.Frame(self.root, padding="20")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(0, weight=1)
        
        
        title_label = ttk.Label(
            main_container,
            text="Voice Recognition Assistant",
            font=self.title_font,
            foreground='#2c3e50'
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        
        text_frame = ttk.Frame(main_container)
        text_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=self.text_font,
            bg='white',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        
    
        self.start_button = tk.Button(
            button_frame,
            text="Start Listening",
            command=self.toggle_listening,
            font=self.button_font,
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=5
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.clear_button = tk.Button(
            button_frame,
            text="Clear Text",
            command=self.clear_text,
            font=self.button_font,
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=5
        )
        self.clear_button.grid(row=0, column=1, padx=5)
        
        
        self.status_label = ttk.Label(
            main_container,
            text="Ready",
            font=self.button_font,
            foreground='#7f8c8d'
        )
        self.status_label.grid(row=3, column=0, columnspan=2)
        
        
        self.start_button.bind('<Enter>', lambda e: self.start_button.config(bg='#2980b9'))
        self.start_button.bind('<Leave>', lambda e: self.start_button.config(bg='#3498db'))
        self.clear_button.bind('<Enter>', lambda e: self.clear_button.config(bg='#7f8c8d'))
        self.clear_button.bind('<Leave>', lambda e: self.clear_button.config(bg='#95a5a6'))
        
    def toggle_listening(self):
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
            
    def start_listening(self):
        self.is_listening = True
        self.start_button.config(text="Stop Listening")
        self.status_label.config(text="Listening...", foreground='#27ae60')
        
        
        threading.Thread(target=self.listen_for_speech, daemon=True).start()
        
    def stop_listening(self):
        self.is_listening = False
        self.start_button.config(text="Start Listening")
        self.status_label.config(text="Ready", foreground='#7f8c8d')
        
    def listen_for_speech(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    self.audio_queue.put(audio)
                except sr.WaitTimeoutError:
                    continue
                except Exception as e:
                    print(f"Error: {e}")
                    break
                    
        
        while not self.audio_queue.empty():
            audio = self.audio_queue.get()
            try:
                text = self.recognizer.recognize_google(audio)
                self.text_area.insert(tk.END, text + "\n")
                self.text_area.see(tk.END)  # Auto-scroll to the bottom
            except sr.UnknownValueError:
                self.text_area.insert(tk.END, "Could not understand audio\n")
                self.text_area.see(tk.END)
            except sr.RequestError as e:
                self.text_area.insert(tk.END, f"Could not request results; {e}\n")
                self.text_area.see(tk.END)
                
    def clear_text(self):
        self.text_area.delete(1.0, tk.END)
        self.status_label.config(text="Text cleared", foreground='#7f8c8d')

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecognitionGUI(root)
    root.mainloop() 