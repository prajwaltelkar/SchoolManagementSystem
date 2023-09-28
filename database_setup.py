import sqlite3


# Create a table to store class information
def create_class_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS class (
                    class_id INTEGER PRIMARY KEY,
                    class_name TEXT
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
                    class_id INTEGER,
                    FOREIGN KEY (class_id) REFERENCES class(class_id)
                    )''')

    conn.commit()
    conn.close()


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
                    role TEXT
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
                    course_description TEXT
                    )''')


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
                        content TEXT
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
