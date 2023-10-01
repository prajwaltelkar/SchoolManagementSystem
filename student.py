import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import tkinter.font as tkfont


class Student:
    def __init__(self):
        self.student_window = tk.Toplevel()
        self.student_window.title("Register Student")

        # Create and pack entry fields for student attributes
        self.student_id_label = tk.Label(self.student_window, text="Student ID:")
        self.student_id_label.pack()
        self.student_id_entry = tk.Entry(self.student_window)
        self.student_id_entry.pack()

        self.first_name_label = tk.Label(self.student_window, text="First Name:")
        self.first_name_label.pack()
        self.first_name_entry = tk.Entry(self.student_window)
        self.first_name_entry.pack()

        self.last_name_label = tk.Label(self.student_window, text="Last Name:")
        self.last_name_label.pack()
        self.last_name_entry = tk.Entry(self.student_window)
        self.last_name_entry.pack()

        # Create and pack entry fields for student attributes
        self.dob_label = tk.Label(self.student_window, text="Date of Birth:")
        self.dob_label.pack()
        self.dob_entry = tk.Entry(self.student_window)
        self.dob_entry.pack()

        self.address_label = tk.Label(self.student_window, text="Address:")
        self.address_label.pack()
        self.address_entry = tk.Entry(self.student_window)
        self.address_entry.pack()

        self.contact_number_label = tk.Label(self.student_window, text="Contact Number:")
        self.contact_number_label.pack()
        self.contact_number_entry = tk.Entry(self.student_window)
        self.contact_number_entry.pack()

        self.father_name_label = tk.Label(self.student_window, text="Father's Name:")
        self.father_name_label.pack()
        self.father_name_entry = tk.Entry(self.student_window)
        self.father_name_entry.pack()

        self.mother_name_label = tk.Label(self.student_window, text="Mother's Name:")
        self.mother_name_label.pack()
        self.mother_name_entry = tk.Entry(self.student_window)
        self.mother_name_entry.pack()

        self.enrollment_date_label = tk.Label(self.student_window, text="Enrollment Date:")
        self.enrollment_date_label.pack()
        self.enrollment_date_entry = tk.Entry(self.student_window)
        self.enrollment_date_entry.pack()

        self.gender_label = tk.Label(self.student_window, text="Gender:")
        self.gender_label.pack()
        self.gender_entry = tk.Entry(self.student_window)
        self.gender_entry.pack()

        self.password_label = tk.Label(self.student_window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.student_window)
        self.password_entry.pack()

        self.class_id_label = tk.Label(self.student_window, text="Class ID:")
        self.class_id_label.pack()
        self.class_id_entry = tk.Entry(self.student_window)
        self.class_id_entry.pack()

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.student_window, text="Save", command=self.save_student)
        self.save_button.pack()

    def save_student(self):
        # Retrieve data from entry fields
        student_id = self.student_id_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        dob = self.dob_entry.get()
        address = self.address_entry.get()
        contact_number = self.contact_number_entry.get()
        father_name = self.father_name_entry.get()
        mother_name = self.mother_name_entry.get()
        enrollment_date = self.enrollment_date_entry.get()
        gender = self.gender_entry.get()
        password = self.password_entry.get()
        class_id = self.class_id_entry.get()

        # Insert student information into the database
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO students (
                            student_id, first_name, last_name, dob, address, contact_number, 
                            father_name, mother_name, enrollment_date, gender, password, class_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (student_id, first_name, last_name, dob, address, contact_number,
                        father_name, mother_name, enrollment_date, gender, password, class_id))

        conn.commit()
        conn.close()

        # Close the student registration window
        self.student_window.destroy()
        messagebox.showinfo("Registration Successful", "Student Registered!")


def show_student_records():
    # Create a new window for displaying records
    records_window = tk.Toplevel()
    records_window.title("Student Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(records_window, columns=("Student ID", "First Name", "Last Name", "DOB", "Address",
                                                 "Contact Number", "Father Name", "Mother Name",
                                                 "Enrollment Date",
                                                 "Gender", "Password", "Class ID"))
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
    tree.heading("#10", text="Gender")
    tree.heading("#11", text="Password")
    tree.heading("#12", text="Class ID")

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
    confirmation = messagebox.askquestion("Delete All Records",
                                          "Are you sure you want to delete all student records?")
    if confirmation == 'yes':
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students")
        conn.commit()
        messagebox.showinfo("Deletion Successful", "All student records have been deleted.")


def fetch_student_grades(student_id):
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT course.course_name, grades.marks, grades.grade FROM course "
                   "INNER JOIN grades ON course.course_id = grades.course_id "
                   "WHERE grades.student_id = ?", (student_id,))
    grades = cursor.fetchall()
    conn.close()
    return grades


def display_student_grades(student_id):
    grades = fetch_student_grades(student_id)

    # Create a new window
    window = tk.Toplevel()
    window.title("Student Grades")

    # Create a treeview widget to display grades
    tree = ttk.Treeview(window, columns=("Course", "Marks", "Grade"))
    tree.heading("#0", text="Student Grade Report")
    tree.heading("#1", text="Course")
    tree.heading("#2", text="Marks")
    tree.heading("#3", text="Grade")
    tree.pack()

    # Insert the grades into the treeview
    for grade in grades:
        tree.insert("", "end", values=(grade[0], grade[1], grade[2]))

    # Adjust column widths
    tree.column("#1", width=150)
    tree.column("#2", width=75)
    tree.column("#3", width=75)


