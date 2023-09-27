import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import tkinter.font as tkfont


class Fee:
    def __init__(self):
        self.fee_window = tk.Toplevel()
        self.fee_window.title("Register fee")

        # Create and pack entry fields for fee attributes
        self.student_id_label = tk.Label(self.fee_window, text="Student ID:")
        self.student_id_label.pack()
        self.student_id_entry = tk.Entry(self.fee_window)
        self.student_id_entry.pack()

        self.amount_label = tk.Label(self.fee_window, text="Fee Amount Paid:")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self.fee_window)
        self.amount_entry.pack()

        self.payment_date_label = tk.Label(self.fee_window, text="Payment Date:")
        self.payment_date_label.pack()
        self.payment_date_entry = tk.Entry(self.fee_window)
        self.payment_date_entry.pack()

        self.payment_status_label = tk.Label(self.fee_window, text="Payment Status:")
        self.payment_status_label.pack()
        self.payment_status_entry = tk.Entry(self.fee_window)
        self.payment_status_entry.pack()

        self.academic_year_label = tk.Label(self.fee_window, text="Academic Year:")
        self.academic_year_label.pack()
        self.academic_year_entry = tk.Entry(self.fee_window)
        self.academic_year_entry.pack()

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.fee_window, text="Save", command=self.save_fee)
        self.save_button.pack()

    def save_fee(self):
        # Retrieve data from entry fields
        student_id = self.student_id_entry.get()
        amount = self.amount_entry.get()
        payment_date = self.payment_date_entry.get()
        payment_status = self.payment_status_entry.get()
        academic_year = self.academic_year_entry.get()

        # Insert student information into the database
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO fee_payments (
                                student_id, amount, payment_date, payment_status, academic_year
                            ) VALUES (?, ?, ?, ?, ?)''',
                       (student_id, amount, payment_date, payment_status, academic_year))

        conn.commit()
        conn.close()

        # Close the student registration window
        self.fee_window.destroy()
        messagebox.showinfo("Fee Status Updated", "Fee status has been updated for the student.")


def show_fee_records():
    # Create a new window for displaying records
    fee_records_window = tk.Toplevel()
    fee_records_window.title("Student Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(fee_records_window, columns=("Payment ID", "Student ID", "Amount", "Payment Date",
                                                     "Payment Status", "Academic Year"))
    tree.heading("#0", text="Record")
    tree.heading("#1", text="Payment ID")
    tree.heading("#2", text="Student ID")
    tree.heading("#3", text="Amount")
    tree.heading("#4", text="Payment Date")
    tree.heading("#5", text="Payment Status")
    tree.heading("#6", text="Academic Year")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(fee_records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch student records from the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fee_payments")
    student_records = cursor.fetchall()
    conn.close()

    # Insert student records into the treeview
    for record in student_records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_all_fee_records():
    confirmation = messagebox.askquestion("Delete All Records",
                                          "Are you sure you want to delete all student fee records?")
    if confirmation == 'yes':
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM fee_payments")
        conn.commit()
        messagebox.showinfo("Deletion Successful", "All student fee records have been deleted.")
