import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector as sqltor

# Database connection function
def connect_db():
    try:
        return sqltor.connect(host="localhost", user="root", passwd="helpmelaugh", database="testdb")
    except sqltor.Error as err:
        if err.errno == sqltor.errorcode.ER_ACCESS_DENIED_ERROR:
            messagebox.showerror("Database Error", "Something is wrong with your user name or password")
        elif err.errno == sqltor.errorcode.ER_BAD_DB_ERROR:
            messagebox.showerror("Database Error", "Database does not exist")
        else:
            messagebox.showerror("Database Error", f"Error: {err}")
        return None


# Main application window
class ReportCardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("REPORT CARD SYSTEM")
        self.geometry('550x500')
        self.config(bg='slate gray')
        self.create_main_screen()

    def create_main_screen(self):
        tk.Button(self, text="Teacher/Admin", width=15, bg="white", font=('Arial', 14), command=self.open_ta_login).pack(pady=20)
        tk.Button(self, text="Student", width=15, bg="white", font=('Arial', 14), command=self.open_student_login).pack(pady=20)

    def open_ta_login(self):
        TALoginWindow(self)

    def open_student_login(self):
        StudentLoginWindow(self)

# Teacher/Admin Login Window
class TALoginWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("LOGIN")
        self.geometry('750x600')
        self.config(bg='slate gray')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, bg="gray76", height=25, width=60).place(x=129, y=160)

        self.username = tk.Entry(self, font=('Arial', 12))
        self.username.place(x=305, y=260)
        tk.Label(self, text="Username", width=10, bg="white", font=('Arial', 14)).place(x=145, y=260)

        self.password = tk.Entry(self, font=('Arial', 12), show="*")
        self.password.place(x=305, y=310)
        tk.Label(self, text="Password", width=10, bg="white", font=('Arial', 14)).place(x=145, y=310)

        self.designation = tk.Entry(self, font=('Arial', 12))
        self.designation.place(x=305, y=360)
        tk.Label(self, text="Designation", width=10, bg="white", font=('Arial', 14)).place(x=145, y=360)

        tk.Button(self, text="LOGIN", width=12, bg="white", font=('Arial', 14), command=self.login).place(x=180, y=470)
        tk.Button(self, text="RESET PASSWORD", width=18, bg="white", font=('Arial', 14), command=self.open_reset_window).place(x=340, y=470)

    def login(self):
        username = self.username.get().lower()
        password = self.password.get()
        designation = self.designation.get().lower()

        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("SELECT * FROM login WHERE Username=%s", (username,))
            output = mc.fetchone()

            if output and output[1] == password and output[2].lower() == designation:
                messagebox.showinfo("LOGIN", "Login successful")
                if designation == "admin":
                    AdminWindow(self)
                elif designation == "teacher":
                    TeacherWindow(self)
            else:
                messagebox.showinfo("LOGIN", "Login unsuccessful")

    def open_reset_window(self):
        ResetPasswordWindow(self)

# Reset Password Window
class ResetPasswordWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("RESET PASSWORD")
        self.geometry('750x600')
        self.config(bg='slate gray')
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, bg="gray76", height=25, width=68).place(x=129, y=160)

        self.old_pwd = tk.Entry(self, font=('Arial', 12), show="*")
        self.old_pwd.place(x=335, y=260)
        tk.Label(self, text="Current password", width=15, bg="white", font=('Arial', 14)).place(x=145, y=260)

        self.new_pwd = tk.Entry(self, font=('Arial', 12), show="*")
        self.new_pwd.place(x=335, y=310)
        tk.Label(self, text="New Password", width=15, bg="white", font=('Arial', 14)).place(x=145, y=310)

        tk.Button(self, text="OK", width=12, bg="white", font=('Arial', 14), command=self.reset_password).place(x=280, y=470)

    def reset_password(self):
        old_password = self.old_pwd.get()
        new_password = self.new_pwd.get()

        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("UPDATE login SET Password=%s WHERE Password=%s", (new_password, old_password))
            mydb.commit()

        messagebox.showinfo("RESET", "Password reset successful")
        self.destroy()