def fetch_student_courses(student_id):
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT course.course_name FROM course "
                   "INNER JOIN class_courses ON course.course_id = class_courses.course_id "
                   "WHERE class_courses.class_id = (SELECT class_id FROM students WHERE student_id = ?)",
                   (student_id,))
    courses = cursor.fetchall()
    conn.close()
    return courses


def display_student_courses(student_id):
    courses = fetch_student_courses(student_id)

    # Create a new window
    window = tk.Toplevel()
    window.title("Enrolled Courses")

    if not courses:
        # If no courses are found, display a message
        label = tk.Label(window, text="You are not enrolled in any courses.")
        label.pack()
    else:
        # Display the list of enrolled courses
        label = tk.Label(window, text="Enrolled Courses:")
        label.pack()
        for course in courses:
            course_name = course[0]
            label = tk.Label(window, text=course_name)
            label.pack()


def fetch_student_class(student_id):
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT class.class_name FROM class "
                   "INNER JOIN students ON class.class_id = students.class_id "
                   "WHERE students.student_id = ?", (student_id,))
    class_name = cursor.fetchone()

    if class_name is not None:
        cursor.execute("SELECT students.first_name, students.last_name FROM students "
                       "WHERE students.class_id = (SELECT class_id FROM students WHERE student_id = ?)",
                       (student_id,))
        students_in_class = cursor.fetchall()
    else:
        students_in_class = []

    conn.close()
    return class_name, students_in_class


def display_student_class_and_students(student_id):
    class_name, students_in_class = fetch_student_class(student_id)

    # Create a new window
    window = tk.Toplevel()
    window.title("Enrolled Class and Students")

    if class_name is not None:
        # Display the enrolled class
        label = tk.Label(window, text=f"Enrolled Class: {class_name[0]}")
        label.pack()

        if students_in_class:
            # Display the list of students in the class
            label = tk.Label(window, text="Classmates:")
            label.pack()
            for student in students_in_class:
                student_name = f"{student[0]} {student[1]}"
                label = tk.Label(window, text=student_name)
                label.pack()
        else:
            # If no students are found in the class, display a message
            label = tk.Label(window, text="No students found in the class.")
            label.pack()
    else:
        # If no class is found, display a message
        label = tk.Label(window, text="You are not enrolled in any class.")
        label.pack()


def fetch_student_fee_payments(student_id):
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT payment_id, amount, payment_date, payment_status, academic_year "
                   "FROM fee_payments WHERE student_id = ? ORDER BY payment_date ASC",
                   (student_id,))
    fee_payments = cursor.fetchall()
    conn.close()
    return fee_payments


def display_student_fee_report(student_id):
    fee_payments = fetch_student_fee_payments(student_id)

    # Create a new window
    window = tk.Toplevel()
    window.title("Fee Payment Report")

    if not fee_payments:
        # If no fee payments are found, display a message
        label = tk.Label(window, text="No fee payments found for this student.")
        label.pack()
    else:
        # Create a treeview widget to display the fee payment report
        tree = ttk.Treeview(window, columns=("Payment ID", "Amount", "Payment Date", "Payment Status", "Academic Year"))
        tree.heading("#0", text="Fee Payment Report")
        tree.heading("#1", text="Payment ID")
        tree.heading("#2", text="Amount")
        tree.heading("#3", text="Payment Date")
        tree.heading("#4", text="Payment Status")
        tree.heading("#5", text="Academic Year")
        tree.pack()

        # Insert fee payment data into the treeview
        for payment in fee_payments:
            tree.insert("", "end", values=payment)

        # Adjust column widths
        tree.column("#1", width=75)
        tree.column("#2", width=75)
        tree.column("#3", width=100)
        tree.column("#4", width=100)
        tree.column("#5", width=100)


def fetch_student_attendance(student_id):
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, status FROM attendance WHERE student_id = ? ORDER BY date ASC",
                   (student_id,))
    attendance_data = cursor.fetchall()
    conn.close()
    return attendance_data


def display_student_attendance_report(student_id):
    attendance_data = fetch_student_attendance(student_id)

    # Create a new window
    window = tk.Toplevel()
    window.title("Attendance Report")

    if not attendance_data:
        # If no attendance data is found, display a message
        label = tk.Label(window, text="No attendance data found for this student.")
        label.pack()
    else:
        # Create a treeview widget to display the attendance report
        tree = ttk.Treeview(window, columns=("Date", "Status"))
        tree.heading("#0", text="Attendance Report")
        tree.heading("#1", text="Date")
        tree.heading("#2", text="Status")
        tree.pack()

        # Insert attendance data into the treeview
        for date, status in attendance_data:
            tree.insert("", "end", values=(date, status))

        # Adjust column widths
        tree.column("#1", width=100)
        tree.column("#2", width=100)
