import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import tkinter.font as tkfont


class Student:
    def __init__(self):
        self.student_window = tk.Toplevel()
        self.student_window.title("Register Student")

        # Create and pack entry fields for student attributes
        self.student_id_label = tk.Label(self.student_window, text="Student ID:")
        self.student_id_label.pack()
        self.student_id_entry = tk.Entry(self.student_window)
        self.student_id_entry.pack()

        self.first_name_label = tk.Label(self.student_window, text="First Name:")
        self.first_name_label.pack()
        self.first_name_entry = tk.Entry(self.student_window)
        self.first_name_entry.pack()

        self.last_name_label = tk.Label(self.student_window, text="Last Name:")
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(self.student_window)
        self.last_name_entry.pack()

        # Create and pack entry fields for student attributes
        self.dob_label = tk.Label(self.student_window, text="Date of Birth:")
        self.dob_label.pack()
        self.dob_entry = tk.Entry(self.student_window)
        self.dob_entry.pack()

        self.address_label = tk.Label(self.student_window, text="Address:")
        self.address_label.pack()
        self.address_entry = tk.Entry(self.student_window)
        self.address_entry.pack()

        self.contact_number_label = tk.Label(self.student_window, text="Contact Number:")
        self.contact_number_label.pack()
        self.contact_number_entry = tk.Entry(self.student_window)
        self.contact_number_entry.pack()

        self.father_name_label = tk.Label(self.student_window, text="Father's Name:")
        self.father_name_label.pack()
        self.father_name_entry = tk.Entry(self.student_window)
        self.father_name_entry.pack()

        self.mother_name_label = tk.Label(self.student_window, text="Mother's Name:")
        self.mother_name_label.pack()
        self.mother_name_entry = tk.Entry(self.student_window)
        self.mother_name_entry.pack()

        self.enrollment_date_label = tk.Label(self.student_window, text="Enrollment Date:")
        self.enrollment_date_label.pack()
        self.enrollment_date_entry = tk.Entry(self.student_window)
        self.enrollment_date_entry.pack()

        self.gender_label = tk.Label(self.student_window, text="Gender:")
        self.gender_label.pack()
        self.gender_entry = tk.Entry(self.student_window)
        self.gender_entry.pack()

        self.password_label = tk.Label(self.student_window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.student_window)
        self.password_entry.pack()

        self.class_id_label = tk.Label(self.student_window, text="Class ID:")
        self.class_id_label.pack()
        self.class_id_entry = tk.Entry(self.student_window)
        self.class_id_entry.pack()

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.student_window, text="Save", command=self.save_student)
        self.save_button.pack()

    def save_student(self):
        # Retrieve data from entry fields
        student_id = self.student_id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        dob = self.dob_entry.get()
        address = self.address_entry.get()
        contact_number = self.contact_number_entry.get()
        father_name = self.father_name_entry.get()
        mother_name = self.mother_name_entry.get()
        enrollment_date = self.enrollment_date_entry.get()
        gender = self.gender_entry.get()
        password = self.password_entry.get()
        class_id = self.class_id_entry.get()

        # Insert student information into the database
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO students (
                            student_id, first_name, last_name, dob, address, contact_number, 
                            father_name, mother_name, enrollment_date, gender, password, class_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (student_id, first_name, last_name, dob, address, contact_number,
                        father_name, mother_name, enrollment_date, gender, password, class_id))

        conn.commit()
        conn.close()

        # Close the student registration window
        self.student_window.destroy()
        messagebox.showinfo("Registration Successful", "Student Registered!")


def show_student_records():
    # Create a new window for displaying records
    records_window = tk.Toplevel()
    records_window.title("Student Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(records_window, columns=("Student ID", "First Name", "Last Name", "DOB", "Address",
                                                 "Contact Number", "Father Name", "Mother Name",
                                                 "Enrollment Date",
                                                 "Gender", "Password", "Class ID"))
    tree.heading("#0", text="Student Records")
    tree.heading("#1", text="Student ID")
    tree.heading("#2", text="First Name")
    tree.heading("#3", text="Last Name")
    tree.heading("#4", text="Date of Birth")
    tree.heading("#5", text="Address")
    tree.heading("#6", text="Contact Number")
    tree.heading("#7", text="Father Name")
    tree.heading("#8", text="Mother Name")
    tree.heading("#9", text="Enrollment Date")
    tree.heading("#10", text="Gender")
    tree.heading("#11", text="Password")
    tree.heading("#12", text="Class ID")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch student records from the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    student_records = cursor.fetchall()
    conn.close()

    # Insert student records into the treeview
    for record in student_records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_all_student_records():
    confirmation = messagebox.askquestion("Delete All Records",
                                          "Are you sure you want to delete all student records?")
    if confirmation == 'yes':
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students")
        conn.commit()
        messagebox.showinfo("Deletion Successful", "All student records have been deleted.")
