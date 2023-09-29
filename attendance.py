import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.font as tkfont


class AttendanceSystem:
    def __init__(self):

        # Initialize tkinter
        self.conn = sqlite3.connect("school_database.db")
        self.cursor = self.conn.cursor()
        self.attendance_window = tk.Toplevel()
        self.attendance_window.title("Attendance System")

        # Create a tkinter variable to store the selected class
        self.class_var = tk.StringVar()

        # Create a label for class selection
        self.class_label = tk.Label(self.attendance_window, text="Select Class:")
        self.class_label.grid(row=0, column=0)

        # Create a dropdown menu for class selection
        self.class_dropdown = ttk.Combobox(self.attendance_window, textvariable=self.class_var)
        self.class_dropdown.grid(row=0, column=1)

        # Create a dropdown menu for class selection
        self.classes = self.cursor.execute("SELECT class_name FROM class").fetchall()
        self.class_names = [row[0] for row in self.classes]
        self.class_dropdown = ttk.Combobox(self.attendance_window, textvariable=self.class_var, values=self.class_names)
        self.class_dropdown.grid(row=0, column=1)

        # Create a label for attendance date
        self.date_var = tk.StringVar()
        self.date_label = tk.Label(self.attendance_window, text="Attendance Date (YYYY-MM-DD):")
        self.date_label.grid(row=1, column=0)

        # Create an entry field for attendance date
        self.attendance_date = tk.Entry(self.attendance_window, textvariable=self.date_var)
        self.attendance_date.grid(row=1, column=1)

        # Create a listbox to display students for the selected class
        self.student_listbox = tk.Listbox(self.attendance_window)
        self.student_listbox.grid(row=2, column=0, columnspan=5)

        # Create a button to load students for the selected class
        self.load_students_button = tk.Button(self.attendance_window, text="Load Students", command=self.load_students)
        self.load_students_button.grid(row=3, column=0, columnspan=5)

        # Create a label for marking attendance
        self.attendance_label = tk.Label(self.attendance_window, text="Mark Attendance after selecting the status:")
        self.attendance_label.grid(row=4, column=0)

        # Create a variable to store the attendance status (Present/Absent)
        self.status_var = tk.StringVar()
        self.status_var.set("Absent")  # Default status is "Absent"

        # Create a dropdown menu for marking attendance status
        self.status_dropdown = ttk.Combobox(self.attendance_window, textvariable=self.status_var,
                                            values=["Present", "Absent"])
        self.status_dropdown.grid(row=4, column=1)

        # Create a button to mark attendance
        self.mark_attendance_button = tk.Button(self.attendance_window, text="Mark Attendance",
                                                command=self.mark_attendance)
        self.mark_attendance_button.grid(row=4, column=2)

        # Initialize student_ids and student_names as empty lists
        self.student_ids = []
        self.student_names = []

    def load_students(self):
        selected_class = self.class_var.get()
        if selected_class:
            class_id = self.cursor.execute("SELECT class_id FROM class WHERE class_name=?",
                                           (selected_class,)).fetchone()
            if class_id:
                class_id = class_id[0]
                students = self.cursor.execute(
                    "SELECT student_id, first_name, last_name FROM students WHERE class_id=?",
                    (class_id,)).fetchall()
                self.student_ids = [row[0] for row in students]
                self.student_names = [f"{row[1]} {row[2]}" for row in students]
                self.student_listbox.delete(0, tk.END)
                for name in self.student_names:
                    self.student_listbox.insert(tk.END, name)
            else:
                print("Selected class not found in the database.")

    def mark_attendance(self):
        selected_class = self.class_var.get()
        date = self.date_var.get()
        selected_student = self.student_listbox.get(tk.ACTIVE)
        student_id = self.student_ids[self.student_names.index(selected_student)]
        status = self.status_var.get()

        # Insert attendance data into the database
        self.cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                            (student_id, date, status))
        self.conn.commit()

        # Clear the status variable
        self.status_var.set("Absent")


class AttendanceViewer:
    def __init__(self):
        self.conn = sqlite3.connect("school_database.db")
        self.cursor = self.conn.cursor()

        # Create a tkinter window
        self.attendance_view_window = tk.Toplevel()
        self.attendance_view_window.title("Attendance Viewer")

        # Create a tkinter variable to store the selected class
        self.class_var = tk.StringVar()

        # Create a label for class selection
        self.class_label = tk.Label(self.attendance_view_window, text="Select Class:")
        self.class_label.pack()

        # Create a dropdown menu for class selection
        self.classes = self.cursor.execute("SELECT class_name FROM class").fetchall()
        self.class_names = [row[0] for row in self.classes]
        self.class_dropdown = ttk.Combobox(self.attendance_view_window, textvariable=self.class_var,
                                           values=self.class_names)
        self.class_dropdown.pack()

        # Create a label for attendance date
        self.date_var = tk.StringVar()
        self.date_label = tk.Label(self.attendance_view_window, text="Attendance Date (YYYY-MM-DD):")
        self.date_label.pack()

        # Create an entry field for attendance date
        self.date_entry = tk.Entry(self.attendance_view_window, textvariable=self.date_var)
        self.date_entry.pack()

        # Create a button to view attendance
        self.view_attendance_button = tk.Button(self.attendance_view_window, text="View Attendance",
                                                command=self.show_attendance)
        self.view_attendance_button.pack()

    def show_attendance(self):
        selected_class = self.class_var.get()
        selected_date = self.date_var.get()

        class_id = self.cursor.execute("SELECT class_id FROM class WHERE class_name=?", (selected_class,)).fetchone()[0]
        attendance_data = self.cursor.execute("SELECT students.first_name, students.last_name, attendance.status FROM students JOIN attendance ON students.student_id = attendance.student_id WHERE students.class_id=? AND attendance.date=?",
            (class_id, selected_date)).fetchall()

        # Create a new tkinter window to display attendance
        attendance_window = tk.Toplevel(self.attendance_view_window)
        attendance_window.title("Attendance for {} on {}".format(selected_class, selected_date))

        # Create a table to display attendance
        table = ttk.Treeview(attendance_window, columns=("Name", "Status"), show="headings")
        table.heading("Name", text="Name")
        table.heading("Status", text="Status")
        table.pack()

        # Populate the table with attendance data
        for student_data in attendance_data:
            student_name = f"{student_data[0]} {student_data[1]}"
            status = student_data[2]
            table.insert("", "end", values=(student_name, status))


def show_attendance_records():
    # Create a new window for displaying records
    attendance_records_window = tk.Toplevel()
    attendance_records_window.title("Student Notice Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(attendance_records_window, columns=("Student ID", "Date", "Status"))
    tree.heading("#0", text="Attendance Record")
    tree.heading("#1", text="Student ID")
    tree.heading("#2", text="Date")
    tree.heading("#3", text="Status")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(attendance_records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch student records from the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    student_records = cursor.fetchall()
    conn.close()

    # Insert student records into the treeview
    for record in student_records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)