# Admin Window
class AdminWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("ADMIN")
        self.geometry('300x500')
        self.config(bg='slate gray')
        self.create_widgets()

    def create_widgets(self):
        buttons = [
            ("INSERT", self.insert_button),
            ("UPDATE", self.update_button),
            ("DELETE", self.delete_button),
            ("VIEW", self.view_button)
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(self, text=text, width=20, bg="white", fg="black", font=('Arial', 14), command=command).place(x=20, y=150 + i*100)

    def insert_button(self):
        InsertWindow(self)

    def update_button(self):
        UpdateWindow(self)

    def delete_button(self):
        DeleteWindow(self)

    def view_button(self):
        ViewWindow(self)

# Insert Window
class InsertWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("INSERT RECORD")
        self.geometry('400x300')
        self.config(bg='slate gray')
        self.create_widgets()

    def create_widgets(self):
        self.roll_no = tk.Entry(self, font=('Arial', 12))
        self.roll_no.pack(pady=10)
        tk.Label(self, text="Roll No", bg="white", font=('Arial', 14)).pack()

        self.name = tk.Entry(self, font=('Arial', 12))
        self.name.pack(pady=10)
        tk.Label(self, text="Name", bg="white", font=('Arial', 14)).pack()

        tk.Button(self, text="Insert", width=12, bg="white", font=('Arial', 14), command=self.insert_record).pack(pady=20)

    def insert_record(self):
        roll_no = self.roll_no.get()
        name = self.name.get()

        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("INSERT INTO admin (RollNo, Name) VALUES (%s, %s)", (roll_no, name))
            mydb.commit()

        messagebox.showinfo("INSERT", "Record inserted successfully")
        self.destroy()

# Update Window
class UpdateWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("UPDATE RECORD")
        self.geometry('400x300')
        self.config(bg='slate gray')
        self.create_widgets()

    def create_widgets(self):
        self.roll_no = tk.Entry(self, font=('Arial', 12))
        self.roll_no.pack(pady=10)
        tk.Label(self, text="Roll No", bg="white", font=('Arial', 14)).pack()

        self.new_name = tk.Entry(self, font=('Arial', 12))
        self.new_name.pack(pady=10)
        tk.Label(self, text="New Name", bg="white", font=('Arial', 14)).pack()

        tk.Button(self, text="Update", width=12, bg="white", font=('Arial', 14), command=self.update_record).pack(pady=20)

    def update_record(self):
        roll_no = self.roll_no.get()
        new_name = self.new_name.get()

        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("UPDATE admin SET Name=%s WHERE RollNo=%s", (new_name, roll_no))
            mydb.commit()

        messagebox.showinfo("UPDATE", "Record updated successfully")
        self.destroy()

# Delete Window
class DeleteWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("DELETE RECORD")
        self.geometry('400x200')
        self.config(bg='slate gray')
        self.create_widgets()

    def create_widgets(self):
        self.roll_no = tk.Entry(self, font=('Arial', 12))
        self.roll_no.pack(pady=10)
        tk.Label(self, text="Roll No to Delete", bg="white", font=('Arial', 14)).pack()

        tk.Button(self, text="Delete", width=12, bg="white", font=('Arial', 14), command=self.delete_record).pack(pady=20)

    def delete_record(self):
        roll_no = self.roll_no.get()

        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("DELETE FROM admin WHERE RollNo=%s", (roll_no,))
            mydb.commit()

        messagebox.showinfo("DELETE", "Record deleted successfully")
        self.destroy()

# View Window
class ViewWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("VIEW RECORDS")
        self.geometry('600x400')
        self.config(bg='slate gray')
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('Roll No', 'Name'), show='headings')
        self.tree.heading('Roll No', text='Roll No')
        self.tree.heading('Name', text='Name')
        self.tree.pack(pady=20, padx=20, expand=True, fill='both')

        self.load_data()

    def load_data(self):
        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("SELECT RollNo, Name FROM admin")
            records = mc.fetchall()

        for record in records:
            self.tree.insert('', 'end', values=record)

