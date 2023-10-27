import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter import messagebox, simpledialog


class Course:
    def __init__(self, db_connection):
        # Create a new window for employee registration
        self.course_window = tk.Toplevel()
        self.course_window.title("Create course")

        self.conn = db_connection

        # Create and pack entry fields for course attributes
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

        employee_id_label = tk.Label(self.course_window, text="Employee ID:")
        employee_id_label.pack()
        self.employee_id_entry = tk.Entry(self.course_window)
        self.employee_id_entry.pack()

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.course_window, text="Save", command=self.save_course)
        self.save_button.pack()

    def save_course(self):
        try:
            cursor = self.conn.cursor()

            course_id = self.course_id_entry.get()
            course_name = self.course_name_entry.get()
            course_description = self.course_description_entry.get()
            employee_id = self.employee_id_entry.get()

            cursor.execute('''INSERT INTO course (
                                course_id, course_name, course_description, employee_id
                            ) VALUES (?, ?, ?, ?)''',
                           (course_id, course_name, course_description, employee_id))

            self.course_window.destroy()
            messagebox.showinfo("Successful", "Course Created!")

            self.conn.commit()
        except sqlite3.Error as error:
            messagebox.showerror("Error", str(error))


def show_course_records():
    # Create a new window for displaying records
    course_records_window = tk.Toplevel()
    course_records_window.title("Course Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(course_records_window, columns=("Course ID", "Course Name", "Course Description", "Employee ID"))
    tree.heading("#0", text="Course Record")
    tree.heading("#1", text="Course ID")
    tree.heading("#2", text="Course Name")
    tree.heading("#3", text="Course Description")
    tree.heading("#4", text="Employee ID")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(course_records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch Employee records from the database
    try:
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM course")
        employee_records = cursor.fetchall()
        conn.close()

        # Insert Employee records into the treeview
        for record in employee_records:
            tree.insert("", "end", values=record)

        # Adjust column widths based on content
        for col in tree["columns"]:
            tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

        tree.pack(fill=tk.BOTH, expand=True)

    except sqlite3.Error as error:
        messagebox.showerror("Error", str(error))


def delete_course(conn):
    # Create a Tkinter window
    course_window = tk.Tk()
    course_window.withdraw()  # Hide the main window

    # Prompt the user for course_id using simpledialog
    course_id = simpledialog.askinteger("Input", "Enter Course ID:")

    if course_id is not None:
        confirmation = messagebox.askquestion("Delete Course",
                                              f"Are you sure you want to delete Course ID "
                                              f" {course_id} from the Courses?")
        if confirmation == 'yes':
            cursor = conn.cursor()

            # Delete the course record for the specified course_id
            try:
                cursor.execute("DELETE FROM course WHERE course_id = ?", (course_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Deletion Successful", f"Course record with ID "
                                                               f" {course_id} has been deleted.")
                else:
                    messagebox.showerror("Invalid Input", "No such Course record.")
            except sqlite3.Error as error:
                conn.rollback()  # Rollback the transaction in case of an error
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "Course record has not been deleted.")
    else:
        messagebox.showerror("Invalid Input", "Please provide a valid Course ID.")

    # Close the Tkinter window
    course_window.destroy()


def delete_all_course_records(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM course")
    count = cursor.fetchone()[0]

    if count == 0:
        messagebox.showerror("No Records", "There are no Course records to delete.")
    else:
        confirmation = messagebox.askquestion("Delete All Records",
                                              "Are you sure you want to delete all Course records?")
        if confirmation == 'yes':
            try:
                cursor.execute("DELETE FROM course")
                conn.commit()
                messagebox.showinfo("Deletion Successful", f"{count} Course records have been deleted.")
            except sqlite3.Error as error:
                conn.rollback()
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "No Course records have been deleted.")


# Function to update course information
def update_course_record(conn):
    # Create a new window for course information update
    update_course_window = tk.Toplevel()
    update_course_window.title("Update Course Details")

    # Course ID input field
    course_id_label = tk.Label(update_course_window, text="Enter Course ID:")
    course_id_label.grid(row=0, column=0)
    course_id_entry = tk.Entry(update_course_window)
    course_id_entry.grid(row=0, column=1)
    get_info_button = tk.Button(update_course_window, text="Get Course Info",
                                command=lambda: update_course_info(conn, course_id_entry))
    get_info_button.grid(row=0, column=2)


def update_course_info(conn, course_id_entry):
    try:
        # Get the course ID from the user
        course_id = int(course_id_entry.get())

        # Check if the course ID exists in the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM course WHERE course_id = ?", (course_id,))
        course = cursor.fetchone()

        if course:
            # Create a separate pop-up window for displaying and updating the current information
            current_info_window = tk.Toplevel()
            current_info_window.title(f"Update Information for Course ID {course_id}")

            # Labels (keys) next to the white space for updated information
            course_name_label = tk.Label(current_info_window, text="Course Name:")
            course_description_label = tk.Label(current_info_window, text="Course Description:")
            employee_id_label = tk.Label(current_info_window, text="Employee ID:")

            course_name_label.grid(row=0, column=0, sticky='e')
            course_description_label.grid(row=1, column=0, sticky='e')
            employee_id_label.grid(row=2, column=0, sticky='e')

            # Entry fields for updated information
            new_course_name_entry = tk.Entry(current_info_window, width=30)
            new_course_description_entry = tk.Entry(current_info_window, width=30)
            new_employee_id_entry = tk.Entry(current_info_window, width=30)

            new_course_name_entry.grid(row=0, column=1, pady=5)
            new_course_description_entry.grid(row=1, column=1, pady=5)
            new_employee_id_entry.grid(row=2, column=1, pady=5)

            # Update button in the pop-up window
            update_button = tk.Button(current_info_window, text="Update Information",
                                      command=lambda: [update_course_info_in_database(course_id, new_course_name_entry.get(),
                                                                               new_course_description_entry.get(),
                                                                               new_employee_id_entry.get(), conn),
                                                       current_info_window.destroy()])  # Close the window
            update_button.grid(row=3, column=0, columnspan=2, pady=10)

            # Populate the input fields with the current information
            new_course_name_entry.insert(0, course[1])
            new_course_description_entry.insert(0, course[2])
            new_employee_id_entry.insert(0, course[3])

        else:
            messagebox.showerror("Error", f"Course with ID {course_id} not found in the database.")

    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid Course ID.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Function to update course information in the database
def update_course_info_in_database(course_id, new_course_name, new_course_description, new_employee_id, conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE course SET course_name = ?, course_description = ?, employee_id = ? WHERE course_id = ?",
            (new_course_name, new_course_description, new_employee_id, course_id))
        conn.commit()
        messagebox.showinfo("Success", "Course information updated successfully")
    except sqlite3.Error as e:
        conn.rollback()  # Rollback the transaction
        messagebox.showerror("Error", f"Error updating course information: {str(e)}")
