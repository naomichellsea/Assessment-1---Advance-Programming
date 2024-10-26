#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 22:07:37 2024

@author: naomichellsea
"""

""" 
Assessment 1 - Exercise 2
Your solution must be no more than 100 lines of code.
The randomJokes.txt file in the resources folder contains a dataset of random 
jokes. Each joke is on a new line and consists of a setup and 
punchline separated by a question mark. For example:
Why did the chicken cross the road?To get to the other side.
What happens if you boil a clown?You get a laughing stock.
Write a program that when prompted with the phrase "Alexa tell me a Joke" 
responds with a random joke from the dataset. 
The program should first present the setup then allow the user to enter a key to display the punchline.
The user should be able to continue requesting new jokes until they decide to quit the program.

98 lines of code without comments
I added functions of window photo, iconphoto, background sounds, hover buttons, emojis for excitemment etc.
"""

import tkinter as tk
from tkinter import messagebox
import random #to generate random values
from PIL import Image, ImageTk
import pygame  # Import pygame for audio playback

#main window
root = tk.Tk()
root.title("Joke Teller") #window title
root.geometry("600x600") #window size
root.iconphoto(False,ImageTk.PhotoImage(file = "/Users/naomichellsea/Advance Programming/iconph.jpg"))

image_path = "/Users/naomichellsea/Advance Programming/image.jpg"  
bg_img = Image.open(image_path)
bg_img = bg_img.resize((600, 600), Image.ANTIALIAS)  #resizing the image to fit in the window
bg_photo = ImageTk.PhotoImage(bg_img)

#creating canvas to place the image
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")  #image placed in canvas

#for background sounds
pygame.mixer.init()
#load the background sound from the file
pygame.mixer.music.load('/Users/naomichellsea/Advance Programming/112158__jobro__joke-drum-fill-03.wav')  


#function to load jokes from the existing file
def file_jokes(file_path):
    #"r" read rokes from the existing file provided
    with open(file_path, 'r') as file:
        funny = file.readlines()
    return [joke.strip() for joke in funny if joke.strip()]

funny = file_jokes('randomJokes.txt') #jokes file
points = 0  #the program is starting and no jokes are stated yet

#function to run and tell the jokes
def run_joke():
    global points
    #every 5 jokes, a message box that shows a fun fact will pop up to add excitement
    if points % 5 == 0 and points > 0:
        messagebox.showinfo("Fun Fact from Naomi", "💡 Fun Fact: Laughter and Smiling can make you age slower! So keep Smiling ;> ")
    
    #select random joke from the file
    joke = random.choice(funny)
    setup, jokeline = joke.split('?', 1)  #separate the joke line and set up label
    setup_label.config(text=f"🌟 Joke: {setup}?")  
    jokelinelabel.config(text="")  # Clear the previous data
    punchline_button.config(command=lambda: displaypunchline(jokeline))  #button command for punchline

def displaypunchline(jokeline):
    jokelinelabel.config(text=f"😂 Punchline: {jokeline}")  
    global points #use points globally that can be used across functions in these code.
    points += 1  #increase the jokes that has been said
    score_label.config(text=f"🎉 You've told {points} jokes so far! Make it more !! ")  #score label update
    pygame.mixer.music.play()  #jokeline background music

#quit the whole program
def quit_jokes():
    messagebox.showinfo("Goodbye ;< ", f"You told {points} jokes. Hope it was enjoyable ;> ")  #goodbye message box when quiting the program
    root.destroy()  

#each labels for start up, jokes, and scores
setup_label = tk.Label(root, text="Naomi's Joke Hub: Laugh Lab!", font=("Helvetica", 24, "bold"), bg="#fff1e6", fg="#ff99c8", borderwidth=0, relief="flat", padx=10, pady=10, wraplength=400)
setup_label.place(relx=0.55, rely=0.22, anchor="center")  

jokelinelabel = tk.Label(root, text="", font=("Helvetica", 18), bg="#fff1e6", fg="#333", borderwidth=0, relief="flat", padx=10, pady=10, wraplength=300)
jokelinelabel.place(relx=0.55, rely=0.35, anchor="center")  #aligning the position for the window layout

score_label = tk.Label(root, text="🎉 Zero jokes? Sounds like a punchline emergency!", font=("Helvetica", 16), bg="#fff1e6", fg="#333", borderwidth=0, relief="flat", padx=10, pady=10)
score_label.place(relx=0.55, rely=0.5, anchor="center") 


#extra functions for hover effect in buttons
def hover_enter(e):
    e.widget['bg'] = '#ef94d5'  #button background color when hovered
    e.widget['fg'] = '#6e44ff'  #text color when hovered

def hover_leave(e):
    e.widget['bg'] = '#d7b8f3'  # return button background color when not hovering
    e.widget['fg'] = '#f42272'  


button_frame = tk.Frame(root, bg="#f0f8ff")
button_frame.place(relx=0.55, rely=0.68, anchor="center")  

#buttons for disclosing jokes on the window
joke_button = tk.Button(button_frame, text="Tell me a joke ;p", command=run_joke, font=("Helvetica", 16),  borderwidth=2, relief="raised", padx=10, pady=5)
joke_button.pack(side=tk.LEFT, padx=5)  #allignment left for horizontal alignment
joke_button.bind("<Enter>", hover_enter) #implementing the def function of buttons when hovered using bind.
joke_button.bind("<Leave>", hover_leave)

punchline_button = tk.Button(button_frame, text="Show Punchline", command=lambda: None, font=("Helvetica", 16),  borderwidth=2, relief="raised", padx=10, pady=5)
punchline_button.pack(side=tk.LEFT, padx=5)
punchline_button.bind("<Enter>", hover_enter)
punchline_button.bind("<Leave>", hover_leave)

quit_button = tk.Button(button_frame, text="Quit ;<", command=quit_jokes, font=("Helvetica", 16),  borderwidth=2, relief="raised", padx=10, pady=5)
quit_button.pack(side=tk.LEFT, padx=5)
quit_button.bind("<Enter>", hover_enter) 
quit_button.bind("<Leave>", hover_leave) #implementing the def function of buttons when hovered using bind.


root.mainloop() #should always be at the end to run the whole code's function



