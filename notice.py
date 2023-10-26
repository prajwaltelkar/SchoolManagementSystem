import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import sqlite3
import tkinter.font as tkfont


class StudentNotice:
    def __init__(self, db_connection):
        self.student_notice_window = tk.Toplevel()
        self.student_notice_window.title("Send Student Notice")

        self.conn = db_connection

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
        student_id = self.student_id_entry.get()
        title = self.title_entry.get()
        content = self.content_entry.get()
        publish_date = self.publish_date_entry.get()

        # Insert student information into the database
        cursor = self.conn.cursor()

        try:
            cursor.execute('''INSERT INTO student_notice (
                                    student_id, title, content, publish_date
                                ) VALUES (?, ?, ?, ?)''',
                           (student_id, title, content, publish_date))
            self.conn.commit()

            # Close the student registration window
            self.student_notice_window.destroy()
            messagebox.showinfo("Student Notice Status Updated", "Student Notice"
                                                                 " has been sent to the student.")
        except sqlite3.Error as error:
            messagebox.showerror("Error", str(error))


def show_student_notice_records():
    # Create a new window for displaying records
    student_notice_records_window = tk.Tk()
    student_notice_records_window.title("Student Notice Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(student_notice_records_window, columns=("Notice ID", "Student ID", "Title", "Content", "Published Date"))
    tree.heading("#0", text="Student Notice Record")
    tree.heading("#1", text="Notice ID")
    tree.heading("#2", text="Student ID")
    tree.heading("#3", text="Title")
    tree.heading("#4", text="Content")
    tree.heading("#5", text="Published Date")

    # Establish a connection to the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()

    # Fetch student notice records from the database
    cursor.execute("SELECT * FROM student_notice")
    student_records = cursor.fetchall()

    # Insert student notice records into the treeview
    for record in student_records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=200)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)

    # Create a text widget for displaying full content
    text_widget = tk.Text(student_notice_records_window, wrap="word")
    text_widget.pack(fill=tk.BOTH, expand=True)

    # Bind a click event to display full content in the text widget
    def display_content(event):
        item = tree.selection()
        if item:
            content = tree.item(item, "values")[3]
            text_widget.delete("1.0", "end")
            text_widget.insert("1.0", content)

    tree.bind("<ButtonRelease-1>", display_content)

    # Close the database connection
    conn.close()

    student_notice_records_window.mainloop()


