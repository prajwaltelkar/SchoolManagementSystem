import sqlite3
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox, simpledialog


class ClassCourses:
    def __init__(self, db_connection):
        self.window = tk.Toplevel()
        self.window.title("Assign courses to class")

        self.conn = db_connection

        # Create and pack entry fields for class attributes
        self.class_id_label = tk.Label(self.window, text="Class ID")
        self.class_id_label.pack()
        self.class_id_entry = tk.Entry(self.window)
        self.class_id_entry.pack()

        self.course_id_label = tk.Label(self.window, text="Course ID:")
        self.course_id_label.pack()
        self.course_id_entry = tk.Entry(self.window)
        self.course_id_entry.pack()

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.window, text="Save", command=self.save)
        self.save_button.pack()

    def save(self):
        cursor = self.conn.cursor()

        class_id = self.class_id_entry.get()
        course_id = self.course_id_entry.get()

        try:
            cursor.execute("INSERT INTO class_courses (class_id, course_id) VALUES (?, ?)",
                           (class_id, course_id))
            self.conn.commit()
            messagebox.showinfo("Successful", "Course-Class Assigned!")
        except sqlite3.Error as error:
            messagebox.showerror("Error", str(error))

        self.window.destroy()


def show_class_courses_records():
    # Create a new window for displaying records
    records_window = tk.Toplevel()
    records_window.title("Class Course Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(records_window, columns=("Class ID", "Class Name"))
    tree.heading("#0", text="Class Courses Record")
    tree.heading("#1", text="Class ID")
    tree.heading("#2", text="Course ID")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch Class records from the database
    try:
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM class_courses")
        records = cursor.fetchall()
        conn.close()
    except sqlite3.Error as error:
        messagebox.showerror("Error", str(error))

    # Insert Class records into the treeview
    for record in records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_class_course_record(conn):
    # Create a Tkinter window
    class_course_window = tk.Tk()
    class_course_window.withdraw()  # Hide the main window

    # Prompt the user for class_id and course_id using simpledialog
    class_id = simpledialog.askinteger("Input", "Enter Class ID:")
    course_id = simpledialog.askinteger("Input", "Enter Course ID:")

    if class_id is not None and course_id is not None:
        confirmation = messagebox.askquestion("Delete Class-Course Association",
                                              f"Are you sure you want to delete the Class ID-"
                                              f"{class_id} Course ID-{course_id} association from the"
                                              f" Class-Course associations?")
        if confirmation == 'yes':
            cursor = conn.cursor()

            # Delete the class_course record for the specified class_id and course_id
            try:
                cursor.execute("DELETE FROM class_courses WHERE class_id = ? AND course_id = ?",
                               (class_id, course_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Deletion Successful", f"Class-Course association for Class ID"
                                                               f" {class_id} and Course ID {course_id} has been deleted.")
                else:
                    messagebox.showerror("Invalid Input", "No such Class-Course record.")
            except sqlite3.Error as error:
                conn.rollback()  # Rollback the transaction in case of an error
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "Class-Course association has not been deleted.")
    else:
        messagebox.showerror("Invalid Input", "Please provide valid Class ID and Course ID.")

    # Close the Tkinter window
    class_course_window.destroy()


def delete_all_class_courses_records(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM class_courses")
    count = cursor.fetchone()[0]

    if count == 0:
        messagebox.showerror("No Records", "There are no Class-Course records to delete.")
    else:
        confirmation = messagebox.askquestion("Delete All Records",
                                              "Are you sure you want to delete all Class records?")
        if confirmation == 'yes':
            try:
                cursor.execute("DELETE FROM class_courses")
                conn.commit()
                messagebox.showinfo("Deletion Successful", "All Class records have been deleted.")
            except sqlite3.Error as error:
                conn.rollback()
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "No Class-Course records have been deleted.")


# Login authentication
def authenticate_student(student_id, student_password):
    try:
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        # Execute a query to check if the student ID and password match
        cursor.execute(
            "SELECT COUNT(*) FROM students WHERE student_id = CAST(:student_id AS INTEGER) AND password = :password",
            {"student_id": student_id, "password": student_password})

        result = cursor.fetchone()
        conn.close()

        # If the query result is 1, it means the student with the provided ID and password exists
        return result[0] == 1

    except sqlite3.Error as error:
        messagebox.showerror("Error", str(error))


def center_window(root, width, height):
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window's geometry to be centered on the screen
    root.geometry(f"{width}x{height}+{x}+{y}")


class EmployeeClassAssignment:
    def __init__(self, db_connection):
        self.window = tk.Toplevel()
        self.window.title("Assign Employee to Class")

        self.conn = db_connection

        # Create and pack entry fields for assignment attributes
        self.employee_id_label = tk.Label(self.window, text="Employee ID")
        self.employee_id_label.pack()
        self.employee_id_entry = tk.Entry(self.window)
        self.employee_id_entry.pack()

        self.class_id_label = tk.Label(self.window, text="Class ID:")
        self.class_id_label.pack()
        self.class_id_entry = tk.Entry(self.window)
        self.class_id_entry.pack()

        # Create the "Assign" button and bind it to the assign_employee_to_class method
        self.assign_button = tk.Button(self.window, text="Assign", command=self.assign_employee_to_class)
        self.assign_button.pack()

    def assign_employee_to_class(self):
        cursor = self.conn.cursor()

        employee_id = self.employee_id_entry.get()
        class_id = self.class_id_entry.get()

        # Check if the employee with the given ID exists and is a teacher
        cursor.execute("SELECT * FROM employees WHERE employee_id = ? AND role = 'Teacher'", (employee_id,))
        employee = cursor.fetchone()

        if employee:
            # If the employee is a teacher, assign them to the class
            try:
                cursor.execute("INSERT INTO employee_class (employee_id, class_id) VALUES (?, ?)",
                               (employee_id, class_id))
                self.conn.commit()
                self.window.destroy()
                messagebox.showinfo("Successful", "Employee-Class Assignment Successful!")
            except sqlite3.Error as error:
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Error", "Employee not found or not a teacher.")


def show_employee_class_records():
    # Create a new window for displaying records
    records_window = tk.Toplevel()
    records_window.title("Employee Class Assignment Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(records_window, columns=("Employee ID", "Class ID"))
    tree.heading("#0", text="Employee-Class Assignment Record")
    tree.heading("#1", text="Employee ID")
    tree.heading("#2", text="Class ID")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch employee-class assignment records from the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee_class")
    records = cursor.fetchall()
    conn.close()

    # Insert employee-class assignment records into the treeview
    for record in records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_all_employee_class_records(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employee_class")
    count = cursor.fetchone()[0]

    if count == 0:
        messagebox.showerror("No Records", "There are no Employee-Class record to delete.")
    else:
        confirmation = messagebox.askquestion("Delete All Records",
                                              "Are you sure you want to delete all Employee-Class Assignment records?")
        if confirmation == 'yes':
            try:
                cursor.execute("DELETE FROM employee_class")
                conn.commit()
                messagebox.showinfo("Deletion Successful", "All Employee-Class Assignment records have been deleted.")
            except sqlite3.Error as error:
                conn.rollback()
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "No Employee-Class records have been deleted.")


def delete_employee_class_record(conn):
    # Create a Tkinter window
    employee_class_window = tk.Tk()
    employee_class_window.withdraw()  # Hide the main window

    # Prompt the user for employee_id and class_id using simpledialog
    employee_id = simpledialog.askinteger("Input", "Enter Employee ID:")
    class_id = simpledialog.askinteger("Input", "Enter Class ID:")

    if employee_id is not None and class_id is not None:
        confirmation = messagebox.askquestion("Delete Employee-Class Assignment",
                                              f"Are you sure you want to delete the Employee ID-"
                                              f"{employee_id} Class ID-{class_id} assignment from the"
                                              f" Employee-Class assignments?")
        if confirmation == 'yes':
            cursor = conn.cursor()

            # Delete the employee_class assignment record for the specified employee_id and class_id
            try:
                cursor.execute("DELETE FROM employee_class WHERE employee_id = ? AND class_id = ?",
                               (employee_id, class_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Deletion Successful", f"Employee-Class assignment for Employee ID"
                                                               f" {employee_id} and Class ID {class_id} has been deleted.")
                else:
                    messagebox.showerror("Invalid Input", "No such Employee-Class record.")
            except sqlite3.Error as error:
                conn.rollback()  # Rollback the transaction in case of an error
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "Employee-Class assignment has not been deleted.")
    else:
        messagebox.showerror("Invalid Input", "Please provide valid Employee ID and Class ID.")

    # Close the Tkinter window
    employee_class_window.destroy()


# Function to update class_courses information in a pop-up window
def update_class_courses_records(conn):
    update_class_courses_window = tk.Toplevel()
    update_class_courses_window.title("Update Class Courses")

    # Class ID and Course ID input fields
    class_id_label = tk.Label(update_class_courses_window, text="Enter Class ID:")
    course_id_label = tk.Label(update_class_courses_window, text="Enter Course ID:")
    class_id_label.grid(row=0, column=0)
    course_id_label.grid(row=1, column=0)
    class_id_entry = tk.Entry(update_class_courses_window)
    course_id_entry = tk.Entry(update_class_courses_window)
    class_id_entry.grid(row=0, column=1)
    course_id_entry.grid(row=1, column=1)
    get_info_button = tk.Button(update_class_courses_window, text="Get Class Courses Info",
                                command=lambda: update_class_courses_info(conn, class_id_entry, course_id_entry))
    get_info_button.grid(row=0, column=2, columnspan=2)


def update_class_courses_info(conn, class_id_entry, course_id_entry):
    try:
        # Get the class ID and course ID from the user
        class_id = int(class_id_entry.get())
        course_id = int(course_id_entry.get())

        # Check if the class and course IDs exist in the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM class WHERE class_id = ?", (class_id,))
        class_data = cursor.fetchone()
        cursor.execute("SELECT * FROM course WHERE course_id = ?", (course_id,))
        course_data = cursor.fetchone()

        if class_data and course_data:
            # Create a separate pop-up window for displaying and updating the current information
            current_info_window = tk.Toplevel()
            current_info_window.title(f"Update Class Courses Information (Class ID {class_id}, Course ID {course_id})")

            # Labels (keys) next to the white space for updated information
            # You can add more fields as needed for the class_courses table
            label1 = tk.Label(current_info_window, text="Class ID:")
            label2 = tk.Label(current_info_window, text="Course ID:")
            label1.grid(row=0, column=0, sticky='e')
            label2.grid(row=1, column=0, sticky='e')

            # Entry fields for updated information
            entry1 = tk.Entry(current_info_window, width=30)
            entry2 = tk.Entry(current_info_window, width=30)
            entry1.grid(row=0, column=1, pady=5)
            entry2.grid(row=1, column=1, pady=5)

            # Update button in the pop-up window
            update_button = tk.Button(current_info_window, text="Update Information",
                                      command=lambda: [
                                          update_class_courses_info_in_database(class_id, course_id, entry1.get(),
                                                                                entry2.get(), conn),
                                          current_info_window.destroy()])  # Close the window
            update_button.grid(row=2, column=0, columnspan=2, pady=10)

            # Populate the input fields with the current information
            cursor.execute("SELECT class_id, course_id FROM class_courses WHERE class_id = ? AND course_id = ?",
                           (class_id, course_id))
            current_info = cursor.fetchone()
            if current_info:
                entry1.insert(0, current_info[0])
                entry2.insert(0, current_info[1])

        else:
            messagebox.showerror("Error", "Class or Course not found in the database.")

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid Class and Course IDs.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to update class_courses information in the database
def update_class_courses_info_in_database(class_id, course_id, field1, field2, conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE class_courses SET class_id = ?, course_id = ? WHERE class_id = ? AND course_id = ?",
            (field1, field2, class_id, course_id))
        conn.commit()
        messagebox.showinfo("Success", "Class Courses information updated successfully")
    except sqlite3.Error as e:
        conn.rollback()  # Rollback the transaction
        messagebox.showerror("Error", f"Error updating class_courses information: {str(e)}")
