#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:49:38 2024

@author: naomichellsea
"""

"""
Assessment 1 - Exercise 3
We are asked to make a program that is under 250 lines of code that uses the 
studentMarks.txt file that manages student marks that includes their marks and 
student codes. Functions should include: Menu Options of View All Records, 
View Individual Record, Highest Total Score, and Lowest Total Score.
Extension of Exercise 3 encourages a program up to 700 lines of code that has 
features of Sort Records, Add Record, Delete Record, Update Record. Plus, ensuring 
that all the changes must be reflected to the original file. (studentMarks.txt)

246 lines of code
I added functions of ttkbootstrap for the theme, search menu, dropdowns option, treeview
etc.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv #for reading and writing command seperated values
from ttkbootstrap import Style #import theme I used for UI Design

FileName = '/Users/naomichellsea/Advance Programming/studentMarks.txt'

class StudentList: #class that manages the student records
    def __init__(self, rec):
        self.rec = rec
        self.style = Style(theme='vapor') #theme application for the design (ttkboothstrap)
        self.rec.title("Naomi's Class Student Records")
        self.rec.geometry("900x600")
        self.rec.configure(bg="#F5F7FA")  #background colour that is different from the theme I used

        #main frame for the window
        nametitle = tk.Frame(self.rec, pady=10)
        nametitle.pack(fill=tk.X)

        namelabl = tk.Label(nametitle, text="Naomi's Student Records", font=("Helvetica", 24, "bold"))
        namelabl.pack()

        #frame for the buttons and the treeview (GUI widget for hierarchical structure)
        contentarea = tk.Frame(self.rec, bg="#ff0054")
        contentarea.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        #buttons menu
        buttonsarea = tk.Frame(contentarea)
        buttonsarea.pack(pady=10)

        all_buttons = [ #each buttons for their commands
            ("Display All Records", self.displayallstudent),
            ("Display Individual Record", self.displayperrecord),
            ("Highest Total Score", self.highestscore),
            ("Lowest Total Score", self.lowestscore)
        ]

        #each buttons for their theme colour and grid style
        for index, (text, command) in enumerate(all_buttons):
            btn = ttk.Button(buttonsarea, text=text, command=command, style="Secondary.TButton")
            btn.grid(row=index // 4, column=index % 4, padx=10, pady=10)

        
        searchbar = tk.Frame(contentarea, bg="#dee2ff")
        searchbar.pack(pady=10)

        self.search_content = ttk.Entry(searchbar, width=30, font=("Helvetica", 12))
        self.search_content.insert(0, "Search by student name") #placeholder text
        self.search_content.bind("<FocusIn>", self.empty_placehol)  #when pressed placeholder text will be removed
        self.search_content.bind("<FocusOut>", self.create_placehol) #will be restored if its not pressed
        self.search_content.bind("<KeyRelease>", self.search_coname)
        self.search_content.grid(row=0, column=0, padx=10)
        
        #search button for search section
        ttk.Button(searchbar, text="Search", command=self.search_onestu, width=8, style="Success.TButton").grid(row=0, column=1)
        #"success.tbutton" for the styling of button colour in applied theme

        # Dropdowns section
        self.organize = tk.StringVar(value="Sort everything by")
        sortselection = ["Total Marks", "Percentage", "Name"] #sorting options in dropdown menu
        self.sort_menu = ttk.OptionMenu(searchbar, self.organize, *sortselection, command=self.sortallstudents)
        self.sort_menu.grid(row=0, column=2, padx=10)

        self.sortgrade = tk.StringVar(value="Filter by Grade")
        organisegrade = ["Grade", "A", "B", "C", "D", "F"] #filtering for sorting by grade
        self.grade_menu = ttk.OptionMenu(searchbar, self.sortgrade, *organisegrade, command=self.arrangebygrade)
        self.grade_menu.grid(row=0, column=3, padx=10)

        #treeview widget section
        treewidget = tk.Frame(contentarea)
        treewidget.pack(pady=20, fill=tk.BOTH, expand=True)

        #each column headers in treeview widget
        self.tree = ttk.Treeview(treewidget, columns=("Code", "Name", "Total Marks", "Exam Marks", "Percentage", "Grade"), show="headings", height=15)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  #allow the widget to expand for extra spaces

        for col in ("Code", "Name", "Total Marks", "Exam Marks", "Percentage", "Grade"):
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, anchor='center', width=120) #width and allignment


        self.scrollbar = ttk.Scrollbar(treewidget, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set) #scrollbar within the treeview widget

        self.loadstudentfile() #loads the records of the student from the file

    def loadstudentfile(self):
        self.students = []
        try:
            with open(FileName, "r") as file: #"r" for reading the specified file
                reader = csv.reader(file)  #comma seperated values reader
                next(reader)  # Skip first line
                for row in reader:
                    code, name, *subjectmarks, examinationscore = row #unpack each record per row
                    total_marks = sum(map(int, subjectmarks)) + int(examinationscore)
                    percent = (total_marks / 160) * 100
                    grade = self.gradecalculation(percent)
                    self.students.append({
                        'code': code,
                        'name': name,
                        'total_marks': total_marks,
                        'exam_mark': int(examinationscore),
                        'percentage': percent,
                        'grade': grade
                    }) #append to the student list
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")

    def gradecalculation(self, percent):
        if percent >= 70: return 'A'
        if percent >= 60: return 'B'
        if percent >= 50: return 'C'
        if percent >= 40: return 'D'
        return 'F'

    def displayallstudent(self):
        self.tree.delete(*self.tree.get_children()) #clear existing records
        for student in self.students:
            self.tree.insert("", "end", values=(
                student['code'],
                student['name'],
                student['total_marks'],
                student['exam_mark'],
                f"{student['percentage']:.2f}%",
                student['grade']
            )) #add student informations in treeview widget

        studenttotal = len(self.students)
        #calculating average percentage of students
        avgpercent = sum(s['percentage'] for s in self.students) / studenttotal if studenttotal > 0 else 0
        summary = f"Total Students: {studenttotal}\nAverage Percentage: {avgpercent:.2f}%"
        messagebox.showinfo("Summary", summary) #output in the message box

    def displayperrecord(self):
        searchstu = simpledialog.askstring("Input", "Enter student name or code:") #prompt for search individual record
        student = next((s for s in self.students if s['name'].lower() == searchstu.lower() or s['code'] == searchstu), None) #seach the student

        if student: #deatils of students for displaying
            details = (
                f"Student Name: {student['name']}\n"
                f"Student Code: {student['code']}\n"
                f"Total Coursework Marks: {student['total_marks']}\n"
                f"Exam Marks: {student['exam_mark']}\n"
                f"Overall Percentage: {student['percentage']:.2f}%\n"
                f"Grade: {student['grade']}"
            )
            messagebox.showinfo("Student Record", details)
        else:
            messagebox.showinfo("No record", "Student not found.") #error message if there is no record found

    def highestscore(self):
        if not self.students:
            messagebox.showinfo("Info", "There are no records.")
            return
        self.tree.delete(*self.tree.get_children()) #remove existing records on display
        higheststu = max(self.students, key=lambda s: s['total_marks']) #find students with the highest total marks to display
        self.tree.insert("", "end", values=(
            higheststu['code'],
            higheststu['name'],
            higheststu['total_marks'],
            higheststu['exam_mark'],
            f"{higheststu['percentage']:.2f}%",
            higheststu['grade']
        ))

    def lowestscore(self):
        if not self.students:
            messagebox.showinfo("Info", "There are no records.")
            return
        self.tree.delete(*self.tree.get_children())
        loweststu = min(self.students, key=lambda s: s['total_marks']) #find students with the highest total marks to display
        self.tree.insert("", "end", values=(
            loweststu['code'],
            loweststu['name'],
            loweststu['total_marks'],
            loweststu['exam_mark'],
            f"{loweststu['percentage']:.2f}%",
            loweststu['grade']
        )) #insert lowest score in the treeview widget
        
    #get the input of user to search
    def search_onestu(self):
        search_name = self.search_content.get()
        #find the name that matches from the user input
        student = next((s for s in self.students if search_name.lower() in s['name'].lower()), None)
        if student:
            self.displayperrecord()
        else:
            messagebox.showinfo("No record", "Student not found.")

    def search_coname(self, event):
        search_name = self.search_content.get()
        #clear the current data on treeview widget
        self.tree.delete(*self.tree.get_children())
        for student in self.students:
            if search_name.lower() in student['name'].lower():
                #integrate the matching data
                self.tree.insert("", "end", values=(
                    student['code'],
                    student['name'],
                    student['total_marks'],
                    student['exam_mark'],
                    f"{student['percentage']:.2f}%",
                    student['grade']
                ))

    def sortallstudents(self, _):
        sorting = self.organize.get()
        #sort students based on the selected option on the dropdown menu
        if sorting == "Total Marks":
            self.students.sort(key=lambda s: s['total_marks'], reverse=True)
        elif sorting == "Percentage":
            self.students.sort(key=lambda s: s['percentage'], reverse=True)
        elif sorting == "Name":
            self.students.sort(key=lambda s: s['name'])
        self.displayallstudent()  #refresh the display to show the chosen criteria

    def arrangebygrade(self, _):
        filteredgrade = self.sortgrade.get()
        if filteredgrade == "Filter by Grade":
            self.displayallstudent()
            return
        #filter the students by selected grade
        filtered_students = [s for s in self.students if s['grade'] == filteredgrade]
        self.tree.delete(*self.tree.get_children())
        for student in filtered_students:
            self.tree.insert("", "end", values=(
                student['code'],
                student['name'],
                student['total_marks'],
                student['exam_mark'],
                f"{student['percentage']:.2f}%",
                student['grade']
            ))

    def empty_placehol(self, event): #clearing the placeholder when the user starts typing
        if self.search_content.get() == "Search by student name":
            self.search_content.delete(0, tk.END)

    def create_placehol(self, event): #restoring everything if its empty
        if not self.search_content.get():
            self.search_content.insert(0, "Search by student name")

root = tk.Tk()
app = StudentList(root)
root.mainloop()







