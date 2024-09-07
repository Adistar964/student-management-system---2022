from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter.font import Font

con = sqlite3.connect("students.db")
cur = con.cursor()
con.row_factory = sqlite3.Row

def del_student(ad_no):
    try:
        cur.execute("DELETE FROM students WHERE admission_number=?",(int(ad_no),))
        con.commit()
        messagebox.showinfo("success", "successfully deleted the specified student entry")
    except:
        messagebox.showerror("error", "could not delete the student entry")

def update(student):
    r = Toplevel()
    def change_ent_data():
        inp.delete(0,END)
        inp.insert(0,student[strvar.get()])
    labels = list(dict(student).keys())
    labels.pop(0)
    strvar = StringVar()
    menu = OptionMenu(r, textvariable=strvar,*labels, command=change_ent_data)
    menu.grid(column=0,row=0)
    inp = Entry(r, font=Font(size=12))
    inp.grid(column=1, row=0)
    Button(r, text="Update", command=do_update)
    r.mainloop()

def op_menu(op):
    r = Toplevel()
    r.geometry("500x500")
    Label(r, text="Admission Number:").pack()
    def do_op():
        ad_no = admission_number.get()
        if ad_no.isnumeric() and password.get() == "1234":
            cur.execute("SELECT * FROM students WHERE admission_number=?",(ad_no,))
            data = cur.fetchone()
            if data:
                if op == "delete":
                    r.destroy()
                    del_student(ad_no)
                elif op == "update":
                    update(data)
            else:
                r.destroy()
                messagebox.showerror("error!", "Admission number does not esists!")
        else:
            r.destroy()
            messagebox.showerror("wrong data","Wrong data provided!")
    admission_number = Entry(r)
    admission_number.pack()
    Label(r, text="Your Password:").pack()
    password = Entry(r)
    password.pack()
    Button(r, text="Confirm", command=do_op).pack()
    r.mainloop()

def main_window():
    r = Tk()
    r.geometry("700x700")
    Label(r,text="Student Management System").pack()
    Label(r, text="Student Operations:").pack(pady=20)
    ops = ["create","update","search","delete"]
    def goto_op(i):
        op_menu(i)
    for i in ops:
        Button(r, text=i+" student", command=lambda:goto_op(i)).pack(pady=10)
    Label(r, text="User-Operations").pack(pady=10)
    Button(r, text="logout").pack(pady=10)
    r.mainloop()

main_window()