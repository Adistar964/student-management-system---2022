from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import sqlite3

conn = sqlite3.connect("students.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def display_student(student):
    r = Toplevel()
    r.geometry("500x500")
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
    options = list(student.keys())
    options.pop(0)
    print(options)
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
    Label(r, text="Student Management System", font=Font(underline=True)).pack(pady=20)
    Label(r, text="").pack(pady=30)
    Label(r, text="Student Operations: ", font=Font(underline=True)).pack(pady=10)
    ops = ["create","search","update","delete"]
    for i in ops:
        Button(r, text=i+" student", command=lambda i=i:adm_no_win(i)).pack(pady=10)
    Label(r, text="User Operations: ", font=Font(underline=True)).pack(pady=10)
    Button(r, text="Log-out").pack(pady=10)
    r.mainloop()

main_win()