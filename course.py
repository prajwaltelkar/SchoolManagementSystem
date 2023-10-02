import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter import messagebox, simpledialog


class Course:
    def __init__(self):
        # Create a new window for employee registration
        self.course_window = tk.Toplevel()
        self.course_window.title("Create course")

        # Create and pack entry fields for course attributes
        course_id_label = tk.Label(self.course_window, text="Course ID")
        course_id_label.pack()
        self.course_id_entry = tk.Entry(self.course_window)
        self.course_id_entry.pack()

        course_name_label = tk.Label(self.course_window, text="Course Name:")
        course_name_label.pack()
        self.course_name_entry = tk.Entry(self.course_window)
        self.course_name_entry.pack()

        course_description_label = tk.Label(self.course_window, text="Course description:")
        course_description_label.pack()
        self.course_description_entry = tk.Entry(self.course_window)
        self.course_description_entry.pack()

        employee_id_label = tk.Label(self.course_window, text="Employee ID:")
        employee_id_label.pack()
        self.employee_id_entry = tk.Entry(self.course_window)
        self.employee_id_entry.pack()

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.course_window, text="Save", command=self.save_course)
        self.save_button.pack()

    def save_course(self):
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        course_id = self.course_id_entry.get()
        course_name = self.course_name_entry.get()
        course_description = self.course_description_entry.get()
        employee_id = self.employee_id_entry.get()

        cursor.execute('''INSERT INTO course (
                            course_id, course_name, course_description, employee_id
                        ) VALUES (?, ?, ?, ?)''',
                       (course_id, course_name, course_description, employee_id))

        self.course_window.destroy()
        messagebox.showinfo("Successful", "Course Created!")

        conn.commit()
        conn.close()


def show_course_records():
    # Create a new window for displaying records
    course_records_window = tk.Toplevel()
    course_records_window.title("Course Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(course_records_window, columns=("Course ID", "Course Name", "Course Description", "Employee ID"))
    tree.heading("#0", text="Course Record")
    tree.heading("#1", text="Course ID")
    tree.heading("#2", text="Course Name")
    tree.heading("#3", text="Course Description")
    tree.heading("#4", text="Employee ID")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(course_records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch Employee records from the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course")
    employee_records = cursor.fetchall()
    conn.close()

    # Insert Employee records into the treeview
    for record in employee_records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_course():
    # Create a Tkinter window
    course_window = tk.Tk()
    course_window.withdraw()  # Hide the main window

    # Prompt the user for course_id using simpledialog
    course_id = simpledialog.askinteger("Input", "Enter Course ID:")

    if course_id is not None:
        confirmation = messagebox.askquestion("Delete Course",
                                              f"Are you sure you want to delete Course ID "
                                              f" {course_id} from the Courses?")
        if confirmation == 'yes':
            conn = sqlite3.connect("school_database.db")
            cursor = conn.cursor()

            # Delete the course record for the specified course_id
            cursor.execute("DELETE FROM course WHERE course_id = ?", (course_id,))

            conn.commit()
            conn.close()
            messagebox.showinfo("Deletion Successful", f"Course record with ID "
                                                       f" {course_id} has been deleted.")
        else:
            messagebox.showinfo("Deletion Canceled", "Course record has not been deleted.")
    else:
        messagebox.showinfo("Invalid Input", "Please provide a valid Course ID.")

    # Close the Tkinter window
    course_window.destroy()


def delete_all_course_records():
    confirmation = messagebox.askquestion("Delete All Records",
                                          "Are you sure you want to delete all Course records?")
    if confirmation == 'yes':
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM course")
        conn.commit()
        messagebox.showinfo("Deletion Successful", "All Course records have been deleted.")
