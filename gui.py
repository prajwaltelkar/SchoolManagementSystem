import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from student import (Student, show_student_records, delete_all_student_records, display_student_grades,
                     display_student_courses, display_student_class_and_students, display_student_fee_report,
                     display_student_attendance_report, view_report, display_student_notices, delete_student)
from classroom import ClassRoom, show_class_records, delete_all_class_records, delete_class
from course import Course, show_course_records, delete_all_course_records, delete_course
from employee import (Employee, show_employee_records, delete_all_employee_records, display_employee_notices,
                      authenticate_teacher, authenticate_non_teacher, delete_employee,
                      window_for_update_employee_record)
from fee import Fee, show_fee_records, delete_all_fee_records, delete_fee
from notice import (StudentNotice, EmployeeNotice, show_student_notice_records, delete_all_student_notice_records,
                    show_employee_notice_records, delete_all_employee_notice_records, delete_student_notice_record,
                    delete_employee_notice_record)
from database_setup import (create_student_notice_table, create_student_table, create_course_table, create_class_table,
                            create_employee_table, create_employee_notice_table, create_fee_table,
                            create_attendance_table, create_class_courses_table, create_grade_table,
                            create_employee_class_table)
from attendance import (AttendanceSystem, AttendanceViewer, show_attendance_records, delete_all_attendance_records,
                        delete_attendance)
from common_util import (ClassCourses, show_class_courses_records, delete_all_class_courses_records,
                         authenticate_student, center_window, delete_class_course_record, EmployeeClassAssignment,
                         show_employee_class_records, delete_all_employee_class_records, delete_employee_class_record)
from grades import StudentGradesViewer, GradeAssignmentApp, show_grades_records, delete_all_grades_records, delete_grade


