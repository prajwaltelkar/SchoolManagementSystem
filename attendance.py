import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.font as tkfont
from tkinter import messagebox
from tkinter import simpledialog


class AttendanceSystem:
    def __init__(self, db_connection, employee_id):

        # Initialize tkinter
        self.employee_id = employee_id
        self.conn = db_connection
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
        self.date_label = tk.Label(self.attendance_window, text="Attendance Date (DD-MM-YYYY):")
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
        self.attendance_label = tk.Label(self.attendance_window, text="Mark Attendance after selecting the student:")
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
        try:
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
        except sqlite3.Error as error:
            messagebox.showerror("Error", str(error))

    def mark_attendance(self):
        try:
            selected_class = self.class_var.get()
            date = self.date_var.get()
            selected_student = self.student_listbox.get(tk.ACTIVE)
            student_id = self.student_ids[self.student_names.index(selected_student)]
            status = self.status_var.get()

            # Check if the logged-in employee is authorized to take attendance for the selected class
            authorized = self.is_employee_authorized(self.employee_id, selected_class)

            if authorized:
                # Insert attendance data into the database
                self.cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                                    (student_id, date, status))
                self.conn.commit()
                messagebox.showinfo("Attendance Marked", f"Attendance for {selected_student} marked"
                                                         f" successfully.")
            else:
                messagebox.showinfo("Authorization Error", "You are not authorized to mark attendance"
                                                           " for this class.")
        except sqlite3.Error as error:
            messagebox.showerror("Error", str(error))

    # Function to check if the employee is authorized to take attendance for the selected class
    def is_employee_authorized(self, employee_id, selected_class):
        try:
            class_id = self.cursor.execute("SELECT class_id FROM class WHERE class_name=?",
                                           (selected_class,)).fetchone()
            if class_id:
                class_id = class_id[0]
                # Check if there is a record in the employee_class table with the given employee_id and class_id
                record_exists = self.cursor.execute("SELECT * FROM employee_class WHERE employee_id=? AND class_id=?",
                                                    (employee_id, class_id)).fetchone()
                return bool(record_exists)
            return False
        except sqlite3.Error as error:
            messagebox.showerror("Error", str(error))


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
        self.date_label = tk.Label(self.attendance_view_window, text="Attendance Date (DD-MM-YYYY):")
        self.date_label.pack()

        # Create an entry field for attendance date
        self.date_entry = tk.Entry(self.attendance_view_window, textvariable=self.date_var)
        self.date_entry.pack()

        # Create a button to view attendance
        self.view_attendance_button = tk.Button(self.attendance_view_window, text="View Attendance",
                                                command=self.show_attendance)
        self.view_attendance_button.pack()

    def show_attendance(self):
        try:
            selected_class = self.class_var.get()
            selected_date = self.date_var.get()

            class_id = \
            self.cursor.execute("SELECT class_id FROM class WHERE class_name=?", (selected_class,)).fetchone()[0]
            attendance_data = self.cursor.execute(
                "SELECT students.first_name, students.last_name, attendance.status FROM students JOIN attendance ON students.student_id = attendance.student_id WHERE students.class_id=? AND attendance.date=?",
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

        except sqlite3.Error as error:
            self.conn.rollback()
            messagebox.showerror("Error", str(error))


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
    try:
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

    except sqlite3.Error as error:
        messagebox.showerror("Error", str(error))


def delete_attendance(conn):
    attendance_window = tk.Tk()
    attendance_window.withdraw()  # Hide the main window

    # Prompt the user for student_id and date using simpledialog
    student_id = simpledialog.askinteger("Input", "Enter Student ID:")
    date = simpledialog.askstring("Input", "Enter Date (DD-MM-YYYY):")

    if student_id is not None and date is not None:
        confirmation = messagebox.askquestion("Delete Attendance",
                                              f"Are you sure you want to delete {student_id}"
                                              f" Attendance record on {date}?")
        if confirmation == 'yes':
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM attendance WHERE student_id = ? AND date = ?",
                               (student_id, date))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Deletion Successful", "Attendance record has been deleted.")
                else:
                    messagebox.showerror("Invalid Input", "No such Attendance record.")
            except sqlite3.Error as error:
                conn.rollback()  # Rollback the transaction in case of an error
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "Attendance record has not been deleted.")
    else:
        messagebox.showerror("Invalid Input", "Please provide a valid Student ID and Date.")

    # Close the Tkinter window
    attendance_window.destroy()