# Teacher Window
class TeacherWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("TEACHER")
        self.geometry('450x500')
        self.config(bg='slate gray')
        self.create_widgets()

    def create_widgets(self):
        self.subid = tk.Entry(self, width=15, font=('Arial', 12))
        self.subid.place(x=220, y=70)
        tk.Label(self, text="SUBJECT ID", width=15, bg="white", font=('Arial', 14)).place(x=20, y=70)

        buttons = [
            ("INSERT", self.insert_button),
            ("UPDATE", self.update_button),
            ("VIEW", self.view_button)
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(self, text=text, width=20, bg="white", fg="black", font=('Arial', 14), command=command).place(x=20, y=150 + i*100)

    def insert_button(self):
        InsertMarksWindow(self, self.subid.get())

    def update_button(self):
        UpdateMarksWindow(self, self.subid.get())

    def view_button(self):
        ViewMarksWindow(self, self.subid.get())

# Insert Marks Window
class InsertMarksWindow(tk.Toplevel):
    def __init__(self, master, subject_id):
        super().__init__(master)
        self.title("INSERT MARKS")
        self.geometry('400x300')
        self.config(bg='slate gray')
        self.subject_id = subject_id
        self.create_widgets()

    def create_widgets(self):
        self.roll_no = tk.Entry(self, font=('Arial', 12))
        self.roll_no.pack(pady=10)
        tk.Label(self, text="Roll No", bg="white", font=('Arial', 14)).pack()

        self.marks = tk.Entry(self, font=('Arial', 12))
        self.marks.pack(pady=10)
        tk.Label(self, text="Marks", bg="white", font=('Arial', 14)).pack()

        tk.Button(self, text="Insert", width=12, bg="white", font=('Arial', 14), command=self.insert_marks).pack(pady=20)

    def insert_marks(self):
        roll_no = self.roll_no.get()
        marks = self.marks.get()

        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("INSERT INTO marks (RollNo, SubjectID, Marks) VALUES (%s, %s, %s)", (roll_no, self.subject_id, marks))
            mydb.commit()

        messagebox.showinfo("INSERT", "Marks inserted successfully")
        self.destroy()

# Update Marks Window
class UpdateMarksWindow(tk.Toplevel):
    def __init__(self, master, subject_id):
        super().__init__(master)
        self.title("UPDATE MARKS")
        self.geometry('400x300')
        self.config(bg='slate gray')
        self.subject_id = subject_id
        self.create_widgets()

    def create_widgets(self):
        self.roll_no = tk.Entry(self, font=('Arial', 12))
        self.roll_no.pack(pady=10)
        tk.Label(self, text="Roll No", bg="white", font=('Arial', 14)).pack()

        self.new_marks = tk.Entry(self, font=('Arial', 12))
        self.new_marks.pack(pady=10)
        tk.Label(self, text="New Marks", bg="white", font=('Arial', 14)).pack()

        tk.Button(self, text="Update", width=12, bg="white", font=('Arial', 14), command=self.update_marks).pack(pady=20)

    def update_marks(self):
        roll_no = self.roll_no.get()
        new_marks = self.new_marks.get()

        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("UPDATE marks SET Marks=%s WHERE RollNo=%s AND SubjectID=%s", (new_marks, roll_no, self.subject_id))
            mydb.commit()

        messagebox.showinfo("UPDATE", "Marks updated successfully")
        self.destroy()

# View Marks Window
class ViewMarksWindow(tk.Toplevel):
    def __init__(self, master, subject_id):
        super().__init__(master)
        self.title("VIEW MARKS")
        self.geometry('600x400')
        self.config(bg='slate gray')
        self.subject_id = subject_id
        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('Roll No', 'Marks'), show='headings')
        self.tree.heading('Roll No', text='Roll No')
        self.tree.heading('Marks', text='Marks')
        self.tree.pack(pady=20, padx=20, expand=True, fill='both')

        self.load_data()

    def load_data(self):
        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("SELECT RollNo, Marks FROM marks WHERE SubjectID=%s", (self.subject_id,))
            records = mc.fetchall()

        for record in records:
            self.tree.insert('', 'end', values=record)

# Student Login Window
class StudentLoginWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("STUDENT LOGIN")
        self.geometry('500x300')
        self.config(bg='slate gray')
        self.create_widgets()

    def create_widgets(self):
        self.rollno = tk.Entry(self, font=('Arial', 12))
        self.rollno.place(x=150, y=30)
        tk.Label(self, text="Roll No", width=10, bg="white", font=('Arial', 14)).place(x=20, y=30)

        tk.Button(self, text="Report card", width=12, bg="white", font=('Arial', 14), command=self.show_report).place(x=120, y=125)

    def show_report(self):
        rid = self.rollno.get()
        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("SELECT * from admin where RollNo=%s", (rid,))
            output = mc.fetchone()

        if not output:
            messagebox.showinfo("LOGIN", "Roll No does not exist")
        else:
            ReportCardWindow(self, rid)

# Report Card Window
class ReportCardWindow(tk.Toplevel):
    def __init__(self, master, rid):
        super().__init__(master)
        self.title("REPORT CARD")
        self.geometry('700x800')
        self.config(bg='slate gray')
        self.rid = rid
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=f"Report Card for Roll No: {self.rid}", bg="white", font=('Arial', 16, 'bold')).pack(pady=20)

        self.tree = ttk.Treeview(self, columns=('Subject', 'Marks'), show='headings')
        self.tree.heading('Subject', text='Subject')
        self.tree.heading('Marks', text='Marks')
        self.tree.pack(pady=20, padx=20, expand=True, fill='both')

        self.load_data()

        tk.Button(self, text="Print", width=12, bg="white", font=('Arial', 14), command=self.print_report).pack(pady=20)

    def load_data(self):
        with connect_db() as mydb:
            mc = mydb.cursor()
            mc.execute("""
                SELECT s.SubjectName, m.Marks
                FROM marks m
                JOIN subjects s ON m.SubjectID = s.SubjectID
                WHERE m.RollNo = %s
            """, (self.rid,))
            records = mc.fetchall()

        for record in records:
            self.tree.insert('', 'end', values=record)

    def print_report(self):
        # In a real application, this would generate a PDF or send to a printer
        messagebox.showinfo("Print", "Printing report card...")

if __name__ == "__main__":
    app = ReportCardApp()
    app.mainloop()