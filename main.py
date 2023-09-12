import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import tkinter.font as tkfont
from common_util import ApplicationState

# Create or connect to a database
conn = sqlite3.connect("school_database.db")
cursor = conn.cursor()

# Create a table to store student information
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                dob DATE,
                address TEXT,
                contact_number TEXT,
                father_name TEXT,
                mother_name TEXT,
                enrollment_date DATE,
                age INTEGER,
                gender TEXT
                )''')

# Create a table to store employee information
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                dob DATE,
                address TEXT,
                contact_number TEXT,
                role TEXT
                )''')

# Create a table to store class information
cursor.execute('''CREATE TABLE IF NOT EXISTS class (
                class_id INTEGER PRIMARY KEY,
                class_name TEXT
                )''')

# Create a table to store class information
cursor.execute('''CREATE TABLE IF NOT EXISTS course (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT,
                course_description TEXT
                )''')

# Commit changes and close the database connection
conn.commit()
conn.close()

# Create the main window
root = tk.Tk()
root.title("School Database Management System")


# Function to handle login button click
def login():
    username = username_entry.get()
    password = password_entry.get()
    role = role_var.get()

    # Add your authentication logic here
    if role == "Admin" and username == "admin" and password == "admin":
        # Close the login window
        root.withdraw()
        # Open the admin dashboard
        admin_dashboard()
    elif role == "Student" and username == "student" and password == "studentpassword":
        # Student functionality
        messagebox.showinfo("Login Successful", "Welcome, Student!")
        # Add student functionality here
    elif role == "Staff" and username == "staff" and password == "staffpassword":
        # Staff functionality
        messagebox.showinfo("Login Successful", "Welcome, Staff!")
        # Add staff functionality here
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")


def register_student():
    # Create a new window for student registration
    student_window = tk.Toplevel()
    student_window.title("Register Student")

    # Create and pack entry fields for student attributes
    first_name_label = tk.Label(student_window, text="First Name:")
    first_name_label.pack()
    first_name_entry = tk.Entry(student_window)
    first_name_entry.pack()

    last_name_label = tk.Label(student_window, text="Last Name:")
    last_name_label.pack()
    last_name_entry = tk.Entry(student_window)
    last_name_entry.pack()

    # Create and pack entry fields for student attributes
    dob_label = tk.Label(student_window, text="Date of Birth:")
    dob_label.pack()
    dob_entry = tk.Entry(student_window)
    dob_entry.pack()

    address_label = tk.Label(student_window, text="Address:")
    address_label.pack()
    address_entry = tk.Entry(student_window)
    address_entry.pack()

    contact_number_label = tk.Label(student_window, text="Contact Number:")
    contact_number_label.pack()
    contact_number_entry = tk.Entry(student_window)
    contact_number_entry.pack()

    father_name_label = tk.Label(student_window, text="Father's Name:")
    father_name_label.pack()
    father_name_entry = tk.Entry(student_window)
    father_name_entry.pack()

    mother_name_label = tk.Label(student_window, text="Mother's Name:")
    mother_name_label.pack()
    mother_name_entry = tk.Entry(student_window)
    mother_name_entry.pack()

    enrollment_date_label = tk.Label(student_window, text="Enrollment Date:")
    enrollment_date_label.pack()
    enrollment_date_entry = tk.Entry(student_window)
    enrollment_date_entry.pack()

    age_label = tk.Label(student_window, text="Age:")
    age_label.pack()
    age_entry = tk.Entry(student_window)
    age_entry.pack()

    gender_label = tk.Label(student_window, text="Gender:")
    gender_label.pack()
    gender_entry = tk.Entry(student_window)
    gender_entry.pack()

    # Add more entry fields for other student attributes (dob, address, contact_number, etc.)

    def save_student():
        # Retrieve data from entry fields
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        dob = dob_entry.get()
        address = address_entry.get()
        contact_number = contact_number_entry.get()
        father_name = father_name_entry.get()
        mother_name = mother_name_entry.get()
        enrollment_date = enrollment_date_entry.get()
        age = age_entry.get()
        gender = gender_entry.get()
        # Retrieve other student attributes here

        # Insert student information into the database
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO students (
                            first_name, last_name, dob, address, contact_number, 
                            father_name, mother_name, enrollment_date, age, gender
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (first_name, last_name, dob, address, contact_number,
                        father_name, mother_name, enrollment_date, age, gender))

        conn.commit()
        conn.close()

        # Close the student registration window
        student_window.destroy()
        messagebox.showinfo("Registration Successful", "Student Registered!")

    save_button = tk.Button(student_window, text="Save", command=save_student)
    save_button.pack()