def delete_student_notice_record(conn):
    # Create a Tkinter window
    notice_window = tk.Tk()
    notice_window.withdraw()

    # Prompt the user for stud_notice_id using simpledialog
    stud_notice_id = simpledialog.askinteger("Input", "Enter Student Notice ID:")

    if stud_notice_id is not None:
        confirmation = messagebox.askquestion("Delete Student Notice",
                                              f"Are you sure you want to delete Student Notice ID {stud_notice_id} from the Student Notices?")
        if confirmation == 'yes':
            cursor = conn.cursor()

            # Delete the student notice record for the specified stud_notice_id
            try:
                cursor.execute("DELETE FROM student_notice WHERE stud_notice_id = ?", (stud_notice_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Deletion Successful", f"Student notice with ID {stud_notice_id} has been deleted.")
                else:
                    messagebox.showerror("Invalid Input", "No such Student Notice record.")
            except sqlite3.Error as error:
                conn.rollback()  # Rollback the transaction in case of an error
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showinfo("Deletion Canceled", "Student notice has not been deleted.")
    else:
        messagebox.showinfo("Invalid Input", "Please provide a valid Student Notice ID.")

    # Close the Tkinter window
    notice_window.destroy()


def delete_all_student_notice_records(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM student_notice")
    count = cursor.fetchone()[0]

    if count == 0:
        messagebox.showerror("No Records", "There are no Student Notice records to delete.")
    else:
        confirmation = messagebox.askquestion("Delete All Records",
                                              "Are you sure you want to delete all student notice records?")
        if confirmation == 'yes':
            try:
                cursor.execute("DELETE FROM student_notice")
                conn.commit()
                messagebox.showinfo("Deletion Successful", "All student notice records have been deleted.")
            except sqlite3.Error as error:
                conn.rollback()
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "No Course records have been deleted.")


class EmployeeNotice:
    def __init__(self, db_connection):
        self.employee_notice_window = tk.Toplevel()
        self.employee_notice_window.title("Send Employee Notice")

        self.conn = db_connection

        # Create and pack entry fields for employee_notice attributes
        self.employee_id_label = tk.Label(self.employee_notice_window, text="Employee ID:")
        self.employee_id_label.pack()
        self.employee_id_entry = tk.Entry(self.employee_notice_window)
        self.employee_id_entry.pack()

        self.title_label = tk.Label(self.employee_notice_window, text="Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(self.employee_notice_window)
        self.title_entry.pack()

        self.content_label = tk.Label(self.employee_notice_window, text="Content:")
        self.content_label.pack()
        self.content_entry = tk.Entry(self.employee_notice_window)
        self.content_entry.pack()

        self.publish_date_label = tk.Label(self.employee_notice_window, text="Published Date:")
        self.publish_date_label.pack()
        self.publish_date_entry = tk.Entry(self.employee_notice_window)
        self.publish_date_entry.pack()

        # Create the "Save" button and bind it to the save_Employee method
        self.save_button = tk.Button(self.employee_notice_window, text="Save", command=self.save_employee_notice)
        self.save_button.pack()

    def save_employee_notice(self):
        # Retrieve data from entry fields
        employee_id = self.employee_id_entry.get()
        title = self.title_entry.get()
        content = self.content_entry.get()
        publish_date = self.publish_date_entry.get()

        # Insert Employee information into the database
        cursor = self.conn.cursor()
        try:
            cursor.execute('''INSERT INTO employee_notice (
                                    employee_id, title, content, publish_date
                                ) VALUES (?, ?, ?, ?)''',
                           (employee_id, title, content, publish_date))
            self.conn.commit()

            # Close the Employee registration window
            self.employee_notice_window.destroy()
            messagebox.showinfo("Employee Notice Status Updated", "Employee Notice"
                                                                  " has been sent the Employee.")
        except sqlite3.Error as error:
            messagebox.showerror("Error", str(error))


def show_employee_notice_records():
    # Create a new window for displaying records
    employee_notice_records_window = tk.Toplevel()
    employee_notice_records_window.title("Employee Notice Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(employee_notice_records_window, columns=("Notice ID", "Employee ID", "Title", "Content",
                                                                 "Published Date"))
    tree.heading("#0", text="Employee Notice Record")
    tree.heading("#1", text="Notice ID")
    tree.heading("#2", text="Employee ID")
    tree.heading("#3", text="Title")
    tree.heading("#4", text="Content")
    tree.heading("#5", text="Published Date")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(employee_notice_records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch Employee records from the database
    try:
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee_notice")
        employee_records = cursor.fetchall()
        conn.close()

        # Insert Employee records into the treeview
        for record in employee_records:
            formatted_content = record[3].replace("\n", " | ")  # Replace line breaks with a separator
            tree.insert("", "end", values=(record[0], record[1], record[2], formatted_content, record[4]))

        # Adjust column widths based on content
        for col in tree["columns"]:
            tree.column(col, width=200)  # Adjust the width as needed

        tree.pack(fill=tk.BOTH, expand=True)
    except sqlite3.Error as error:
        messagebox.showerror("Error", str(error))


def delete_employee_notice_record(conn):
    # Create a Tkinter window
    notice_window = tk.Tk()
    notice_window.withdraw()  # Hide the main window

    # Prompt the user for emp_notice_id using simpledialog
    emp_notice_id = simpledialog.askinteger("Input", "Enter Employee Notice ID:")

    if emp_notice_id is not None:
        confirmation = messagebox.askquestion("Delete Employee Notice",
                                              f"Are you sure you want to delete Employee Notice ID"
                                              f" {emp_notice_id} from the Employee Notices?")
        if confirmation == 'yes':
            cursor = conn.cursor()

            # Delete the employee notice record for the specified emp_notice_id
            try:
                cursor.execute("DELETE FROM employee_notice WHERE emp_notice_id = ?", (emp_notice_id,))

                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Deletion Successful", f"Employee notice with ID {emp_notice_id}"
                                                               f" has been deleted.")
                else:
                    messagebox.showerror("Invalid Input", "No such Course record.")
            except sqlite3.Error as error:
                conn.rollback()  # Rollback the transaction in case of an error
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showinfo("Deletion Canceled", "Employee notice has not been deleted.")
    else:
        messagebox.showinfo("Invalid Input", "Please provide a valid Employee Notice ID.")

    # Close the Tkinter window
    notice_window.destroy()


def delete_all_employee_notice_records(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employee_notice")
    count = cursor.fetchone()[0]

    if count == 0:
        messagebox.showerror("No Records", "There are no Employee Notice records to delete.")
    else:
        confirmation = messagebox.askquestion("Delete All Records",
                                              "Are you sure you want to delete all Employee notice records?")
        if confirmation == 'yes':
            try:
                cursor.execute("DELETE FROM employee_notice")
                conn.commit()
                messagebox.showinfo("Deletion Successful", "All Employee  notice records have been deleted.")
            except sqlite3.Error as error:
                conn.rollback()
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "No Employee Notice records have been deleted.")
