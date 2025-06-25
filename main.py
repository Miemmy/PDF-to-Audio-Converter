from gtts import gTTS
import fitz  # PyMuPDF
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygame


last_output_path = ""
is_playing="False"

def choose_file():
    file_path=filedialog.askopenfilename(
                title="Select PDF File",
                filetypes=[("PDF files",".pdf")])

    if file_path:
        selected_file.set(file_path)
        status_label.config(text="Selected: " + os.path.basename(file_path))


def read_and_extract(pdf_path):
    try:
        file=fitz.open(pdf_path)
        text=""
        for page in file:
            text+=page.get_text()

        return text
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read PDF: {str(e)}")
        return None

def convert_to_audio(text, output_file):
    try:
        tts=gTTS(text,lang="en",slow=False)
        tts.save(output_file)
        return True
    except Exception as e :
        messagebox.showerror("Error", f"Conversion failed: {str(e)}")
        return False
def pdf_to_audio():
    pdf_path=selected_file.get()
    if not pdf_path:
        messagebox.showwarning("No File", "Please select a PDF file first.")
        return None
    status_label.config(text="Extracting text........")
    text=read_and_extract(pdf_path)
    if not text:
        messagebox.showwarning("Empty PDF", "No readable text found.")
        return
    output_name=os.path.splitext(pdf_path)[0] + "_audio.mp3"


    global last_output_path
    last_output_path = output_name# making this global so it won't be annoying as an argument for playsound when i need to make it a default command for the play button



    status_label.config(text="Converting to audio...")
    success = convert_to_audio(text, output_name)

    if success:
        messagebox.showinfo("Success", f"Audio saved as:\n{output_name}")
        status_label.config(text="Conversion complete!")
def play_audio():
    global is_playing

    try:
        if not last_output_path or not os.path.exists(last_output_path):
            messagebox.showwarning("Audio Not Found", "No audio file has been created yet.")
            return

        if not is_playing:
            pygame.mixer.music.load(last_output_path)
            pygame.mixer.music.play()
            play_btn.config(text="Pause Audio")
            is_playing = True
        else:
            pygame.mixer.music.pause()
            play_btn.config(text="Play Audio")
            is_playing = False

    except Exception as e:
        messagebox.showerror("Error", f"Failed to play/pause audio: {str(e)}")
    ...
# --- GUI Setup ---
root = tk.Tk()
root.title("AudioPDF Converter")
root.geometry("550x400")
root.configure(bg="#FFE6F0")
root.resizable(True, True)

pygame.mixer.init()


selected_file = tk.StringVar()

title = tk.Label(root, text="PDF to Audio Converter🎧", font=("Comic Sans MS", 20,"bold"),fg="#7A4E76",bg="#FFE6F0")
title.pack(pady=15)


select_btn = tk.Button(root, text="Choose PDF File", command=choose_file, width=25,bg="#7A4E76")
select_btn.pack(pady=5)

convert_btn = tk.Button(root, text="Convert to Audio", command=pdf_to_audio, width=25,bg="white")
convert_btn.pack(pady=10)

footer = tk.Label(root, text="Built by Uzor Jemima", font=("Monotype Corsiva", 8), bg="white")
footer.pack(side="bottom", pady=10)

status_label = tk.Label(root, text="No file selected.", bg="#9C6B98")
status_label.pack(pady=10)

play_btn = tk.Button(root, text="Play Audio🎶",font=("Comic Sans Ms",16,"bold"),command=play_audio, width=25, bg="#9C6B98", )
play_btn.pack(pady=5)



root.mainloop()