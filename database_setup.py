import sqlite3


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
                    age INTEGER,
                    gender TEXT
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
def create_class_table():
    conn = sqlite3.connect("school_database.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS class (
                    class_id INTEGER PRIMARY KEY,
                    class_name TEXT
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