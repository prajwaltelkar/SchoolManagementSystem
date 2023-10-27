import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import sqlite3
import tkinter.font as tkfont


class Fee:
    def __init__(self, db_connection):
        self.fee_window = tk.Toplevel()
        self.fee_window.title("Register fee")

        self.conn = db_connection

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
        cursor = self.conn.cursor()
        try:
            cursor.execute('''INSERT INTO fee_payments (
                                    student_id, amount, payment_date, payment_status, academic_year
                                ) VALUES (?, ?, ?, ?, ?)''',
                           (student_id, amount, payment_date, payment_status, academic_year))

            self.conn.commit()

            # Close the student registration window
            self.fee_window.destroy()
            messagebox.showinfo("Fee Status Updated", "Fee status has been updated for the student.")
        except sqlite3.Error as error:
            messagebox.showerror("Error", str(error))


def show_fee_records():
    # Create a new window for displaying records
    fee_records_window = tk.Toplevel()
    fee_records_window.title("Fee Payments Database")

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
    try:
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

    except sqlite3.Error as error:
        messagebox.showerror("Error", str(error))


def delete_fee(conn):
    # Create a Tkinter window
    fee_window = tk.Tk()
    fee_window.withdraw()  # Hide the main window

    # Prompt the user for payment_id using simpledialog
    payment_id = simpledialog.askinteger("Input", "Enter Payment ID:")

    if payment_id is not None:
        confirmation = messagebox.askquestion("Delete Fee Payment",
                                              f"Are you sure you want to delete Payment ID {payment_id} from the Fee Payments?")
        if confirmation == 'yes':
            cursor = conn.cursor()

            # Delete the fee payment record for the specified payment_id
            try:
                cursor.execute("DELETE FROM fee_payments WHERE payment_id = ?", (payment_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Deletion Successful",
                                        f"Fee payment record with ID {payment_id} has been deleted.")
                else:
                    messagebox.showerror("Invalid Input", "No such Fee record.")
            except sqlite3.Error as error:
                conn.rollback()  # Rollback the transaction in case of an error
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showinfo("Deletion Canceled", "Fee payment record has not been deleted.")
    else:
        messagebox.showinfo("Invalid Input", "Please provide a valid Payment ID.")

    # Close the Tkinter window
    fee_window.destroy()


def delete_all_fee_records(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM fee_payments")
    count = cursor.fetchone()[0]

    if count == 0:
        messagebox.showerror("No Records", "There are no Course records to delete.")
    else:
        confirmation = messagebox.askquestion("Delete All Records",
                                              "Are you sure you want to delete all student fee records?")
        if confirmation == 'yes':
            try:
                cursor.execute("DELETE FROM fee_payments")
                conn.commit()
                messagebox.showinfo("Deletion Successful", "All student fee records have been deleted.")
            except sqlite3.Error as error:
                conn.rollback()
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "No Fee records have been deleted.")


# Function to update fee information in a pop-up window
def update_fee_records(conn):
    update_fee_window = tk.Toplevel()
    update_fee_window.title("Update Fee Payments")

    # Payment ID and Student ID input fields
    payment_id_label = tk.Label(update_fee_window, text="Enter Payment ID:")
    student_id_label = tk.Label(update_fee_window, text="Enter Student ID:")
    payment_id_label.grid(row=0, column=0)
    student_id_label.grid(row=1, column=0)
    payment_id_entry = tk.Entry(update_fee_window)
    student_id_entry = tk.Entry(update_fee_window)
    payment_id_entry.grid(row=0, column=1)
    student_id_entry.grid(row=1, column=1)
    get_info_button = tk.Button(update_fee_window, text="Get Fee Info",
                                command=lambda: update_fee_info(conn, payment_id_entry, student_id_entry))
    get_info_button.grid(row=0, column=2, columnspan=2)


def update_fee_info(conn, payment_id_entry, student_id_entry):
    try:
        # Get the payment ID and student ID from the user
        payment_id = int(payment_id_entry.get())
        student_id = int(student_id_entry.get())

        # Check if the payment and student IDs exist in the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fee_payments WHERE payment_id = ? AND student_id = ?", (payment_id, student_id))
        fee_data = cursor.fetchone()

        if fee_data:
            # Create a separate pop-up window for displaying and updating the current information
            current_info_window = tk.Toplevel()
            current_info_window.title(
                f"Update Fee Payment Information (Payment ID {payment_id}, Student ID {student_id})")

            # Labels (keys) next to the white space for updated information
            amount_label = tk.Label(current_info_window, text="Amount:")
            payment_date_label = tk.Label(current_info_window, text="Payment Date (dd-mm-yyyy):")
            payment_status_label = tk.Label(current_info_window, text="Payment Status:")
            academic_year_label = tk.Label(current_info_window, text="Academic Year:")

            amount_label.grid(row=0, column=0, sticky='e')
            payment_date_label.grid(row=1, column=0, sticky='e')
            payment_status_label.grid(row=2, column=0, sticky='e')
            academic_year_label.grid(row=3, column=0, sticky='e')

            # Entry fields for updated information
            new_amount_entry = tk.Entry(current_info_window, width=30)
            new_payment_date_entry = tk.Entry(current_info_window, width=30)
            new_payment_status_entry = tk.Entry(current_info_window, width=30)
            new_academic_year_entry = tk.Entry(current_info_window, width=30)

            new_amount_entry.grid(row=0, column=1, pady=5)
            new_payment_date_entry.grid(row=1, column=1, pady=5)
            new_payment_status_entry.grid(row=2, column=1, pady=5)
            new_academic_year_entry.grid(row=3, column=1, pady=5)

            # Update button in the pop-up window
            update_button = tk.Button(current_info_window, text="Update Information",
                                      command=lambda: [
                                          update_fee_info_in_database(payment_id, student_id, new_amount_entry.get(),
                                                                  new_payment_date_entry.get(),
                                                                  new_payment_status_entry.get(),
                                                                  new_academic_year_entry.get(), conn),
                                          current_info_window.destroy()])  # Close the window
            update_button.grid(row=4, column=0, columnspan=2, pady=10)

            # Populate the input fields with the current information
            new_amount_entry.insert(0, fee_data[2])
            new_payment_date_entry.insert(0, fee_data[3])
            new_payment_status_entry.insert(0, fee_data[4])
            new_academic_year_entry.insert(0, fee_data[5])

        else:
            messagebox.showerror("Error", "Payment with given ID not found in the database.")

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid Payment and Student IDs.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to update fee information in the database
def update_fee_info_in_database(payment_id, student_id, new_amount, new_payment_date, new_payment_status, new_academic_year,
                            conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE fee_payments SET amount = ?, payment_date = ?, payment_status = ?, academic_year = ? "
            "WHERE payment_id = ? AND student_id = ?",
            (new_amount, new_payment_date, new_payment_status, new_academic_year, payment_id, student_id))
        conn.commit()
        messagebox.showinfo("Success", "Fee information updated successfully")
    except sqlite3.Error as e:
        conn.rollback()  # Rollback the transaction
        messagebox.showerror("Error", f"Error updating fee information: {str(e)}")
