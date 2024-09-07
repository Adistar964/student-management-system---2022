from multiprocessing import Value
from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import sqlite3

conn = sqlite3.connect("students.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def delete_student(adm_no):
    cur.execute(f"DELETE FROM students WHERE admission_number={adm_no}")
    conn.commit()
    messagebox.showinfo("Student deleted", "successfully deleted the student entry!")

def display_student(student):
    r = Toplevel()
    Label(r, text=student["name"]).pack()
    Label(r,text="").pack(pady=15)
    keys = list(student.keys())
    keys.pop(0)
    labels = []
    for i in keys:
        labels.append(i)
    for i in labels:
        ent = Entry(r)
        ent.insert(0,i.replace("_"," ")+" : "+student[i])
        ent.config(state="disabled")
        ent.pack(fill=X)
    r.resizable(0,0)
    r.mainloop()

def update_student(student):
    keys = list(student.keys())
    keys.pop(0)
    labels = []
    for i in keys:
        labels.append(i.replace("_"," "))
    def change_entry(e):
        ent.delete(0,END)
        print(student[e.replace(" ","_")])
        ent.insert(0,student[e.replace(" ","_")])
    def do_update():
        cur.execute(f"UPDATE students SET {value_of_menu.get().replace(' ','_')}='{ent.get()}'")
        conn.commit()
        r.destroy()
        messagebox.showinfo("updated student", "successfully updated the student entry!")
    r = Toplevel()
    r.geometry("500x500")
    r.resizable(0,0)
    value_of_menu = StringVar()
    value_of_menu.set(labels[0])
    ent = Entry(r)
    ent.insert(0,student["name"])
    OptionMenu(r, value_of_menu, *labels, command=change_entry).pack()
    ent.pack()
    Button(r, text="Update", command=do_update).pack()
    r.mainloop()

def create_student():
    r = Toplevel()
    r.resizable(0,0)
    r.state("zoomed")
    fr = Frame(r)
    fr.pack()
    Label(fr, text="Create Student").grid(row=0,column=0,pady=10)
    # Label(r,text="").grid(pady=15)
    cur.execute("SELECT * FROM students")
    conn.commit()
    data = list(dict(cur.fetchone()).keys())
    data.pop(0)
    for idx,i in enumerate(data):
        data[idx] = i.replace("_"," ")
    labels = [data[n:n+3] for n in range(0,len(data),3)]
    ents = []
    def do_cr():
        ents_val = []
        for i in ents:
            ents_val.append(i.get())
        cur.execute("""INSERT INTO students VALUES(
                NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )""", tuple(ents_val))
        conn.commit()
        messagebox.showinfo("created student", "successfully created student entry!")
    for idx,i in enumerate(labels):
        for jdx,j in enumerate(i):
            frame = Frame(fr)
            Label(frame, text=j).pack(pady=10)
            ent = Entry(frame)
            ent.insert(0,"Asas")
            ents.append(ent)
            ent.pack()
            frame.grid(row=idx+1,column=jdx)
    Button(r, text="Create", command=do_cr).pack()
    r.mainloop()

def op_win(op):
    r = Toplevel()
    r.geometry("500x500")
    r.resizable(0,0)
    def do_op():
        if adm_no.get().isnumeric() and password.get() == "1234":
            cur.execute("SELECT * FROM students WHERE admission_number="+adm_no.get())
            conn.commit()
            data = cur.fetchone()
            if data:
                data_dict = dict(data)
                if op == "delete":
                    delete_student(data_dict["admission_number"])
                elif op == "update":
                    update_student(data_dict)
                elif op == "search":
                    display_student(data_dict)
                else:
                    print("Nothingg")
            else:
                r.destroy()
                messagebox.showerror("wrong admission number!","Wrong admission number provided!")
        else:
            r.destroy()
            messagebox.showerror("wrong data!","wrong data provided!")
    Label(r, text="Your Data:", font=Font(underline=True)).pack(pady=10)
    Label(r, text="").pack(pady="5")
    Label(r, text="Admission Number:").pack(pady=10)
    adm_no = Entry(r)
    adm_no.pack()
    Label(r, text="Your Password:").pack(pady=10)
    password = Entry(r, show="*")
    password.pack()
    Button(r, text="Confirm", command=do_op).pack(pady=14)
    r.mainloop()

def main_window():
    r = Tk()
    r.geometry("500x700")
    Label(r, text="Student Management System", font=Font(underline=True, size=25, weight="bold")).pack()
    Label(r, text="").pack(pady=10)
    Label(r, text="Student Operations:", font=Font(underline=True,size=16)).pack(pady=10)
    Button(r, bg="lightblue",fg="black",text="Create Student", command=create_student).pack(pady=10,ipady=15, ipadx=25)
    ops = ["update","search","delete"]
    for i in ops:
        Button(r, bg="lightblue",fg="black",text=i+" Student", command=lambda i=i:op_win(i)).pack(pady=10,ipady=15, ipadx=25)
    r.mainloop()

main_window()