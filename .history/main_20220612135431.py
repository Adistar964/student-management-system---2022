from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import sqlite3

connection = sqlite3.connect("students.db")
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

def delete_student(adm_no):
    cursor.execute(f"DELETE FROM students WHERE admission_number={adm_no}")
    connection.commit()
    messagebox.showinfo("Completed", "Successfully deleted a student!")

def search_student(data):
    r = Toplevel()
    r.geometry("700x700")
    r.resizable(0,0)
    def give_name():
        name = data["name"]
        val = ""
        if len(name) > 23:
            val = name[0:19] + "..."
        else:
            val=name
        return val
    Label(r, text=give_name(), font=Font(size=20, underline=True, weight="bold")).pack(pady=14, padx=30)
    frame = Frame(r, highlightbackground="black", highlightthickness=2)
    frame.pack(ipady=15, ipadx=10,fill=X)
    for i in data.keys():
        row = Entry(frame, font=Font(size=15, weight="bold"))
        row.insert(0,i.replace("_", " ")+" : "+str(data[i]))
        row["state"] = "disabled"
        row.pack(fill=X, padx=9)
    r.mainloop()

def update_student(info):
    r = Toplevel()
    r.resizable(0,0)
    data = list(info.keys())
    admission_number = info["admission_number"]
    def update():
        try:
            cursor.execute(f"UPDATE students SET {value_of_menu.get()}='{input.get()}' WHERE admission_number={admission_number}")
            connection.commit()
            messagebox.showinfo("updated!", "successfully updated the student")
        except Exception as e:
            print(e)
            print("wronff")
            messagebox.showerror("error", "wrong data entered!")
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

def operation_dialogue(op):
    r = Toplevel()
    r.geometry("400x400")
    r.title("student operations")
    def do_operation():
        if userpass.get() == "1234" and adm_no.get().isnumeric():
            ad_no = int(adm_no.get())
            cursor.execute(f"SELECT * FROM students WHERE admission_number={ad_no}")
            connection.commit()
            data = cursor.fetchone()
            if data:
                r.destroy()
                if op == "delete":
                    delete_student(ad_no)
                elif op == "search":
                    search_student(dict(data))
                else:
                    update_student(dict(data))
            else:
                messagebox.showerror("Wrong Admission Number!", "Wrong Admission Number entered!")
        else:
            messagebox.showerror("Wrong Data!", "Wrong Information entered!")

    Label(r, text="Student Admission Number:", font=Font(size=12)).pack(pady=6)
    adm_no = Entry(r, font=Font(size=12))
    adm_no.pack(ipadx=40,ipady=8)
    Label(r, text="Your Password:", font=Font(size=12)).pack(pady=6)
    userpass = Entry(r, font=Font(size=12), show="*")
    userpass.pack(ipadx=40,ipady=8)
    Button(r, command=do_operation,text="Confirm", font=Font(size=12), bg="Red", fg="white").pack(ipadx=25, ipady=7, pady=13)
    r.mainloop()

def main_window():
    w = Tk()
    w.geometry("700x700")
    w.resizable(0,0)
    w.title("student management system")

    def back_to_login():
        answer = messagebox.askquestion("logout", "Are you sure you want to logout?")
        if answer == "yes":
            w.destroy()
            login_window()

    Label(w, text="Student Management System", font=Font(size=25), bg="red", fg="white").pack(padx=100, pady=20)
    Label(w, text="Ali is using the system.", font=Font(size=10, weight="bold")).pack()
    Label(w, text="Student Operations:", font=Font(size=20, underline=True)).pack(pady=12)
    create_btn = Button(text="create student", font=Font(size=15), bg="lightblue", fg="black")
    create_btn.pack(pady=10)
    update_btn = Button(command=lambda: operation_dialogue("update"),text="update student Info", font=Font(size=15), bg="lightblue", fg="black")
    update_btn.pack(pady=10)
    search_btn = Button(command=lambda: operation_dialogue("search"),text="search student", font=Font(size=15), bg="lightblue", fg="black")
    search_btn.pack(pady=10)
    delete_btn = Button(text="delete student", command=lambda:operation_dialogue("delete"),font=Font(size=15), bg="lightblue", fg="black")
    delete_btn.pack(pady=10)
    Label(w, text="User Operations:", font=Font(size=20, underline=True)).pack(pady=13)
    logout_btn = Button(text="logout", font=Font(size=15), bg="lightblue", fg="black", command=back_to_login)
    logout_btn.pack()
    w.mainloop()

def login_window():
    r = Tk()
    r.title("Login")
    r.config(bg="black")
    r.geometry("700x500")
    r.resizable(0,0)
    def check_cred():
        username = user_inp.get()
        password = pass_inp.get()
        if username.lower() == "ali" and password.lower() == "1234":
            r.destroy()
            main_window()
        else:
            messagebox.showwarning("Wrong credentials!", "Wrong username or password entered!")
        # r.destroy()
        # main_window()


    title = Label(r, text="Admin Login", bg="black", fg="white", font=Font(size=28, underline=True))
    title.pack(ipady=15)

    Label(r, text="", bg="black").pack(pady=10)

    user_label = Label(r, text="username", bg="black", fg="white", font=Font(size=15))
    user_label.pack(ipadx=16, ipady=5) 

    user_inp = Entry(r, font=Font(size=12))
    user_inp.pack(ipadx=40,ipady=8, padx=20)

    Label(r, text="", bg="black").pack(pady=6)

    pass_label = Label(r, text="password", bg="black", fg="white", font=Font(size=15))
    pass_label.pack(ipadx=16, ipady=5) 

    pass_inp = Entry(r, font=Font(size=12), show="*")
    pass_inp.pack(ipadx=40,ipady=8, padx=20)

    Button(r, command=check_cred,text="Login", font=Font(size=12), bg="green", fg="white").pack(pady=30, ipadx=25, ipady=10)

    r.mainloop()

login_window()
connection.close()