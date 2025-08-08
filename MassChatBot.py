import json
import random
from gtts import gTTS
import pygame
import time
import os
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
from PIL import Image, ImageTk  # pip install pillow

# Load dialogues JSON
with open("dialogues.json", "r", encoding="utf-8") as f:
    dialogues = json.load(f)

mood_keywords = {
    "mass": ["mass", "attitude", "hero", "power"],
    "comedy": ["funny", "comedy", "joke", "laugh", "haasyam", "chirikkuka"],
    "romantic": ["love", "romantic", "pranayam", "sneham"],
    "emotional": ["sad", "emotional", "dukkham", "thot"],
    "trending": ["trending", "viral", "popular"],
    "pickup line": ["pickup", "flirt", "romantic", "witty"]
}

def detect_mood(user_input):
    user_input = user_input.lower()
    for mood, keywords in mood_keywords.items():
        for kw in keywords:
            if kw in user_input:
                return mood
    return "mass"

def pick_dialogue(mood_tag):
    filtered = [d["text"] for d in dialogues if mood_tag in d["tags"]]
    if not filtered:
        filtered = [d["text"] for d in dialogues]
    return random.choice(filtered)

def speak_manglish(text):
    tts = gTTS(text=text, lang='en')
    filename = "reply.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    time.sleep(0.2)
    os.remove(filename)

def insert_message(text_widget, sender, message):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, "\n")

    if sender == "user":
        tag_name = "right"
        display_text = f"You:\n{message}\n"
    else:
        tag_name = "left"
        display_text = f"Bot:\n{message}\n"

    text_widget.insert(tk.END, display_text, tag_name)
    text_widget.config(state=tk.DISABLED)
    text_widget.see(tk.END)

def on_enter(event=None):
    user_text = entry.get().strip()
    if user_text == "":
        return

    entry.delete(0, tk.END)

    insert_message(chat_window, "user", user_text)

    mood = detect_mood(user_text)
    reply = pick_dialogue(mood)

    insert_message(chat_window, "bot", reply)

    threading.Thread(target=speak_manglish, args=(reply,), daemon=True).start()

root = tk.Tk()
root.title("Malayalam Manglish Dialogue Bot")
root.geometry("800x700")
root.configure(bg="#ADD8E6")  # Light blue background

# Left image
left_img_raw = Image.open("left_image.png").resize((100, 600))
left_img = ImageTk.PhotoImage(left_img_raw)
left_label = tk.Label(root, image=left_img, bg="#ADD8E6")
left_label.place(x=10, y=50)

# Right image
right_img_raw = Image.open("right_image.png").resize((100, 600))
right_img = ImageTk.PhotoImage(right_img_raw)
right_label = tk.Label(root, image=right_img, bg="#ADD8E6")
right_label.place(x=690, y=50)

# Frame for chat and input (shifted left)
main_frame = tk.Frame(root, bg="#ADD8E6")
main_frame.place(x=120, y=20, width=560, height=660)

chat_window = scrolledtext.ScrolledText(main_frame, state='disabled', wrap=tk.WORD,
                                        font=("Helvetica", 14), bg="#CFEFFF", fg="black",
                                        padx=15, pady=15, borderwidth=0, highlightthickness=0)
chat_window.pack(padx=5, pady=(5,10), fill=tk.BOTH, expand=True)

chat_window.tag_configure("right", justify="right", foreground="#064273", font=("Helvetica", 14, "bold"))
chat_window.tag_configure("left", justify="left", foreground="#000000", font=("Helvetica", 14))

# Style for rounded Entry using ttk
style = ttk.Style()
style.theme_use('clam')

# Rounded Entry doesn't exist natively; workaround: use padding and flat border
style.configure("RoundedEntry.TEntry",
                foreground="black",
                fieldbackground="#CFEFFF",
                background="#CFEFFF",
                borderwidth=0,
                relief="flat",
                padding=10,
                font=("Helvetica", 16))

entry = ttk.Entry(main_frame, style="RoundedEntry.TEntry", justify="center")
entry.pack(padx=50, pady=(0,20), fill=tk.X, ipady=12)
entry.focus()

entry.bind("<Return>", on_enter)

root.mainloop()