# Function to display all student records in a new window
def show_student_records():
    # Create a new window for displaying records
    records_window = tk.Toplevel()
    records_window.title("Student Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(records_window, columns=("Student ID", "First Name", "Last Name", "DOB", "Address",
                                                 "Contact Number", "Father Name", "Mother Name", "Enrollment Date",
                                                 "Age", "Gender"))
    tree.heading("#0", text="Student Records")
    tree.heading("#1", text="Student ID")
    tree.heading("#2", text="First Name")
    tree.heading("#3", text="Last Name")
    tree.heading("#4", text="Date of Birth")
    tree.heading("#5", text="Address")
    tree.heading("#6", text="Contact Number")
    tree.heading("#7", text="Father Name")
    tree.heading("#8", text="Mother Name")
    tree.heading("#9", text="Enrollment Date")
    tree.heading("#10", text="Age")
    tree.heading("#11", text="Gender")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch student records from the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    student_records = cursor.fetchall()
    conn.close()

    # Insert student records into the treeview
    for record in student_records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_all_student_records():
    confirmation = messagebox.askquestion("Delete All Records", "Are you sure you want to delete all student records?")
    if confirmation == 'yes':
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students")
        conn.commit()
        messagebox.showinfo("Deletion Successful", "All student records have been deleted.")


def register_employee():
    # Create a new window for employee registration
    employee_window = tk.Toplevel()
    employee_window.title("Register Employee")

    # Create and pack entry fields for employee attributes
    employee_id_label = tk.Label(employee_window, text="Employee ID (Primary Key):")
    employee_id_label.pack()
    employee_id_entry = tk.Entry(employee_window)
    employee_id_entry.pack()

    first_name_label = tk.Label(employee_window, text="First Name:")
    first_name_label.pack()
    first_name_entry = tk.Entry(employee_window)
    first_name_entry.pack()

    last_name_label = tk.Label(employee_window, text="Last Name:")
    last_name_label.pack()
    last_name_entry = tk.Entry(employee_window)
    last_name_entry.pack()

    dob_label = tk.Label(employee_window, text="Date of Birth:")
    dob_label.pack()
    dob_entry = tk.Entry(employee_window)
    dob_entry.pack()

    address_label = tk.Label(employee_window, text="Address:")
    address_label.pack()
    address_entry = tk.Entry(employee_window)
    address_entry.pack()

    contact_number_label = tk.Label(employee_window, text="Contact Number:")
    contact_number_label.pack()
    contact_number_entry = tk.Entry(employee_window)
    contact_number_entry.pack()

    role_label = tk.Label(employee_window, text="Role (Teacher/Staff):")
    role_label.pack()
    role_entry = tk.Entry(employee_window)
    role_entry.pack()

    def save_employee():
        # Retrieve data from entry fields
        employee_id = employee_id_entry.get()
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        dob = dob_entry.get()
        address = address_entry.get()
        contact_number = contact_number_entry.get()
        role = role_entry.get()

        # Insert employee information into the database
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO employees (
                            employee_id, first_name, last_name, dob, address, contact_number, 
                            role
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                       (employee_id, first_name, last_name, dob, address, contact_number,
                        role))

        conn.commit()
        conn.close()

        # Close the employee registration window
        employee_window.destroy()
        messagebox.showinfo("Registration Successful", "Employee Registered!")

    # Create the "Register" button and bind it to the save_employee function
    register_button = tk.Button(employee_window, text="Register", command=save_employee)
    register_button.pack()


