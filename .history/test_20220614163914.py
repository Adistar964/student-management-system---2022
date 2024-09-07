from tkinter import *
import sqlite3
from tkinter.messagebox import MessageBox
from tkinter.font import Font

con = sqlite3.connect("students.db")
cur = con.cursor()
