import sqlite3
import tkinter as tk
from tkinter import messagebox


class Course:
    def __init__(self):
        # Create a new window for employee registration
        self.course_window = tk.Toplevel()
        self.course_window.title("Create course")

        # Create and pack entry fields for employee attributes
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

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.course_window, text="Save", command=self.save_course)
        self.save_button.pack()

    def save_course(self):
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        course_id = self.course_id_entry.get()
        course_name = self.course_name_entry.get()
        course_description = self.course_description_entry.get()

        cursor.execute('''INSERT INTO course (
                            course_id, course_name, course_description
                        ) VALUES (?, ?, ?)''',
                       (course_id, course_name, course_description))

        self.course_window.destroy()
        messagebox.showinfo("Successful", "Course Created!")

        conn.commit()
        conn.close()

    @staticmethod
    def get_all_courses():
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM course")
        courses = cursor.fetchall()

        conn.close()
        return courses

    @staticmethod
    def delete_course(course_id):
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM course WHERE course_id = ?", (course_id,))

        conn.commit()
        conn.close()
