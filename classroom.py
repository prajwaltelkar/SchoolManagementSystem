import sqlite3
import tkinter as tk
from tkinter import messagebox


class ClassRoom:
    def __init__(self):
        self.class_window = tk.Toplevel()
        self.class_window.title("Create Class")

        # Create and pack entry fields for employee attributes
        self.class_id_label = tk.Label(self.class_window, text="Class ID")
        self.class_id_label.pack()
        self.class_id_entry = tk.Entry(self.class_window)
        self.class_id_entry.pack()

        self.class_name_label = tk.Label(self.class_window, text="Class Name:")
        self.class_name_label.pack()
        self.class_name_entry = tk.Entry(self.class_window)
        self.class_name_entry.pack()

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.class_window, text="Save", command=self.save_classroom)
        self.save_button.pack()

    def save_classroom(self):
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        class_id = self.class_id_entry.get()
        class_name = self.class_name_entry.get()

        cursor.execute('''INSERT INTO class (
                            class_id, class_name
                        ) VALUES (?, ?)''',
                       (class_id, class_name))

        conn.commit()
        conn.close()

        self.class_window.destroy()
        messagebox.showinfo("Successful", "Class Created!")

    @staticmethod
    def get_all_classes():
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM class")
        classes = cursor.fetchall()

        conn.close()
        return classes

    @staticmethod
    def delete_class(class_id):
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM class WHERE class_id = ?", (class_id,))

        conn.commit()
        conn.close()


def create_class():
    # Create a new instance of StudentRegistrationPage for registering students
    create_class_page = ClassRoom
