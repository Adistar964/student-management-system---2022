from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import sqlite3
from venv import main

conn = sqlite3.connect("students.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def display_student(student):
    r = Toplevel()
    r.geometry("500x500")
    r.resizable(0,0)
    Label(r, text=student["name"].capitalize(), font=Font(underline=True)).pack(pady=10)
    Label(r, text="").pack(pady=23)
    labels = list(student.keys())
    labels.pop(0)
    for i in labels:
        ent = Entry(r)
        ent.insert(0,i.replace("_", " ").capitalize() + " : " + student[i].capitalize())
        ent.config(state="disabled")
        ent.pack(pady=10)
    r.mainloop()

def delete_student(adm_no):
    cur.execute(f"DELETE FROM students WHERE admission_number={adm_no}")
    conn.commit()
    messagebox.showinfo("deleted student", "Successfully deleted the specified student entry!")

def update_student(student):
    r = Toplevel()
    labels = list(student.keys())
    labels.pop(0)
    for idx,i in enumerate(labels):
        labels[idx] = i.replace("_", " ")
    def change_entry(e):
        ent.delete(0,END)
        ent.insert(0,student[e.replace(' ','_')])
    def do_update():
        adm_no = student["admission_number"]
        cur.execute(f"UPDATE students SET {value.get().replace(' ','_')}='{ent.get()}' WHERE admission_number={adm_no}")
        conn.commit()
        r.destroy()
        messagebox.showinfo("success", "successfully updated the specified student entry")
    Label(r, text="Update Student").pack(pady=10)
    Label(r, text="").pack(pady=23)
    value = StringVar()
    value.set(labels[0])
    OptionMenu(r, value,*labels, command=change_entry).pack()
    ent = Entry(r)
    ent.insert(0,student["name"])
    ent.pack()
    Button(r, text="Update", command=do_update).pack()
    r.mainloop()

def adm_no_win(op):
    r = Toplevel()
    def do_op():
        if adm_no.get().isnumeric() and password.get() == "1234":
            cur.execute(f"SELECT * FROM students WHERE admission_number={adm_no.get()}")
            conn.commit()
            student = cur.fetchone()
            if student:
                if op == "delete":
                    delete_student(adm_no.get())
                elif op == "update":
                    update_student(dict(student))
                elif op == "search":
                    display_student(dict(student))
                else:
                    r.destroy()
                    messagebox.showerror("not", "nothinggg")
            else:
                r.destroy()
                messagebox.showerror("error","No Student with corresponding admission number found!")
        else:
            r.destroy()
            messagebox.showerror("error","Credentials provided were incorrect!")
    Label(r, text="Admission Number:").pack(pady=10)
    adm_no = Entry(r)
    adm_no.pack(pady=10)
    Label(r, text="Your Password:").pack(pady=10)
    password = Entry(r)
    password.pack()
    Button(r, text="Confirm", command=do_op).pack(pady=15)
    r.mainloop()

def main_win():
    r = Tk()
    r.geometry("700x700")
    r.resizable(0,0)
    def gotologin():
        answer = messagebox.askyesno("logout?", "Are you sure you want to logout?")
        if answer == True:
            r.destroy()
            login_win()
    Label(r, text="Student Management System", font=Font(underline=True)).pack(pady=20)
    Label(r, text="").pack(pady=30)
    Label(r, text="Student Operations: ", font=Font(underline=True)).pack(pady=10)
    ops = ["create","search","update","delete"]
    for i in ops:
        Button(r, text=i+" student", command=lambda i=i:adm_no_win(i)).pack(pady=10)
    Label(r, text="User Operations: ", font=Font(underline=True)).pack(pady=10)
    Button(r, text="Log-out", command=gotologin).pack(pady=10)
    r.mainloop()

def login_win():
    r = Tk()
    r.geometry("600x600")
    r.resizable(0,0)
    r.configure(bg="black")
    def login():
        if username.get() == "admin" and password.get() == "pass":
            r.destroy()
            main_win()
        else:
            messagebox.showerror("error", "Username or Password is incorrect!")
    Label(r, text="Admin Login", bg="black", fg="white",font=Font(underline=True, size=30)).pack(pady=10)
    Label(r, text="", bg="black").pack(pady=20)
    Label(r, text="Username", bg="black", fg="white", font=Font(size=17)).pack()
    username = Entry(r, font=Font(size=20))
    username.pack()
    Label(r, text="Password", bg="black", fg="white", font=Font(size=17)).pack()
    password = Entry(r, font=Font(size=20))
    password.pack()
    Button(r, text="login", command=login, bg="green",fg="white").pack(pady=20,ipady=15)
    r.mainloop()

login_win()