def create_class():
    # Create a new window for employee registration
    class_window = tk.Toplevel()
    class_window.title("Create Class")

    # Create and pack entry fields for employee attributes
    class_id_label = tk.Label(class_window, text="Class ID")
    class_id_label.pack()
    class_id_entry = tk.Entry(class_window)
    class_id_entry.pack()

    class_name_label = tk.Label(class_window, text="Class Name:")
    class_name_label.pack()
    class_name_entry = tk.Entry(class_window)
    class_name_entry.pack()

    def save_class():
        # Retrieve data from entry fields
        class_id = class_id_entry.get()
        class_name = class_name_entry.get()

        # Insert employee information into the database
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO class (
                            class_id, class_name ) VALUES (?, ?)''',
                       (class_id, class_name))

        conn.commit()
        conn.close()

        # Close the employee registration window
        class_window.destroy()
        messagebox.showinfo("Successful", "Class Created!")

    # Create the "Register" button and bind it to the save_employee function
    register_button = tk.Button(class_window, text="Create", command=save_class)
    register_button.pack()


def create_course():
    # Create a new window for employee registration
    course_window = tk.Toplevel()
    course_window.title("Create course")

    # Create and pack entry fields for employee attributes
    course_id_label = tk.Label(course_window, text="Course ID")
    course_id_label.pack()
    course_id_entry = tk.Entry(course_window)
    course_id_entry.pack()

    course_name_label = tk.Label(course_window, text="Course Name:")
    course_name_label.pack()
    course_name_entry = tk.Entry(course_window)
    course_name_entry.pack()

    course_description_label = tk.Label(course_window, text="Course description:")
    course_description_label.pack()
    course_description_entry = tk.Entry(course_window)
    course_description_entry.pack()

    def save_course():
        # Retrieve data from entry fields
        course_id = course_id_entry.get()
        course_name = course_name_entry.get()
        course_description = course_description_entry.get()

        # Insert employee information into the database
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO course (
                            course_id, course_name, course_description ) VALUES (?, ?, ?)''',
                       (course_id, course_name, course_description))

        conn.commit()
        conn.close()

        # Close the employee registration window
        course_window.destroy()
        messagebox.showinfo("Successful", "Course Created!")

    # Create the "Register" button and bind it to the save_employee function
    register_button = tk.Button(course_window, text="Create", command=save_course)
    register_button.pack()


# Create an instance of ApplicationState to manage program state
state = ApplicationState()


# Create the admin dashboard
def admin_dashboard():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Dashboard")

    # Create buttons for admin actions
    register_student_button = tk.Button(admin_window, text="Register Student", command=register_student)
    create_class_button = tk.Button(admin_window, text="Create Class", command=create_class)
    create_course_button = tk.Button(admin_window, text="Create Course", command=create_course)
    register_employee_button = tk.Button(admin_window, text="Register Employee", command=register_employee)
    assign_teacher_class_button = tk.Button(admin_window, text="Assign Teacher to Class")
    assign_teacher_course_button = tk.Button(admin_window, text="Assign Teacher to a Course")
    assign_course_to_class_button = tk.Button(admin_window, text="Assign Course to Class")
    update_fee_button = tk.Button(admin_window, text="Update Fee Payment Status")
    send_notice_button = tk.Button(admin_window, text="Send Notice")

    # Create a button to show student records
    show_records_button = tk.Button(admin_window, text="Show Student Records", command=show_student_records)
    delete_all_records_button = tk.Button(admin_window, text="Delete All Student Records",
                                          command=delete_all_student_records)

    # Pack the buttons
    register_student_button.pack()
    register_employee_button.pack()
    create_class_button.pack()
    create_course_button.pack()
    assign_teacher_class_button.pack()
    assign_teacher_course_button.pack()
    assign_course_to_class_button.pack()
    update_fee_button.pack()
    send_notice_button.pack()
    show_records_button.pack()
    delete_all_records_button.pack()

    # Function to handle the admin window closing
    def on_admin_window_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit the admin dashboard?"):
            state.stop_program()
            admin_window.destroy()

    admin_window.protocol("WM_DELETE_WINDOW", on_admin_window_closing)  # Handle admin_window close event


# Create and pack widgets
username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

role_label = tk.Label(root, text="Role:")
role_label.pack()
role_var = tk.StringVar()
role_dropdown = tk.OptionMenu(root, role_var, "Admin", "Student", "Staff")
role_dropdown.pack()

login_button = tk.Button(root, text="Login", command=login)
login_button.pack()


# Bind the close event to exit the application gracefully
def login_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        state.stop_program()
        root.destroy()


root.protocol("WM_DELETE_WINDOW", login_closing)

# Start the Tkinter main loop, and continue running while program_running is True
while state.is_program_running():
    root.update_idletasks()
    root.update()