class LoginPage:
    def __init__(self, root, db_connnection):
        self.conn = db_connnection
        self.root = root
        self.root.title("Login")
        center_window(root, 1800, 700)

        # Load the image
        self.image = Image.open("images/logo (1).png")
        self.photo = ImageTk.PhotoImage(self.image)

        # Create a label for the image and display it at the top left
        self.image_label = ttk.Label(root, image=self.photo, background="#87CEEB")
        self.image_label.grid(row=0, column=0, columnspan=1, padx=329, pady=10, sticky="nw")

        # Create a label for the institute's name and address (left half)
        institute_label = tk.Label(root, text="Prajwal S Telkar International School\nMagadi Road, Syndicate"
                                              " Bank Layout\nBengaluru, India\nICSE\n",
                                   font=("Times", "24", "bold italic"), justify="center", bg="#87CEEB", fg="#00008B")
        institute_label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="n")

        # Create a frame for the left side (left half)
        left_frame = tk.Frame(root)
        left_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Create a Text widget to display welcome message (left half)
        welcome_text = """
                        Prajwal S Telkar International School, located in the heart of Bengaluru,\n
                        is a well-known school in India. People from all over the country recognize\n 
                        the quality of education we offer. Our school is really big,and we have amazing\n 
                        facilities. The classrooms are modern, and our labs are super cool. It's a great\n 
                        place for students to learn and have fun while doing it. Our teachers are experienced\n 
                        and friendly. They make sure every student gets the best education possible.\n
                        If you join us at Prajwal S Telkar International School, you'll have a fantastic opportunity to\n 
                        learn, grow, and create a bright future for yourself.\n
                        "Where Education Meets Excellence: Prajwal S Telkar School"\n
                        """

        self.welcome_label = ttk.Label(left_frame, text=welcome_text, font=("Helvetica", 14), justify="center",
                                       background="#87CEEB", foreground="#00008B")
        self.welcome_label.pack()

        # Create a frame for the right side (right half)
        right_frame = tk.Frame(root, bg="#87CEEB")
        right_frame.grid(row=1, column=3, padx=10, pady=10, sticky="nsew")

        font_size = 12

        # Create and pack entry fields for username and password with larger font size (right half)
        self.username_label = tk.Label(right_frame, text="Unique ID:", font=("Helvetica", font_size), bg="#87CEEB")
        self.username_label.pack()
        self.username_entry = tk.Entry(right_frame, font=("Helvetica", font_size))
        self.username_entry.pack()

        self.password_label = tk.Label(right_frame, text="Password:", font=("Helvetica", font_size), bg="#87CEEB")
        self.password_label.pack()
        self.password_entry = tk.Entry(right_frame, show="*", font=("Helvetica", font_size))
        self.password_entry.pack()

        # Create a dropdown menu for user role selection with larger font size (right half)
        self.role_label = tk.Label(right_frame, text="Select Role:", font=("Helvetica", font_size), bg="#87CEEB")
        self.role_label.pack()
        self.role_var = tk.StringVar()
        self.role_dropdown = tk.OptionMenu(right_frame, self.role_var, "Admin", "Student", "Staff")
        self.role_dropdown.config(font=("Helvetica", font_size))
        self.role_dropdown.pack()

        # Create the "Login" button with larger font size and bind it to the login method (right half)
        self.login_button = tk.Button(right_frame, text="Login", command=self.login, font=("Helvetica", font_size),
                                      bg="#FDF5E6")
        self.login_button.pack()

    def login(self):
        self.username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        # Add your authentication logic here
        if role == "Admin" and self.username == "" and password == "":
            # Close the login window
            self.root.withdraw()
            # Open the admin dashboard
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.open_admin_page()
        elif role == "Student":
            if authenticate_student(self.username, password):  # Authenticate based on student ID and password
                self.root.withdraw()
                messagebox.showinfo("Login Successful", "Welcome, Student!")
                self.open_student_page()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")

        elif role == "Staff":
            if authenticate_teacher(self.username,
                                    password):  # Authenticate based on employee ID and password for teacher
                self.root.withdraw()
                messagebox.showinfo("Login Successful", "Welcome, Teacher!")
                self.open_teacher_page()
            elif authenticate_non_teacher(self.username, password):
                self.root.withdraw()
                messagebox.showinfo("Login Successful", "Welcome, Staff!")
                self.open_staff_page()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")

    def open_admin_page(self):
        create_class_table(self.conn)
        create_student_table(self.conn)
        create_course_table(self.conn)
        create_employee_table(self.conn)
        create_student_notice_table(self.conn)
        create_employee_notice_table(self.conn)
        create_fee_table(self.conn)
        create_class_courses_table(self.conn)
        create_attendance_table(self.conn)
        create_grade_table(self.conn)
        create_employee_class_table(self.conn)

        # Create a new window for the admin interface
        self.admin_window = tk.Toplevel()
        self.admin_window.title("Admin Dashboard")
        self.admin_window.configure(bg="#87CEEB")

        font_name = "Helvatica"
        font_size = 14
        font_style = "bold"

        # Create labels for different sections
        tk.Label(self.admin_window, text="Prajwal S Telkar International School", font=("Helvetica", 24, "bold"),
                 bg="#87CEEB", fg="#00008B").grid(row=0, column=0, columnspan=20)
        tk.Label(self.admin_window, text="Admin", font=("Helvetica", 20, "bold"), bg="#87CEEB", fg="#00008B").grid(
            row=1, column=0,
            columnspan=20)
        tk.Label(self.admin_window, text="Employee", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=4,
                                    column=0)
        tk.Label(self.admin_window, text="Course", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=4,
                                    column=1)
        tk.Label(self.admin_window, text="Class", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=4,
                                    column=2)
        tk.Label(self.admin_window, text="Class-Course", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(
            row=4, column=3)
        tk.Label(self.admin_window, text="Assign Class\nTeacher", font=(font_name, font_size, font_style),
                 bg="#87CEEB", fg="#00008B").grid(
            row=4, column=4)
        tk.Label(self.admin_window, text="Student", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=4,
                                    column=5)
        tk.Label(self.admin_window, text="Fee", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=4,
                                    column=6)
        tk.Label(self.admin_window, text="Student\nNotice", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(
            row=4, column=7)
        tk.Label(self.admin_window, text="Employee\nNotice", font=(font_name, font_size, font_style),
                 bg="#87CEEB", fg="#00008B").grid(
            row=4, column=8)
        tk.Label(self.admin_window, text="Attendance", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(
            row=4, column=9)
        tk.Label(self.admin_window, text="Grades", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=4,
                                    column=10)

        # Create buttons for admin actions
        employee_buttons = [
            ("Register Employee", lambda: Employee(self.conn)),
            ("Show Employee Records", show_employee_records),
            ("Update Employee Records", lambda: window_for_update_employee_record(self.conn)),
            ("Delete Employee", lambda: delete_employee(self.conn)),
            ("Delete All Employee\nRecords", lambda: delete_all_employee_records(self.conn))
        ]

        course_buttons = [
            ("Create Course", lambda: Course(self.conn)),
            ("Show Course Records", show_course_records),
            ("Delete Course Record", lambda: delete_course(self.conn)),
            ("Delete All Course\nRecords", lambda: delete_all_course_records(self.conn))
        ]

        class_buttons = [
            ("Create Class", lambda: ClassRoom(self.conn)),
            ("Show Class Records", show_class_records),
            ("Delete Class Records", lambda: delete_class(self.conn)),
            ("Delete All Class\nRecords", lambda: delete_all_class_records(self.conn))
        ]

        employee_class_buttons = [
            ("Assign Class Teacher", lambda: EmployeeClassAssignment(self.conn)),
            ("Show Class Teacher\nRecords", show_employee_class_records),
            ("Unassign Class Teacher", lambda: delete_employee_class_record(self.conn)),
            ("Unassign All Class\nTeacher", lambda: delete_all_employee_class_records(self.conn))
        ]

        student_buttons = [
            ("Register Student", lambda: Student(self.conn)),
            ("Show Student Records", show_student_records),
            ("Delete Student", lambda: delete_student(self.conn)),
            ("Delete All Student\nRecords", lambda: delete_all_student_records(self.conn))
        ]

        fee_buttons = [
            ("Update Fee Payment\nStatus", lambda: Fee(self.conn)),
            ("Show Fee Records", show_fee_records),
            ("Delete Fee Record", lambda: delete_fee(self.conn)),
            ("Delete All Fee\nRecords", lambda: delete_all_fee_records(self.conn))
        ]

        student_notice_buttons = [
            ("Send Notice to\nStudent", lambda: StudentNotice(self.conn)),
            ("Show Student Notice\nRecords", show_student_notice_records),
            ("Delete Student Notice\nRecord", lambda: delete_student_notice_record(self.conn)),
            ("Delete All Student\nNotice Records", lambda: delete_all_student_notice_records(self.conn))
        ]

        employee_notice_buttons = [
            ("Send Notice to\nEmployee", lambda: EmployeeNotice(self.conn)),
            ("Show Employee Notice\nRecords", show_employee_notice_records),
            ("Delete Employee Notice\nRecord", lambda: delete_employee_notice_record(self.conn)),
            ("Delete All Employee\nNotice Records", lambda: delete_all_employee_notice_records(self.conn))
        ]

        attendance_buttons = [
            ("Attendance Viewer", AttendanceViewer),
            ("Show Complete Attendance\nRecords", show_attendance_records),
            ("Delete attendance record", lambda: delete_attendance(self.conn)),
            ("Delete All Attendance\nRecords", lambda: delete_all_attendance_records(self.conn))
        ]

        grades_buttons = [
            ("Grades Viewer", StudentGradesViewer),
            ("Show Grade Records", show_grades_records),
            ("Delete Grade Record", delete_grade),
            ("Delete All Grade\nRecords", delete_all_grades_records)
        ]

        class_course_buttons = [
            ("Assign Courses to\nClass", lambda: ClassCourses(self.conn)),
            ("Show Courses to\nClass Assignment", show_class_courses_records),
            ("Delete Courses to\nClass Assignment", lambda: delete_class_course_record(self.conn)),
            ("Delete All Courses to\nClass Assignment", lambda: delete_all_class_courses_records(self.conn))
        ]

        self.create_buttons(employee_buttons, row_start=5, col_start=0)
        self.create_buttons(course_buttons, row_start=5, col_start=1)
        self.create_buttons(class_buttons, row_start=5, col_start=2)
        self.create_buttons(class_course_buttons, row_start=5, col_start=3)
        self.create_buttons(employee_class_buttons, row_start=5, col_start=4)
        self.create_buttons(student_buttons, row_start=5, col_start=5)
        self.create_buttons(fee_buttons, row_start=5, col_start=6)
        self.create_buttons(student_notice_buttons, row_start=5, col_start=7)
        self.create_buttons(employee_notice_buttons, row_start=5, col_start=8)
        self.create_buttons(attendance_buttons, row_start=5, col_start=9)
        self.create_buttons(grades_buttons, row_start=5, col_start=10)

        logout_button = tk.Button(self.admin_window, text="Logout", command=self.admin_logout, bg="#FDF5E6",
                                  font=("Calibre", 8, "bold"))
        logout_button.grid(row=16, column=0, columnspan=20, padx=15, pady=(20, 15))
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        self.admin_window.protocol("WM_DELETE_WINDOW",
                                   self.on_admin_window_closing)  # Handle admin_window close event

    def create_buttons(self, buttons_info, row_start, col_start):
        for i, (text, command) in enumerate(buttons_info):
            button = tk.Button(self.admin_window, text=text, command=command, bg="#FDF5E6",
                               font=("Calibre", 8, "bold"), width=20, height=3)
            button.grid(row=row_start + i, column=col_start, padx=10, pady=10, sticky="nsew")
            self.admin_window.grid_columnconfigure(col_start, weight=1)

    def admin_logout(self):
        if messagebox.askokcancel("Logout", "Do you want to logout from admin?"):
            # Close the admin window
            self.admin_window.destroy()
            self.root.deiconify()

    def on_admin_window_closing(self):
        if messagebox.askokcancel("Logout", "Do you want to quit from admin?"):
            # Close the admin window
            self.admin_window.destroy()
            self.root.deiconify()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def open_teacher_page(self):
        # Create a staff GUI window or navigate to the staff actions
        create_attendance_table(self.conn)
        create_grade_table(self.conn)

        # Create a new window for the admin interface
        self.employee_window = tk.Toplevel()
        self.employee_window.configure(bg="#87CEEB")
        center_window(self.employee_window, 800, 280)
        self.employee_window.title("Employee Dashboard")

        font_name = "Helvatica"
        font_size = 14
        font_style = "bold"

        # Create labels for different sections
        tk.Label(self.employee_window, text="Prajwal S Telkar International School", font=("Helvetica", 24, "bold"),
                 bg="#87CEEB", fg="#00008B").grid(row=0, column=0, columnspan=20)
        tk.Label(self.employee_window, text="Teacher", font=("Helvetica", 24, "bold"), bg="#87CEEB",
                 fg="#00008B").grid(row=1, column=0, columnspan=20)
        tk.Label(self.employee_window, text="Attendance", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=0)
        tk.Label(self.employee_window, text="Grades", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=1)
        tk.Label(self.employee_window, text="Notice", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=2)

        # Create buttons for employee actions
        attendance_buttons = [
            ("Attendance", lambda: AttendanceSystem(self.conn, self.username)),
            ("Attendance Viewer", AttendanceViewer),
        ]

        grades_buttons = [
            ("Grades", lambda: GradeAssignmentApp(self.username)),
            ("Grades Viewer", StudentGradesViewer),
        ]

        employee_notice_buttons = [
            ("View Employee Notice", lambda: display_employee_notices(self.username))
        ]

        self.create_employee_buttons(attendance_buttons, row_start=4, col_start=0)
        self.create_employee_buttons(grades_buttons, row_start=4, col_start=1)
        self.create_employee_buttons(employee_notice_buttons, row_start=4, col_start=2)

        logout_button = tk.Button(self.employee_window, text="Logout", command=self.employee_logout, bg="#FDF5E6",
                                  font=("Calibre", 8, "bold"))
        logout_button.grid(row=16, column=0, columnspan=20, padx=15, pady=(20, 15))
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        self.employee_window.protocol("WM_DELETE_WINDOW",
                                      self.on_employee_window_closing)  # Handle employee_window close event

    def create_employee_buttons(self, buttons_info, row_start, col_start):
        for i, (text, command) in enumerate(buttons_info):
            button = tk.Button(self.employee_window, text=text, command=command, bg="#FDF5E6",
                               font=("Calibre", 8, "bold"))
            button.grid(row=row_start + i, column=col_start, padx=5, pady=5, sticky="nsew")
            self.employee_window.grid_columnconfigure(col_start, weight=1)

    def employee_logout(self):
        if messagebox.askokcancel("Logout", "Do you want to logout from Teacher?"):
            # Close the admin window
            self.employee_window.destroy()
            self.root.deiconify()

    def on_employee_window_closing(self):
        if messagebox.askokcancel("Logout", "Do you want to quit from Teacher?"):
            # Close the admin window
            self.employee_window.destroy()
            self.root.deiconify()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def open_staff_page(self):
        # Create a new window for the admin interface
        self.staff_window = tk.Toplevel()
        self.staff_window.title("Employee Dashboard")
        self.staff_window.configure(bg="#87CEEB")
        center_window(self.staff_window, 800, 300)

        font_name = "Helvatica"
        font_size = 14
        font_style = "bold"

        # Create buttons for notice viewer
        tk.Label(self.staff_window, text="Prajwal S Telkar International School", font=("Helvetica", 24, "bold"),
                 bg="#87CEEB", fg="#00008B").grid(row=0, column=0, columnspan=20)
        tk.Label(self.staff_window, text="Staff", font=("Helvetica", 20, "bold"), bg="#87CEEB",
                 fg="#00008B").grid(row=1, column=0, columnspan=20)
        tk.Label(self.staff_window, text="View Notice", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=0)

        employee_notice_buttons = [
            ("View Employee Notice", lambda: display_employee_notices(self.username))
        ]

        self.create_staff_buttons(employee_notice_buttons, row_start=4, col_start=0)

        logout_button = tk.Button(self.staff_window, text="Logout", command=self.staff_logout, bg="#FDF5E6",
                                  font=("Calibre", 8, "bold"))
        logout_button.grid(row=16, column=0, columnspan=20, padx=15, pady=(20, 15))
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        self.staff_window.protocol("WM_DELETE_WINDOW",
                                   self.on_staff_window_closing)  # Handle employee_window close event

    def create_staff_buttons(self, buttons_info, row_start, col_start):
        for i, (text, command) in enumerate(buttons_info):
            button = tk.Button(self.staff_window, text=text, command=command, bg="#FDF5E6", font=("Calibre", 8, "bold"))
            button.grid(row=row_start + i, column=col_start, padx=5, pady=5, sticky="nsew")
            self.staff_window.grid_columnconfigure(col_start, weight=1)

    def staff_logout(self):
        if messagebox.askokcancel("Logout", "Do you want to logout from Staff?"):
            # Close the admin window
            self.staff_window.destroy()
            self.root.deiconify()

    def on_staff_window_closing(self):
        if messagebox.askokcancel("Logout", "Do you want to quit from Staff?"):
            # Close the admin window
            self.staff_window.destroy()
            self.root.deiconify()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def open_student_page(self):
        # Create a student GUI window or navigate to the student actions
        # Create a new window for the admin interface
        self.student_window = tk.Toplevel()
        self.student_window.title("Student Dashboard")
        self.student_window.configure(bg="#87CEEB")
        center_window(self.student_window, 1000, 300)

        font_name = "Helvatica"
        font_size = 14
        font_style = "bold"

        # Create buttons for notice viewer
        tk.Label(self.student_window, text="Prajwal S Telkar International School", font=("Helvetica", 24, "bold"),
                 bg="#87CEEB", fg="#00008B").grid(row=0, column=0, columnspan=20)
        tk.Label(self.student_window, text="Student", font=("Helvetica", 20, "bold"), bg="#87CEEB",
                 fg="#00008B").grid(row=1, column=0, columnspan=20)
        tk.Label(self.student_window, text="Class", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=0)
        tk.Label(self.student_window, text="Course", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=1)
        tk.Label(self.student_window, text="Attendance", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=2)
        tk.Label(self.student_window, text="Notice", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=3)
        tk.Label(self.student_window, text="Fee Payment", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=4)
        tk.Label(self.student_window, text="Grades", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=5)
        tk.Label(self.student_window, text="Report", font=(font_name, font_size, font_style), bg="#87CEEB",
                 fg="#00008B").grid(row=3, column=6)

        # Create buttons for admin actions
        class_buttons = [
            ("Class Enrolled", lambda: display_student_class_and_students(self.username))
        ]

        course_buttons = [
            ("Courses Enrolled", lambda: display_student_courses(self.username))
        ]

        attendance_buttons = [
            ("Attendance Viewer", lambda: display_student_attendance_report(self.username))
        ]

        student_notice_buttons = [
            ("Student Notice", lambda: display_student_notices(self.username))
        ]

        fee_buttons = [
            ("Fee Payment Status", lambda: display_student_fee_report(self.username))
        ]

        grades_buttons = [
            ("Grades Viewer", lambda: display_student_grades(self.username))
        ]

        report_buttons = [
            ("Download Report", lambda: view_report(self.username))
        ]

        self.create_student_buttons(class_buttons, row_start=4, col_start=0)
        self.create_student_buttons(course_buttons, row_start=4, col_start=1)
        self.create_student_buttons(attendance_buttons, row_start=4, col_start=2)
        self.create_student_buttons(student_notice_buttons, row_start=4, col_start=3)
        self.create_student_buttons(fee_buttons, row_start=4, col_start=4)
        self.create_student_buttons(grades_buttons, row_start=4, col_start=5)
        self.create_student_buttons(report_buttons, row_start=4, col_start=6)

        logout_button = tk.Button(self.student_window, text="Logout", command=self.student_logout, bg="#FDF5E6",
                                  font=("Calibre", 8, "bold"))
        logout_button.grid(row=16, column=0, columnspan=20, padx=15, pady=(20, 15))
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        self.student_window.protocol("WM_DELETE_WINDOW",
                                     self.on_student_window_closing)  # Handle employee_window close event

    def create_student_buttons(self, buttons_info, row_start, col_start):
        for i, (text, command) in enumerate(buttons_info):
            button = tk.Button(self.student_window, text=text, command=command, bg="#FDF5E6",
                               font=("Calibre", 8, "bold"))
            button.grid(row=row_start + i, column=col_start, padx=10, pady=10, sticky="nsew")
            self.student_window.grid_columnconfigure(col_start, weight=1)

    def student_logout(self):
        if messagebox.askokcancel("Logout", "Do you want to logout from student?"):
            # Close the admin window
            self.student_window.destroy()
            self.root.deiconify()

    def on_student_window_closing(self):
        if messagebox.askokcancel("Logout", "Do you want to quit from student?"):
            # Close the admin window
            self.student_window.destroy()
            self.root.deiconify()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


def main():
    root = tk.Tk()
    root.configure(bg="#87CEEB")
    conn = sqlite3.connect("school_database.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    LoginPage(root, conn)
    root.mainloop()
    conn.close()


if __name__ == "__main__":
    main()
