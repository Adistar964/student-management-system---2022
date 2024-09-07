from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter.font import Font

con = sqlite3.connect("students.db")
cur = con.cursor()
con.row_factory = sqlite3.Row

def delete(ad_no):
    try:
        cur.execute("DELETE FROM students WHERE admission_number=?",(int(ad_no),))
        con.commit()
        messagebox.showinfo("success", "successfully deleted the specified student entry")
    except:
        messagebox.showerror("error", "could not delete the student entry")

def update(student):
    r = Toplevel()
    labels = student
    r.mainloop()

def op_menu(op):
    r = Toplevel()
    r.geometry("500x500")
    Label(r, text="Admission Number:").pack()
    def do_op():
        adn = 0
        if admission_number.get().isnumeric():
            adn = admission_number.get()
        else:
            adn = None
        cur.execute("SELECT * FROM students WHERE admission_number=?",(adn))
        data = cur.fetchone()
        if data and password == "1234":
            if op == "delete":
                r.destroy()
                delete(admission_number.get())
        elif password != "1234":
            messagebox.showerror("wrong password", "wrong password provided!")
        else:
            messagebox.showerror("wrong admission number","Wrong admission number provided!")
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