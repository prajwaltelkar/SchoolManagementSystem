import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.font as tkfont

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from tkinter import messagebox
from tkinter import scrolledtext, simpledialog


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


def delete_student():
    student_window = tk.Tk()
    student_window.withdraw()  # Hide the main window

    # Prompt the user for student_id using simpledialog
    student_id = simpledialog.askinteger("Input", "Enter Student ID:")

    if student_id is not None:
        confirmation = messagebox.askquestion("Delete Student",
                                              f"Are you sure you want to delete Student ID {student_id} from the Student records?")
        if confirmation == 'yes':
            conn = sqlite3.connect("school_database.db")
            cursor = conn.cursor()

            # Delete the student record for the specified student_id
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))

            conn.commit()
            conn.close()
            messagebox.showinfo("Deletion Successful", f"Student record with ID {student_id} has been deleted.")
        else:
            messagebox.showinfo("Deletion Canceled", "Student record has not been deleted.")
    else:
        messagebox.showinfo("Invalid Input", "Please provide a valid Student ID.")

    # Close the Tkinter window
    student_window.destroy()


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


def fetch_student_total_attendance_percentage(student_id):
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = ? AND status = 'Present'",
                   (student_id,))
    present_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = ?",
                   (student_id,))
    total_count = cursor.fetchone()[0]
    conn.close()

    # Calculate attendance percentage
    if total_count > 0:
        attendance_percentage = (present_count / total_count) * 100
    else:
        attendance_percentage = 0.0

    return attendance_percentage


def fetch_student_notices(student_id):
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student_notice WHERE student_id = ?", (student_id,))
    notices = cursor.fetchall()
    conn.close()
    return notices


def display_student_notices(student_id):
    notices = fetch_student_notices(student_id)

    # Create a new window
    window = tk.Toplevel()
    window.title("Student Notices")

    # Create a scrolled text widget to display notices
    text_widget = scrolledtext.ScrolledText(window, width=50, height=20)
    text_widget.pack()

    # Insert the notices into the text widget
    for notice in notices:
        text_widget.insert(tk.END, f"Title: {notice[2]}\n")
        text_widget.insert(tk.END, f"Content: {notice[3]}\n")
        text_widget.insert(tk.END, f"Publish Date: {notice[4]}\n\n")

    # Disable text editing in the widget
    text_widget.config(state=tk.DISABLED)


def fetch_student_grade_report(student_id):
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT course.course_name, grades.marks, grades.grade FROM course "
                   "INNER JOIN grades ON course.course_id = grades.course_id "
                   "WHERE grades.student_id = ?", (student_id,))
    grade_report = cursor.fetchall()

    # Calculate total marks and total percentage
    total_marks = 0
    total_percentage = 0.0
    for _, marks, _ in grade_report:
        total_marks += marks
    if total_marks > 0:
        total_percentage = (total_marks / (len(grade_report) * 100)) * 100

    conn.close()

    return grade_report, total_marks, total_percentage


def generate_pdf_report(student_name, attendance_percentage, grade_report, total_marks, total_percentage):
    try:
        # Create the PDF filename using the provided student_name
        pdf_filename = fr"C:\Users\Prajwal\Downloads\{student_name}_report.pdf".replace(" ", "_")

        # Get the current date and time for report generation time
        generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a PDF document with a custom page template
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Define styles for the report
        styles = getSampleStyleSheet()
        normal_style = styles["Normal"]
        table_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]

        # Create a list to hold the elements of the PDF document
        elements = []

        # Define a page template with frames for header and footer
        frame_time = Frame(36, 36, doc.width - 72, doc.height - 72)
        frame_address = Frame(36, 36, doc.width - 72, doc.height - 72)
        template = PageTemplate(id='custom', frames=[frame_time, frame_address])

        # Define header and footer content
        def header(canvas, doc):
            canvas.setFont('Helvetica', 12)
            canvas.drawString(doc.width - 250, doc.height + 80, "Prajwal International School")
            canvas.drawString(doc.width - 200, doc.height + 50, "CBSE Bangalore")
            # Add any other header elements as needed

        def footer(canvas, doc):
            canvas.setFont('Helvetica', 10)
            canvas.drawString(36, 36, f"Report Generation Time: {generation_time}")
            canvas.drawString(doc.width - 200, 50, "End")
            # Add any other footer elements as needed

        template.beforeDrawPage = header
        template.afterDrawPage = footer
        doc.addPageTemplates([template])

        # Add the student name
        stud_name_text = f"Student Name: {student_name}"
        stud_name_paragraph = Paragraph(stud_name_text, normal_style)
        elements.append(stud_name_paragraph)
        elements.append(Spacer(1, 12))

        # Add the attendance percentage
        attendance_text = f"Attendance Percentage: {attendance_percentage:.1f}%"
        attendance_paragraph = Paragraph(attendance_text, normal_style)
        elements.append(attendance_paragraph)
        elements.append(Spacer(1, 12))

        # Add the grade report table
        grade_data = [["Course", "Marks", "Grade"]]
        for course, marks, grade in grade_report:
            grade_data.append([course, str(marks), grade])

        grade_table = Table(grade_data, colWidths=[150, 50, 50])
        grade_table.setStyle(table_style)
        elements.append(grade_table)
        elements.append(Spacer(1, 12))

        # Add total marks and total percentage
        total_marks_text = f"Total Marks: {total_marks}"
        total_percentage_text = f"Total Percentage: {total_percentage:.1f}%"
        total_marks_paragraph = Paragraph(total_marks_text, normal_style)
        total_percentage_paragraph = Paragraph(total_percentage_text, normal_style)
        elements.append(total_marks_paragraph)
        elements.append(total_percentage_paragraph)

        # Add "All the best" centered
        all_the_best_text = "<b>All the best</b>"
        all_the_best_paragraph = Paragraph(all_the_best_text, normal_style)
        elements.append(Spacer(1, 12))
        elements.append(all_the_best_paragraph)

        # Build the PDF document
        doc.build(elements)

        messagebox.showinfo("Report Generated", f"The report has been saved as {pdf_filename}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def view_report(student_id):
    global student_name
    if student_id is not None:
        attendance_percentage = fetch_student_total_attendance_percentage(student_id)
        grade_report, total_marks, total_percentage = fetch_student_grade_report(student_id)
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name FROM students WHERE student_id=?", (student_id,))
        student_data = cursor.fetchone()
        try:
            first_name, last_name = student_data
            student_name = f"{first_name} {last_name}"
        except Exception as e:
            messagebox.showerror("Error", f"No Student Data: {str(e)}")

        # Close the database connection
        conn.close()
        generate_pdf_report(student_name, attendance_percentage, grade_report, total_marks, total_percentage)
