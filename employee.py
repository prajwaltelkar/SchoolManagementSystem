import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter import messagebox


class Employee:
    def __init__(self):
        # Create a new window for employee registration
        self.employee_window = tk.Toplevel()
        self.employee_window.title("Register Employee")

        # Create and pack entry fields for employee attributes
        employee_id_label = tk.Label(self.employee_window, text="Employee ID (Primary Key):")
        employee_id_label.pack()
        self.employee_id_entry = tk.Entry(self.employee_window)
        self.employee_id_entry.pack()

        first_name_label = tk.Label(self.employee_window, text="First Name:")
        first_name_label.pack()
        self.first_name_entry = tk.Entry(self.employee_window)
        self.first_name_entry.pack()

        last_name_label = tk.Label(self.employee_window, text="Last Name:")
        last_name_label.pack()
        self.last_name_entry = tk.Entry(self.employee_window)
        self.last_name_entry.pack()

        dob_label = tk.Label(self.employee_window, text="Date of Birth:")
        dob_label.pack()
        self.dob_entry = tk.Entry(self.employee_window)
        self.dob_entry.pack()

        address_label = tk.Label(self.employee_window, text="Address:")
        address_label.pack()
        self.address_entry = tk.Entry(self.employee_window)
        self.address_entry.pack()

        contact_number_label = tk.Label(self.employee_window, text="Contact Number:")
        contact_number_label.pack()
        self.contact_number_entry = tk.Entry(self.employee_window)
        self.contact_number_entry.pack()

        role_label = tk.Label(self.employee_window, text="Role (Teacher/Staff):")
        role_label.pack()
        self.role_entry = tk.Entry(self.employee_window)
        self.role_entry.pack()

        # Create the "Save" button and bind it to the save_employee method
        self.save_button = tk.Button(self.employee_window, text="Save", command=self.save_employee)
        self.save_button.pack()

    def save_employee(self):
        employee_id = self.employee_id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        dob = self.dob_entry.get()
        address = self.address_entry.get()
        contact_number = self.contact_number_entry.get()
        role = self.role_entry.get()

        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO employees (
                            employee_id, first_name, last_name, dob, address, contact_number, role
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (employee_id, first_name, last_name, dob, address,
                        contact_number, role))

        self.employee_window.destroy()
        messagebox.showinfo("Successful", "Employee Created!")

        conn.commit()
        conn.close()


def show_employee_records():
    # Create a new window for displaying records
    records_window = tk.Toplevel()
    records_window.title("Employee Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(records_window, columns=("Employee ID", "First Name", "Last Name", "DOB", "Address",
                                                 "Contact Number", "Role"))
    tree.heading("#0", text="Employee Records")
    tree.heading("#1", text="Employee ID")
    tree.heading("#2", text="First Name")
    tree.heading("#3", text="Last Name")
    tree.heading("#4", text="Date of Birth")
    tree.heading("#5", text="Address")
    tree.heading("#6", text="Contact Number")
    tree.heading("#7", text="Role")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch employee records from the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employee_records = cursor.fetchall()
    conn.close()

    # Insert employee records into the treeview
    for record in employee_records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_all_employee_records():
    confirmation = messagebox.askquestion("Delete All Records",
                                          "Are you sure you want to delete all employee records?")
    if confirmation == 'yes':
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees")
        conn.commit()
        messagebox.showinfo("Deletion Successful", "All employee records have been deleted.")
