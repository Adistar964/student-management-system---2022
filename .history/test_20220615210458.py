from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import sqlite3

conn = sqlite3.connect("students.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def delete_student(adm_no):
    cur.execute("DELETE FROM students WHERE admission_number="+adm_no)
    conn.commt()
    messagebox.showinfo("deleted student","successfuly deleted specified student entry!")

def display_student(student):
    r = Toplevel()
    r.geometry("500x500")
    r.resizable(0,0)
    labels = list(student.keys())
    labels.pop(0)
    for idx,i in enumerate(labels):
        labels[idx] = i.replace("_"," ")
    Label(r, text=student["name"]).pack()
    Label(r, text="").pack(pady=7)
    for i in labels:
        ent = Entry(r, font=Font(size=12))
        ent.insert(0,i+" : "+student[i.replace(" ","_")])
        ent.config(state="disabled")
        ent.pack(fill=X)
    r.mainloop()

def update_student(student):
    r = Toplevel()
    r.geometry("500x500")
    r.resizable(0,0)
    options = list(student.keys())
    options.pop(0)
    for idx,i in enumerate(options):
        options[idx] = i.replace("_"," ")
    Label(r, text="Update Student:").pack()
    Label(r,text="").pack(pady=7)
    def change_ent(e):
        ent.delete(0,END)
        ent.insert(0, student[e.replace(" ","_")])
    def do_update():
        cur.execute(f"UPDATE students SET {textVar.get().replace(' ','_')}='{ent.get()}'")
        conn.commit()
        r.destroy()
        messagebox.showinfo("Updated Student","Successfully Updated Student Entry!")
    f = Frame(r)
    ent = Entry(f, font=Font(size=10))
    ent.insert(0, student["name"])
    textVar = StringVar()
    textVar.set(options[0])
    OptionMenu(f,textVar,*options, command=change_ent).grid(row=0,column=0)
    ent.grid(row=0,column=1)
    f.pack()
    Button(r, text="Confirm", command=do_update).pack(ipady=15,ipadx=25,pady=10)
    r.mainloop()

def create_student():
    r = Toplevel()
    r.state("zoomed")
    r.resizable(0,0)
    cur.execute("SELECT * FROM students")
    conn.commit()
    student = cur.fetchone()
    labels = list(student.keys())
    labels.pop(0)
    for idx,i in enumerate(labels):
        labels[idx] = i.replace("_"," ")
    labels_3 = [labels[n:n+3] for n in range(0,len(labels),3)]
    Label(r, text="Create Student:", font=Font(size=23, weight="bold", underline=True)).pack()
    Label(r, text="").pack(pady=7)
    f = Frame(r)
    f.pack()
    ents = []
    def do_create():
        vals = []
        for i in ents:
            if len(i.strip() != 0):
                vals.append(i.get())
        if len(vals) != 17:
            messagebox.showerror("Error!", "All fields are mandatory!")
        else:
            cur.execute("""INSERT INTO students VALUES (
                NULL, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )""", tuple(vals))
            conn.commit()
            r.destroy()
            messagebox.showinfo("Added Student", "Successfully Added The Student!")
        
    for idx,i in enumerate(labels_3):
        for jdx,j in enumerate(i):
            fr = Frame(f)
            Label(fr, text=j, font=Font(size=12)).pack(pady=7)
            ent = Entry(fr, font=Font(size=14))
            ents.append(ent)
            ent.pack(ipady=10,ipadx=27)
            fr.grid(row=idx,column=jdx)
    Button(r, text="Create", bg="green", fg="white", command=do_create).pack(pady=10, ipady=15, ipadx=25)
    r.mainloop()


def op_win(op):
    r = Toplevel()
    r.geometry("500x500")
    r.resizable(0,0)
    Label(r, text="Enter Information:", font=Font(size=23, underline=True)).pack(pady=10)
    def do_op():
        if password.get() == "1234" and adm_no.get().isnumeric():
            cur.execute("SELECT * FROM students WHERE admission_number="+adm_no.get())
            conn.commit()
            data = cur.fetchone()
            if data:
                if op == "delete":
                    delete_student(dict(data)["admission_number"])
                if op == "update":
                    print("here")
                    update_student(dict(data))
                else:
                    display_student(dict(data))
        else:
            messagebox.showinfo("wrong data!","wrong data provided!")
    Label(r, text="Admission Number:", font=Font(size=12)).pack(pady=10)
    adm_no = Entry(r, font=Font(size=10))
    adm_no.pack(ipady=10,ipadx=20)
    Label(r, text="Your Password:", font=Font(size=12)).pack(pady=10)
    password = Entry(r, font=Font(size=10))
    password.pack(ipady=10,ipadx=20)
    Button(r, text="Confirm", bg="red", fg="white", command=do_op, font=Font(size=12)).pack(pady=15, ipady=15,ipadx=30)
    r.mainloop()

def main_window():
    r = Tk()
    r.geometry("700x700")
    r.resizable(0,0)
    Label(r, text="Student Management System:", font=Font(size=23, weight="bold")).pack(pady=15)
    Label(r, text="Student Operations:", font=Font(size=16, underline=True)).pack(pady=10)
    Button(r, bg="lightblue", fg="black",text="Create Student", font=Font(size=12), command=lambda:create_student()).pack(ipady=10,ipadx=17, pady=10)
    ops = ["Update","Search","Delete"]
    for i in ops:
        Button(r, bg="lightblue", fg="black",text=i+" Student", font=Font(size=12), command=lambda i=i:op_win(i)).pack(ipady=10,ipadx=17, pady=10)
    r.mainloop()

main_window()
