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
    Label(r, text=student["name"].capitalize(), font=Font(underline=True)).pack(pady=10)
    Label(r, text="").pack(pady=23)
    for i in student.keys():
        ent = Entry(r)
        ent.insert(i.replace("_", " ").capitalize() + " : " + student[i].capitalize())
        ent.config(state="disabled")
        ent.pack(pady=10)
    r.mainloop()

def delete_student(adm_no):
    cur.execute(f"DELETE FROM students WHERE admission_number={adm_no}")
    conn.commit()
    messagebox.showinfo("deleted student", "Successfully deleted the specified student entry!")

def update_student(student):
    r = Toplevel()
    options = student.keys()
    options.pop(0)
    def change_entry():
        ent.delete(0,END)
        ent.insert(0,student[value.get()])
    def do_update():
        adm_no = student["admission_number"]
        cur.execute(f"UPDATE students SET {value.get()}={ent.get()} WHERE admission_number={adm_no}")
        conn.commit()
        r.destroy()
        messagebox.showinfo("success", "successfully updated the specified student entry")
    Label(r, text="Update Student").pack(pady=10)
    Label(r, text="").pack(pady=23)
    value = StringVar()
    OptionMenu(r, textvariable=value,*options, command=change_entry)
    ent = Entry(r)
    ent.pack()
    Button(r, text="Update", command=do_update).pack()
    r.mainloop()