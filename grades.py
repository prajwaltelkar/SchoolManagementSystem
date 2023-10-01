import tkinter as tk
from tkinter import ttk, simpledialog, scrolledtext
import sqlite3
import tkinter.font as tkfont
from tkinter import messagebox


class GradeAssignmentApp:
    def __init__(self):
        self.conn = sqlite3.connect("school_database.db")
        self.cursor = self.conn.cursor()

        self.app = tk.Tk()
        self.app.title("Grade and Marks Assignment App")

        self.create_widgets()

    def create_widgets(self):
        self.class_combo = ttk.Combobox(self.app)
        self.class_combo.grid(row=0, column=1)

        class_label = ttk.Label(self.app, text="Select Class:")
        class_label.grid(row=0, column=0)

        load_button = ttk.Button(self.app, text="Load Students", command=self.load_students)
        load_button.grid(row=0, column=2)

        self.student_listbox = tk.Listbox(self.app, selectmode=tk.MULTIPLE)
        self.student_listbox.grid(row=1, column=0, columnspan=4)

        course_label = ttk.Label(self.app, text="Select Course:")
        course_label.grid(row=2, column=0)

        self.course_combo = ttk.Combobox(self.app)
        self.course_combo.grid(row=2, column=1)

        assign_button = ttk.Button(self.app, text="Enter Grades and Marks", command=self.enter_grades_and_marks)
        assign_button.grid(row=2, column=2)

        self.class_combo.bind("<<ComboboxSelected>>", self.load_courses)

        self.load_classes()

    def load_classes(self):
        self.cursor.execute("SELECT class_name FROM class")
        classes = [row[0] for row in self.cursor.fetchall()]
        self.class_combo['values'] = classes

    def load_courses(self, event):
        selected_class = self.class_combo.get()
        self.cursor.execute(
            "SELECT course_name FROM course WHERE course_id IN (SELECT course_id FROM class_courses WHERE class_id=(SELECT class_id FROM class WHERE class_name=?))",
            (selected_class,))
        courses = [row[0] for row in self.cursor.fetchall()]
        self.course_combo['values'] = courses

    def load_students(self):
        selected_class = self.class_combo.get()
        self.cursor.execute(
            "SELECT student_id, first_name, last_name FROM students WHERE class_id=(SELECT class_id FROM class WHERE class_name=?)",
            (selected_class,))
        students = self.cursor.fetchall()

        self.student_listbox.delete(0, tk.END)

        for student in students:
            student_name = f"{student[1]} {student[2]}"
            self.student_listbox.insert(tk.END, student_name)

    def enter_grades_and_marks(self):
        selected_course = self.course_combo.get()

        for i in self.student_listbox.curselection():
            student_name = self.student_listbox.get(i)
            student_id = self.cursor.execute("SELECT student_id FROM students WHERE first_name || ' ' || last_name=?",
                                             (student_name,)).fetchone()[0]

            grade_entry = simpledialog.askstring("Enter Grade", f"Enter grade for {student_name} in {selected_course}:")
            marks_entry = simpledialog.askinteger("Enter Marks",
                                                  f"Enter marks for {student_name} in {selected_course}:")

            if grade_entry is not None and marks_entry is not None:
                self.cursor.execute(
                    "INSERT OR REPLACE INTO grades (student_id, course_id, marks, grade) VALUES (?, (SELECT course_id FROM course WHERE course_name=?), ?, ?)",
                    (student_id, selected_course, marks_entry, grade_entry))
                self.conn.commit()


class StudentGradesViewer:
    def __init__(self):
        self.conn = sqlite3.connect("school_database.db")
        self.cursor = self.conn.cursor()

        self.app = tk.Tk()
        self.app.title("Student Grades Viewer")

        self.create_widgets()

    def create_widgets(self):
        self.class_label = ttk.Label(self.app, text="Select Class:")
        self.class_label.grid(row=0, column=0)

        self.class_combo = ttk.Combobox(self.app)
        self.class_combo.grid(row=0, column=1)
        self.class_combo.bind("<<ComboboxSelected>>", self.load_courses)

        self.course_label = ttk.Label(self.app, text="Select Course:")
        self.course_label.grid(row=1, column=0)

        self.course_combo = ttk.Combobox(self.app)
        self.course_combo.grid(row=1, column=1)

        self.show_grades_button = ttk.Button(self.app, text="Show All Grades", command=self.show_all_grades)
        self.show_grades_button.grid(row=2, column=0, columnspan=2)

        # Populate the class combo box initially
        self.load_classes()

    def load_classes(self):
        self.cursor.execute("SELECT class_name FROM class")
        classes = [row[0] for row in self.cursor.fetchall()]
        self.class_combo['values'] = classes

    def load_courses(self, event):
        selected_class = self.class_combo.get()
        self.cursor.execute(
            "SELECT course_name FROM course WHERE course_id IN (SELECT course_id FROM class_courses WHERE class_id=(SELECT class_id FROM class WHERE class_name=?))",
            (selected_class,))
        courses = [row[0] for row in self.cursor.fetchall()]
        self.course_combo['values'] = courses

    def show_all_grades(self):
        selected_class = self.class_combo.get()
        selected_course = self.course_combo.get()
        self.cursor.execute(
            "SELECT students.student_id, students.first_name, students.last_name, grades.marks, grades.grade FROM students JOIN grades ON students.student_id = grades.student_id JOIN course ON course.course_id = grades.course_id WHERE students.class_id=(SELECT class_id FROM class WHERE class_name=?) AND course.course_name=?",
            (selected_class, selected_course))
        grade_data = self.cursor.fetchall()

        grades_window = tk.Toplevel(self.app)
        grades_window.title("Student Grades")

        text_widget = scrolledtext.ScrolledText(grades_window, width=60, height=20)
        text_widget.pack()
        text_widget.insert(tk.END, "Student Grades:\n\n")
        for student_data in grade_data:
            student_id = student_data[0]
            student_name = f"{student_data[1]} {student_data[2]}"
            marks = student_data[3]
            grade = student_data[4]
            message = f"Student ID: {student_id}\nStudent Name: {student_name}\nMarks: {marks}\nGrade: {grade}\n\n"
            text_widget.insert(tk.END, message)
        text_widget.config(state=tk.DISABLED)


def show_grades_records():
    # Create a new window for displaying records
    records_window = tk.Toplevel()
    records_window.title("Grades Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(records_window, columns=("Student ID", "Employee ID", "Marks", "Grade"))
    tree.heading("#0", text="Grade Records")
    tree.heading("#1", text="Student ID")
    tree.heading("#2", text="Employee ID")
    tree.heading("#3", text="Marks")
    tree.heading("#4", text="Grade")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch employee records from the database
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grades")
    employee_records = cursor.fetchall()
    conn.close()

    # Insert employee records into the treeview
    for record in employee_records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_all_grades_records():
    confirmation = messagebox.askquestion("Delete All Records",
                                          "Are you sure you want to delete all grade records?")
    if confirmation == 'yes':
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM grades")
        conn.commit()
        messagebox.showinfo("Deletion Successful", "All grade records have been deleted.")
