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

def update_student(info):
    r = Toplevel()
    r.resizable(0,0)
    data = list(info.keys())
    admission_number = info["admission_number"]
    def update():
        try:
            value = value_of_menu.get().replace(" ","_")
            cur.execute(f"UPDATE students SET {value}='{input.get()}' WHERE admission_number={admission_number}")
            conn.commit()
            messagebox.showinfo("updated!", "successfully updated the student")
            r.destroy()
        except Exception as e:
            print(e)
            messagebox.showerror("error!", "wrong data entered!")
    for idx,i in enumerate(data):
        data[idx] = i.replace("_", " ")
    value_of_menu = StringVar(r)
    value_of_menu.set(data[0])
    input=Entry(r, font=Font(size=12))
    input.insert(0,info["name"])
    def change_inp(e):
        input.delete(0, END)
        input.insert(0,info[e.replace(" ", "_")])
    menu = OptionMenu(r, value_of_menu, *data, command=change_inp)
    menu.config(font=Font(size=12))
    menu.grid(row=0, column=0, pady=15,ipady=15, ipadx=40)
    input.grid(row=0, column=1, pady=15, ipady=15, padx=10, ipadx=50)
    Button(r, command=update,text="update", bg="green", fg="white", font=Font(size=12)).grid(row=1,columnspan=2,column=0, ipadx=20, ipady=15, pady=12)
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