import sqlite3
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox


class ClassCourses:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Assign courses to class")

        # Create and pack entry fields for class attributes
        self.class_id_label = tk.Label(self.window, text="Class ID")
        self.class_id_label.pack()
        self.class_id_entry = tk.Entry(self.window)
        self.class_id_entry.pack()

        self.course_id_label = tk.Label(self.window, text="Course ID:")
        self.course_id_label.pack()
        self.course_id_entry = tk.Entry(self.window)
        self.course_id_entry.pack()

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.window, text="Save", command=self.save)
        self.save_button.pack()

    def save(self):
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        class_id = self.class_id_entry.get()
        course_id = self.course_id_entry.get()

        cursor.execute("INSERT INTO class_courses (class_id, course_id) VALUES (?, ?)",
                       (class_id, course_id))

        conn.commit()
        conn.close()

        self.window.destroy()
        messagebox.showinfo("Successful", "Class Created!")


def show_class_courses_records():
    # Create a new window for displaying records
    records_window = tk.Toplevel()
    records_window.title("Class Course Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(records_window, columns=("Class ID", "Class Name"))
    tree.heading("#0", text="Class Courses Record")
    tree.heading("#1", text="Class ID")
    tree.heading("#2", text="Course ID")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch Class records from the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM class_courses")
    records = cursor.fetchall()
    conn.close()

    # Insert Class records into the treeview
    for record in records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_all_class_courses_records():
    confirmation = messagebox.askquestion("Delete All Records",
                                          "Are you sure you want to delete all Class records?")
    if confirmation == 'yes':
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM class_courses")
        conn.commit()
        messagebox.showinfo("Deletion Successful", "All Class records have been deleted.")


# Login authentication
def authenticate_student(student_id, student_password):
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()

    # Execute a query to check if the student ID and password match
    cursor.execute(
        "SELECT COUNT(*) FROM students WHERE student_id = CAST(:student_id AS INTEGER) AND password = :password",
        {"student_id": student_id, "password": student_password})

    result = cursor.fetchone()

    conn.close()

    # If the query result is 1, it means the student with the provided ID and password exists
    return result[0] == 1


def authenticate_teacher(employee_id, employee_password):
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()

    # Execute a query to check if the employee ID, password, and role match
    cursor.execute("SELECT COUNT(*) FROM employees WHERE employee_id = ? AND password = ? AND role = 'Teacher'",
                   (employee_id, employee_password))

    result = cursor.fetchone()

    conn.close()

    # If the query result is 1, it means the employee with the provided ID, password, and role exists
    return result[0] == 1