def delete_all_attendance_records(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM attendance")
    count = cursor.fetchone()[0]

    if count == 0:
        messagebox.showerror("No Records", "There are no Attendance records to delete.")
    else:
        confirmation = messagebox.askquestion("Delete All Records",
                                              "Are you sure you want to delete all Attendance records?")
        if confirmation == 'yes':
            try:
                cursor.execute("DELETE FROM attendance")
                conn.commit()
                messagebox.showinfo("Deletion Successful", "All Attendance records have been deleted.")
            except sqlite3.Error as error:
                conn.rollback()
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "No Attendance records have been deleted.")


# Function to update attendance information in a pop-up window
def update_attendance_record(conn):
    update_attendance_window = tk.Toplevel()
    update_attendance_window.title("Update Attendance")

    # Student ID and Date input fields
    student_id_label = tk.Label(update_attendance_window, text="Enter Student ID:")
    date_label = tk.Label(update_attendance_window, text="Enter Date (dd-mm-yyyy):")
    student_id_label.grid(row=0, column=0)
    date_label.grid(row=1, column=0)
    student_id_entry = tk.Entry(update_attendance_window)
    date_entry = tk.Entry(update_attendance_window)
    student_id_entry.grid(row=0, column=1)
    date_entry.grid(row=1, column=1)
    get_info_button = tk.Button(update_attendance_window, text="Get Attendance Info",
                                command=lambda: update_attendance_info(conn, student_id_entry, date_entry))
    get_info_button.grid(row=0, column=2, columnspan=2)


def update_attendance_info(conn, student_id_entry, date_entry):
    try:
        # Get the student ID and date from the user
        student_id = int(student_id_entry.get())
        date = date_entry.get()

        # Check if the student ID exists in the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        student_data = cursor.fetchone()

        if student_data:
            # Create a separate pop-up window for displaying and updating the current information
            current_info_window = tk.Toplevel()
            current_info_window.title(f"Update Attendance Information (Student ID {student_id}, Date {date})")

            # Labels (keys) next to the white space for updated information
            status_label = tk.Label(current_info_window, text="Attendance Status:")
            status_label.grid(row=0, column=0, sticky='e')

            # Entry field for updated information
            new_status_entry = tk.Entry(current_info_window, width=30)
            new_status_entry.grid(row=0, column=1, pady=5)

            # Update button in the pop-up window
            update_button = tk.Button(current_info_window, text="Update Information",
                                      command=lambda: [
                                          update_attendance_info_in_database(student_id, date, new_status_entry.get(), conn),
                                          current_info_window.destroy()])  # Close the window
            update_button.grid(row=1, column=0, columnspan=2, pady=10)

            # Populate the input field with the current information
            cursor.execute("SELECT status FROM attendance WHERE student_id = ? AND date = ?", (student_id, date))
            current_status = cursor.fetchone()
            if current_status:
                new_status_entry.insert(0, current_status[0])

        else:
            messagebox.showerror("Error", "Student with given ID not found in the database.")

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid Student ID and Date.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to update attendance information in the database
def update_attendance_info_in_database(student_id, date, new_status, conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE attendance SET status = ? WHERE student_id = ? AND date = ?",
            (new_status, student_id, date))
        conn.commit()
        messagebox.showinfo("Success", "Attendance information updated successfully")
    except sqlite3.Error as e:
        conn.rollback()  # Rollback the transaction
        messagebox.showerror("Error", f"Error updating attendance information: {str(e)}")
