#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:06:39 2024

@author: naomichellsea
"""
"""
Assessment 1 - Exercise 1
We are asked to develop a program up to 250 lines of code that involves 
randomly generated numbers for 10 arithmetic questions.
Main features should include Menu Selection, Random Question Generation, 
Functions (ex. displayMenu, randomInt) and Play Again Option.

245 lines without comment lines
I added functions of welcome section, sounds, timer, pictures etc.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar #time bar 
import random #for random questions
import pygame #for background sounds
import time
from PIL import Image, ImageTk


class MathQuiz:
    TimeLimit = 15 #time limit for every question asked
    MaxQues = 10
    FirstScore = 10 #first correct points
    SecondScore = 5 #second correct points
    SkipLimit = 3 #3 maximum skips only

    def __init__(self, play):
        self.play = play
        self.play.title("Naomi's Quiz Time")
        self.difficulty = 1 #difficulty level
        self.current_question = 0 #current question number tracker
        self.score = 0 #increasing the score per question
        self.MaxQues = MathQuiz.MaxQues #max question limit from the class function
        self.num1 = 0
        self.num2 = 0
        self.correctanswer = 0
        self.operation = '' #operation for addition or subtraction
        self.timeend = MathQuiz.TimeLimit #setting the 15 secs time limit
        self.skipsend = MathQuiz.SkipLimit 
        self.timerplay = False
        self.timerrun = False

        pygame.mixer.init()
        self.correctsound = pygame.mixer.Sound("/Users/naomichellsea/Advance Programming/correct sound.wav")
        self.incorrectsound = pygame.mixer.Sound("/Users/naomichellsea/Advance Programming/incorrect sound.wav")

        #background color and size
        self.play.geometry("600x700")
        self.play.config(bg="#eff7f6") 

        self.image_label = None  # Variable to hold the image label
        self.setup_welcome()

        #List of image files from desktop corresponding to questions
        self.image_files = [
            "/Users/naomichellsea/Downloads/vecteezy_math-lesson-on-whiteboard-3d-icon-illustration_11421604.png",
            "/Users/naomichellsea/Downloads/vecteezy_3d-school-education-illustration-icon-caculator_10915727.png",
            "/Users/naomichellsea/Downloads/vecteezy_3d-illustration-of-ruler-school-education-icon_13721074.png",
            "/Users/naomichellsea/Downloads/vecteezy_3d-isolated-blue-calculator_11662957.png",
            "/Users/naomichellsea/Downloads/vecteezy_funny-pi-rate-pirate-pi-day-vintage-math-teacher_38969933.png",
            "/Users/naomichellsea/Downloads/vecteezy_3d-illustration-calculator-symbol-icon_22796305.png",
            "/Users/naomichellsea/Downloads/vecteezy_math-lesson-on-whiteboard-3d-icon-illustration_11421604.png",
            "/Users/naomichellsea/Downloads/vecteezy_funny-pi-rate-pirate-pi-day-vintage-math-teacher_38969931.png",
            "/Users/naomichellsea/Downloads/vecteezy_3d-illustration-calculator-symbol-icon_22796245.png",
            "/Users/naomichellsea/Downloads/vecteezy_colorful-numbers-pattern-symbol-math_19776513.png"
        ]

    def setup_welcome(self): #welcome window before starting the quiz
        self.clear_window()
        
        
        greeting = tk.Label(self.play, text="Welcome to Naomi's Math Quiz!", font=("Verdana", 24, "bold"), bg="#eff7f6", fg="#f2b5d4")
        greeting.pack(pady=20) #padding for alignment in the area
        
        username = tk.Label(self.play, text="Please enter your name:", font=("Verdana", 16), bg="#eff7f6", fg="#f2b5d4")
        username.pack(pady=10)
        
        self.name_entry = tk.Entry(self.play, font=("Georgia", 14), bg="#dcdde1", fg="#1e272e", bd=2, relief="groove")
        self.name_entry.pack(pady=10)
        
        #button to proceed to the next menu
        next_button = self.buttons("Next", self.setup_menu)
        next_button.pack(pady=20)

    def setup_menu(self): 
        user_name = self.name_entry.get()  #user's name to be inputed
        if not user_name.strip(): #check if user inputed their name
            messagebox.showwarning("Warning", "Please enter your name before proceeding.")
            return
        
        self.clear_window() #clear the window for selecting the level
        
        #setting up the difficulty level by user's option
        welcome = tk.Label(self.play, text=f"Hello, {user_name}! \n Please select your desired difficulty level.", font=("Verdana", 22, "bold"), bg="#eff7f6", fg="#9381ff")
        welcome.place(relx=0.5, rely=0.2, anchor='center')  #align it in the center
    
        #difficulty buttons for options
        button1 = self.buttons("Easy Peasy", lambda: self.set_difficulty(1))
        button1.config(height=2) #adjusting the button height
        button1.place(relx=0.5, rely=0.4, anchor='center')  #first button
    
        button2 = self.buttons("Moderate", lambda: self.set_difficulty(2))
        button2.config(height=2)
        button2.place(relx=0.5, rely=0.5, anchor='center')  #second button
    
        button3 = self.buttons("Brainy Mode", lambda: self.set_difficulty(3))
        button3.config(height=2)
        button3.place(relx=0.5, rely=0.6, anchor='center')  #third button

    def buttons(self, text, command): #styling the buttons using 
        button = tk.Button(self.play, text=text, command=command, width=20, bg="#9381ff", fg="#147df5", font=("Georgia", 14, "bold"), relief="groove", bd=3)
        #for hover effects in the button colours
        button.bind("<Enter>", lambda e: button.config(bg="#450920", fg="#da627d"))
        button.bind("<Leave>", lambda e: button.config(bg="#9381ff", fg="#147df5")) 
        button.place_configure(relx=0.5, rely=0.5, anchor='center')
        button.bind("<ButtonPress>", lambda e: button.config(bd=2, relief="sunken")) #when pressed effect
        button.bind("<ButtonRelease>", lambda e: button.config(bd=3, relief="groove")) #when released effect
        return button

    def set_difficulty(self, level):
        self.mode = level
        self.score = 0 #resetting the score
        self.current_question = 0
        self.skips = 0 #reset the skip count
        self.nextques() #moves to the next quetion

    def randomInt(self): #making random integer based on tbe difficulty level
        if self.mode == 1:
            return random.randint(1, 9) #easy first level 
        elif self.mode == 2:
            return random.randint(10, 99) #secomd intermediate level
        else:
            return random.randint(1000, 9999) #third hard mode level

    def decideOperation(self):
        return random.choice(['+', '-']) #randomly choose between operations of addition or subtraction

    def nextques(self):
        if self.current_question >= self.MaxQues: #checking if there are any repeated question
            self.show_results()
            return

        self.clear_window() 
        self.current_question += 1
        self.num1 = self.randomInt() #generating random first number
        self.num2 = self.randomInt() #generating random second number
        self.operation = self.decideOperation()
        self.correctanswer = self.num1 + self.num2 if self.operation == '+' else self.num1 - self.num2 #calculating the correct answer
        
        self.display_question_image()

        tk.Label(self.play, text=f"Question {self.current_question}/{self.MaxQues}", font=("Verdana", 16), bg="#eff7f6", fg="#ff6f61").pack(pady=10)
        per_question = tk.Label(self.play, text=f"{self.num1} {self.operation} {self.num2} = ?", font=("Georgia", 24, "bold"), bg="#eff7f6", fg="#ff6f61")
        per_question.pack(pady=10)

        self.answer = tk.Entry(self.play, font=("Georgia", 14), bg="#dcdde1", fg="#1e272e", bd=2, relief="groove")
        self.answer.pack(pady=10)

        self.buttons("Submit", self.check_answer).pack(pady=5) #button for submiting the answer
        self.buttons("Skip", self.skip_question).pack(pady=5)

        self.skipsection = tk.Label(self.play, text=f"Skips Left: {self.SkipLimit - self.skips}", font=("Verdana", 12), bg="#fdf0d5", fg="#ff6f61") #calculating how many skips are lef
        self.skipsection.pack(pady=10) #confirming the skip function to be able to function properly
        
        #progress bar for the time limit that is counting
        self.progresssection = Progressbar(self.play, orient=tk.HORIZONTAL, length=200, mode='determinate', maximum=self.timeend)
        self.progresssection.pack(pady=10)

        self.timer = tk.Label(self.play, text=f"Time left: {self.timeend} seconds", font=("Georgia", 12, "bold"), bg="#eff7f6", fg="#1e272e")
        self.timer.pack(pady=10) #running the timer 

        self.timing = MathQuiz.TimeLimit
        if not self.timerrun:
            self.update_timer()
            self.timerrun = True #setting the status of timer

        self.textani(per_question)

    def display_question_image(self):
        #display the image in every question
        if self.image_label:
            self.image_label.destroy()  #Remove the old image label
        
        try:
            image_path = self.image_files[self.current_question - 1]  # Index from 0
            image = Image.open(image_path)
            image = image.resize((300, 300), Image.ANTIALIAS) #image resizing 
            self.photo = ImageTk.PhotoImage(image)

            self.image_label = tk.Label(self.play, image=self.photo)
            self.image_label.pack(pady=20)
        except IndexError: #error handling if there are excess
            print("No more images to display for questions.")

    def check_answer(self):
        answer = self.answer.get() #getting user answer
        self.answer.delete(0, tk.END)
        if not answer:#check if the user interface is empty
            messagebox.showinfo("Error", "Please enter your answer!")
            return

        try:
            answer = int(answer) #converting the answer to number
        except ValueError: #error handling when user inputted invalid
            messagebox.showerror("Invalid Input", "Please enter a valid number!")
            return

        if answer == self.correctanswer: #answer correction section
            self.score += MathQuiz.FirstScore #score increasing every correct answer 10 points
            messagebox.showinfo("Correctieee! <3 ", f"Well Done! GOODJOB!! Your score is {self.score}.") #message box for notifying user
            self.nextques()
            self.correctsound.play() #play correct background sound
        else:
            self.score += MathQuiz.SecondScore #add score for correct answer for 5 points only for second question
            messagebox.showinfo("Wronggg!!", f"Oopsie poopsie! The correct answer was {self.correctanswer}. Your score is {self.score}.")
            self.nextques()
            self.incorrectsound.play() #play incorrect background sound

    def skip_question(self):
        if self.skips < self.SkipLimit: #checking if the skip limit is already over
            self.skips += 1 #increasing the skip count
            messagebox.showinfo("Skipped!", f"You skipped the question. Skips left: {self.SkipLimit - self.skips}.")
            self.nextques()
        else:
            messagebox.showinfo("Limit Reached", "You have reached the skip limit, Sorry ;< ")

    def show_results(self):
        self.clear_window()
        #show the final score at the end
        tk.Label(self.play, text=f"Your Final Score is: {self.score}", font=("Arial", 24, "bold"), bg="#eff7f6", fg="#b388eb").pack(pady=20)
        tk.Label(self.play, text="Thank you for playing! Hope you had a good one ;> ", font=("Verdana", 16), bg="#eff7f6", fg="#f1c0e8").pack(pady=10)
        self.create_button("Play Again", self.restart).pack(pady=20) 
        self.create_button("Exit", self.play.quit).pack(pady=5)

    def restart(self):
        self.clear_window()
        self.score = 0 #reset the score back to zero
        self.setup_welcome()

    def clear_window(self):
        for widget in self.play.winfo_children(): #iterate all the widgets in the window
            widget.destroy()

    def update_timer(self):
        if self.timing <= 0:
            self.check_answer()  # Treat no answer as incorrect
        else:
            self.timing -= 1 #decreasing the final limit
            self.timer.config(text=f"Time left: {self.timing} seconds")
            self.progresssection['value'] = MathQuiz.TimeLimit - self.timing
            self.play.after(1000, self.update_timer) #call the function again

    def textani(self, label):
        for i in range(1, 16): #colour change for 15 times
            label.config(fg="#ff6f61") #change the text colour
            label.update()
            time.sleep(0.5) #pause for half a second
            label.config(fg="#1e272e")
            label.update()
            time.sleep(0.5)

if __name__ == "__main__":
    root = tk.Tk()
    quiz = MathQuiz(root)
    root.mainloop()



        
        
        
        
        
        
        
        
        
                                                 
                                                 
                                                 
                                                 
                                                 
                                                 
                                                 