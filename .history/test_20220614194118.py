from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import sqlite3

conn = sqlite3.connect("students.db")
cur = conn.cursor()
conn.row_factory = sqlite3.Row

def display_student(student):
    r = Toplevel()
    r.geometry("500x500")
    Label(r, text=student["name"].capitalize()).pack(pady=10)
    Label(r, text="").pack(pady=23)
    for i in student.keys():
        ent = Entry(r)
        ent.insert(i.replace("_", " ").capitalize() + " : " + student[i].capitalize())
        ent.config(state="disabled")
        ent.pack(pady=10)
    r.mainloop()