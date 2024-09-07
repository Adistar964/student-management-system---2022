from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import sqlite3

# conn = sqlite3.connect("students.db")
# cur = conn.cursor()
# conn.row_factory = sqlite3.Row

# def display_student(student):
#     r = Toplevel()
#     r.geometry("500x500")
#     for i in student.keys():
#         Entry(r, text="d")
#     r.mainloop()
r = Tk()
Entry(r,text="hi",state="disabled").pack()
r.mainloop()