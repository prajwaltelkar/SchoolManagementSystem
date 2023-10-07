import sqlite3


# Create a table to store employee information
def create_employee_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    employee_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    dob DATE,
                    address TEXT,
                    contact_number TEXT,
                    date_of_join DATE,
                    role TEXT,
                    designation TEXT,
                    email TEXT,
                    salary INTEGER,
                    password TEXT
                    )''')
    conn.commit()
    conn.close()


# Create a table to store class information
def create_course_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS course (
                    course_id INTEGER PRIMARY KEY,
                    course_name TEXT,
                    course_description TEXT,
                    employee_id INTEGER,
                    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
                    )''')


# Create a table to store class information
def create_class_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS class (
                    class_id INTEGER PRIMARY KEY,
                    class_name TEXT,
                    course_id INTEGER,
                    FOREIGN KEY (course_id) REFERENCES course (course_id)
                    )''')
    conn.commit()
    conn.close()


def create_class_courses_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS class_courses (
                    class_id INTEGER,
                    course_id INTEGER,
                    PRIMARY KEY (class_id, course_id),
                    FOREIGN KEY (class_id) REFERENCES class (class_id),
                    FOREIGN KEY (course_id) REFERENCES course (course_id))''')
    conn.commit()
    conn.close()


def create_employee_class_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employee_class (
                    employee_id INTEGER,
                    class_id INTEGER,
                    PRIMARY KEY (employee_id, class_id),
                    FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
                    FOREIGN KEY (class_id) REFERENCES class (class_id)
                    )''')
    conn.commit()
    conn.close()


def create_student_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()

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
                    gender TEXT,
                    email TEXT,
                    password TEXT,
                    class_id INTEGER,
                    FOREIGN KEY (class_id) REFERENCES class(class_id)
                    )''')

    conn.commit()
    conn.close()


def create_fee_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS fee_payments (
                        payment_id INTEGER PRIMARY KEY,
                        student_id INTEGER,
                        amount REAL,
                        payment_date DATE,
                        payment_status TEXT,
                        academic_year TEXT,
                        FOREIGN KEY (student_id) REFERENCES students (student_id)
                    )''')


def create_student_notice_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS student_notice (
                        stud_notice_id INTEGER PRIMARY KEY,
                        student_id INTEGER,
                        title TEXT,
                        content TEXT,
                        publish_date DATE,
                        FOREIGN KEY (student_id) REFERENCES students (student_id)
                    )''')


def create_employee_notice_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employee_notice (
                        emp_notice_id INTEGER PRIMARY KEY,
                        employee_id INTEGER,
                        title TEXT,
                        content TEXT,
                        publish_date DATE,
                        FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
                    )''')


def create_attendance_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                            student_id INTEGER,
                            date DATE,
                            status TEXT,
                            PRIMARY KEY (student_id, date),
                            FOREIGN KEY (student_id) REFERENCES students (student_id)
                        )''')


def create_grade_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS grades (
                        student_id INTEGER,
                        course_id INTEGER,
                        marks INTEGER,
                        grade TEXT,
                        PRIMARY KEY (student_id, course_id),
                        FOREIGN KEY (student_id) REFERENCES students (student_id),
                        FOREIGN KEY (course_id) REFERENCES course (course_id)
                    )''')
    conn.commit()
    conn.close()
