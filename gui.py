import tkinter as tk
from tkinter import messagebox
from student import Student, show_student_records, delete_all_student_records
from classroom import ClassRoom, show_class_records, delete_all_class_records
from course import Course, show_course_records, delete_all_course_records
from employee import (Employee, show_employee_records, delete_all_employee_records, display_employee_notices,
                      authenticate_teacher, authenticate_non_teacher)
from fee import Fee, show_fee_records, delete_all_fee_records
from notice import (StudentNotice, EmployeeNotice, show_student_notice_records, delete_all_student_notice_records,
                    show_employee_notice_records, delete_all_employee_notice_records)
from database_setup import (create_student_notice_table, create_student_table, create_course_table, create_class_table,
                            create_employee_table, create_employee_notice_table, create_fee_table,
                            create_attendance_table, create_class_courses_table, create_grade_table)
from attendance import AttendanceSystem, AttendanceViewer, show_attendance_records, delete_all_attendance_records
from common_util import (ClassCourses, show_class_courses_records, delete_all_class_courses_records,
                         authenticate_student)
from grades import StudentGradesViewer, GradeAssignmentApp


class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # Create and pack entry fields for username and password
        self.username_label = tk.Label(root, text="Unique ID:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        # Create a dropdown menu for user role selection
        self.role_label = tk.Label(root, text="Select Role:")
        self.role_label.pack()
        self.role_var = tk.StringVar()
        self.role_dropdown = tk.OptionMenu(root, self.role_var, "Admin", "Student", "Staff")
        self.role_dropdown.pack()

        # Create the "Login" button and bind it to the login method
        self.login_button = tk.Button(root, text="Login", command=self.login)
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
            else:
                messagebox.showerror("Login Failed", "Invalid credentials")

        elif role == "Staff":
            if authenticate_teacher(self.username, password):  # Authenticate based on employee ID and password for teacher
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
        create_class_table()
        create_student_table()
        create_course_table()
        create_employee_table()
        create_student_notice_table()
        create_employee_notice_table()
        create_fee_table()
        create_class_courses_table()

        # Create a new window for the admin interface
        self.admin_window = tk.Toplevel()
        self.admin_window.title("Admin Dashboard")

        # Create buttons for admin actions
        register_student_button = tk.Button(self.admin_window, text="Register Student", command=Student)
        register_student_button.pack()

        create_class_button = tk.Button(self.admin_window, text="Create Class", command=ClassRoom)
        create_class_button.pack()

        create_course_button = tk.Button(self.admin_window, text="Create Course", command=Course)
        create_course_button.pack()

        register_class_courses_button = tk.Button(self.admin_window, text="Register Courses to Class",
                                                  command=ClassCourses)
        register_class_courses_button.pack()

        register_employee_button = tk.Button(self.admin_window, text="Register Employee", command=Employee)
        register_employee_button.pack()

        update_fee_button = tk.Button(self.admin_window, text="Update Fee Payment Status", command=Fee)
        update_fee_button.pack()

        send_notice_button = tk.Button(self.admin_window, text="Send Notice to Student", command=StudentNotice)
        send_notice_button.pack()

        send_notice_button = tk.Button(self.admin_window, text="Send Notice to Employee", command=EmployeeNotice)
        send_notice_button.pack()

        # Create a button to show student records
        show_stud_records_button = tk.Button(self.admin_window, text="Show Student Records",
                                             command=show_student_records)
        show_stud_records_button.pack()
        delete_all_stud_records_button = tk.Button(self.admin_window, text="Delete All Student Records",
                                                   command=delete_all_student_records)
        delete_all_stud_records_button.pack()

        # Create a button to show employee records
        show_employee_records_button = tk.Button(self.admin_window, text="Show Employee Records",
                                                 command=show_employee_records)
        show_employee_records_button.pack()
        delete_all_employee_records_button = tk.Button(self.admin_window, text="Delete All Employee Records",
                                                       command=delete_all_employee_records)
        delete_all_employee_records_button.pack()

        # Create a button to show class records
        show_class_records_button = tk.Button(self.admin_window, text="Show Class Records",
                                              command=show_class_records)
        show_class_records_button.pack()
        delete_all_class_records_button = tk.Button(self.admin_window, text="Delete All Class Records",
                                                    command=delete_all_class_records)
        delete_all_class_records_button.pack()

        # Create a button to show course records
        show_course_records_button = tk.Button(self.admin_window, text="Show Course Records",
                                               command=show_course_records)
        show_course_records_button.pack()
        delete_all_course_records_button = tk.Button(self.admin_window, text="Delete All Course Records",
                                                     command=delete_all_course_records)
        delete_all_course_records_button.pack()

        # Create a button to show class_courses records
        show_class_courses_records_button = tk.Button(self.admin_window, text="Show Class-Course Records",
                                                      command=show_class_courses_records)
        show_class_courses_records_button.pack()
        delete_all_class_courses_records_button = tk.Button(self.admin_window, text="Delete All Class-Course Records",
                                                            command=delete_all_class_courses_records)
        delete_all_class_courses_records_button.pack()

        # Create a button to show fee records
        show_fee_records_button = tk.Button(self.admin_window, text="Show Student Fee Records",
                                            command=show_fee_records)
        show_fee_records_button.pack()
        delete_all_fee_records_button = tk.Button(self.admin_window, text="Delete All Student Fee Records",
                                                  command=delete_all_fee_records)
        delete_all_fee_records_button.pack()

        # Create a button to show student notice records
        show_student_notice_records_button = tk.Button(self.admin_window, text="Show Student Notice Records",
                                                       command=show_student_notice_records)
        show_student_notice_records_button.pack()
        delete_all_student_notice_records_button = tk.Button(self.admin_window, text="Delete All Student Notice"
                                                                                     " Records",
                                                             command=delete_all_student_notice_records)
        delete_all_student_notice_records_button.pack()

        # Create a button to show employee notice records
        show_employee_notice_records_button = tk.Button(self.admin_window, text="Show Employee Notice Records",
                                                        command=show_employee_notice_records)
        show_employee_notice_records_button.pack()
        delete_all_employee_notice_records_button = tk.Button(self.admin_window, text="Delete All Employee Notice"
                                                                                      " Records",
                                                              command=delete_all_employee_notice_records)
        delete_all_employee_notice_records_button.pack()

        # Create buttons for attendance viewer
        attendance_view_button = tk.Button(self.admin_window, text="Attendance Viewer", command=AttendanceViewer)
        attendance_view_button.pack()

        # Create a button to show attendance records
        show_attendance_records_button = tk.Button(self.admin_window, text="Show Complete Attendance Records",
                                                   command=show_attendance_records)
        show_attendance_records_button.pack()
        delete_all_attendance_records_button = tk.Button(self.admin_window, text="Delete All Attendance Records",
                                                         command=delete_all_attendance_records)
        delete_all_attendance_records_button.pack()

        def admin_logout():
            if messagebox.askokcancel("Logout", "Do you want to logout from admin?"):
                # Close the admin window
                self.admin_window.destroy()
                self.root.deiconify()

        logout_button = tk.Button(self.admin_window, text="Logout", command=admin_logout)
        logout_button.pack()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        self.admin_window.protocol("WM_DELETE_WINDOW",
                                   self.on_admin_window_closing)  # Handle admin_window close event

    def on_admin_window_closing(self):
        if messagebox.askokcancel("Logout", "Do you want to quit from admin?"):
            # Close the admin window
            self.admin_window.destroy()
            self.root.deiconify()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    # def open_student_page(self):
    #     # Create a student GUI window or navigate to the student actions
    #
    #     # You can use the existing class modules and functionalities for student actions here.
    #
    def open_teacher_page(self):
        # Create a staff GUI window or navigate to the staff actions
        create_attendance_table()
        create_grade_table()

        # Create a new window for the admin interface
        self.employee_window = tk.Toplevel()
        self.employee_window.title("Employee Dashboard")

        # Create buttons for attendance
        attendance_button = tk.Button(self.employee_window, text="Attendance", command=AttendanceSystem)
        attendance_button.pack()

        # Create buttons for attendance viewer
        attendance_view_button = tk.Button(self.employee_window, text="Attendance Viewer", command=AttendanceViewer)
        attendance_view_button.pack()

        # Create a button to show complete attendance records
        show_attendance_records_button = tk.Button(self.employee_window, text="Show Complete Attendance Records",
                                                   command=show_attendance_records)
        show_attendance_records_button.pack()

        # Create buttons for attendance
        attendance_button = tk.Button(self.employee_window, text="Assign Grades", command=GradeAssignmentApp)
        attendance_button.pack()

        # Create buttons for grades viewer
        grades_view_button = tk.Button(self.employee_window, text="Grades Viewer", command=StudentGradesViewer)
        grades_view_button.pack()

        # Create buttons for notice viewer
        notice_view_button = tk.Button(self.employee_window, text="View Notices",
                                       command=lambda: display_employee_notices(self.username))
        notice_view_button.pack()

        def employee_logout():
            if messagebox.askokcancel("Logout", "Do you want to logout from employee?"):
                # Close the admin window
                self.employee_window.destroy()
                self.root.deiconify()

        logout_button = tk.Button(self.employee_window, text="Logout", command=employee_logout)
        logout_button.pack()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        self.employee_window.protocol("WM_DELETE_WINDOW",
                                      self.on_employee_window_closing)  # Handle admin_window close event

    def on_employee_window_closing(self):
        if messagebox.askokcancel("Logout", "Do you want to quit from employee?"):
            # Close the admin window
            self.employee_window.destroy()
            self.root.deiconify()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

    def open_staff_page(self):
        # Create a new window for the admin interface
        self.staff_window = tk.Toplevel()
        self.staff_window.title("Employee Dashboard")

        # Create buttons for notice viewer
        notice_view_button = tk.Button(self.staff_window, text="View Notices",
                                       command=lambda: display_employee_notices(self.username))
        notice_view_button.pack()

        def staff_logout():
            if messagebox.askokcancel("Logout", "Do you want to logout from employee?"):
                # Close the admin window
                self.staff_window.destroy()
                self.root.deiconify()

        logout_button = tk.Button(self.staff_window, text="Logout", command=staff_logout)
        logout_button.pack()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        self.staff_window.protocol("WM_DELETE_WINDOW",
                                   self.on_staff_window_closing)  # Handle admin_window close event

    def on_staff_window_closing(self):
        if messagebox.askokcancel("Logout", "Do you want to quit from employee?"):
            # Close the admin window
            self.staff_window.destroy()
            self.root.deiconify()
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)


def main():
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()


if __name__ == "__main__":
    main()
