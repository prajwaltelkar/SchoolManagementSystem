import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import tkinter.font as tkfont


class StudentNotice:
    def __init__(self):
        self.student_notice_window = tk.Toplevel()
        self.student_notice_window.title("Send Student Notice")

        # Create and pack entry fields for student_notice attributes
        self.notice_id_label = tk.Label(self.student_notice_window, text="Notice ID:")
        self.notice_id_label.pack()
        self.notice_id_entry = tk.Entry(self.student_notice_window)
        self.notice_id_entry.pack()

        self.student_id_label = tk.Label(self.student_notice_window, text="Student ID:")
        self.student_id_label.pack()
        self.student_id_entry = tk.Entry(self.student_notice_window)
        self.student_id_entry.pack()

        self.title_label = tk.Label(self.student_notice_window, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.student_notice_window)
        self.title_entry.pack()

        self.content_label = tk.Label(self.student_notice_window, text="Content:")
        self.content_label.pack()
        self.content_entry = tk.Entry(self.student_notice_window)
        self.content_entry.pack()

        self.publish_date_label = tk.Label(self.student_notice_window, text="Published Date:")
        self.publish_date_label.pack()
        self.publish_date_entry = tk.Entry(self.student_notice_window)
        self.publish_date_entry.pack()

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.student_notice_window, text="Save", command=self.save_student_notice)
        self.save_button.pack()

    def save_student_notice(self):
        # Retrieve data from entry fields
        notice_id = self.notice_id_entry.get()
        student_id = self.student_id_entry.get()
        title = self.title_entry.get()
        content = self.content_entry.get()
        publish_date = self.publish_date_entry.get()

        # Insert student information into the database
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO student_notice (
                                stud_notice_id, student_id, title, content, publish_date
                            ) VALUES (?, ?, ?, ?, ?)''',
                       (notice_id, student_id, title, content, publish_date))

        conn.commit()
        conn.close()

        # Close the student registration window
        self.student_notice_window.destroy()
        messagebox.showinfo("Student Notice Status Updated", "Student Notice status"
                                                             "has been updated for the student.")


def show_student_notice_records():
    # Create a new window for displaying records
    student_notice_records_window = tk.Toplevel()
    student_notice_records_window.title("Student Notice Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(student_notice_records_window, columns=("Notice ID", "Student ID", "Title", "Content",
                                                                "Published Date"))
    tree.heading("#1", text="Notice ID")
    tree.heading("#2", text="Student ID")
    tree.heading("#3", text="Title")
    tree.heading("#4", text="Content")
    tree.heading("#5", text="Published Date")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(student_notice_records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch student records from the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_notice")
    student_records = cursor.fetchall()
    conn.close()

    # Insert student records into the treeview
    for record in student_records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_all_student_notice_records():
    confirmation = messagebox.askquestion("Delete All Records",
                                          "Are you sure you want to delete all student student notice records?")
    if confirmation == 'yes':
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student_notice")
        conn.commit()
        messagebox.showinfo("Deletion Successful", "All student student notice records have been deleted.")
