import sqlite3
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox, simpledialog


class ClassRoom:
    def __init__(self, db_connection):
        self.class_window = tk.Toplevel()
        self.class_window.title("Create Class")

        self.conn = db_connection

        # Create and pack entry fields for class attributes
        self.class_id_label = tk.Label(self.class_window, text="Class ID")
        self.class_id_label.pack()
        self.class_id_entry = tk.Entry(self.class_window)
        self.class_id_entry.pack()

        self.class_name_label = tk.Label(self.class_window, text="Class Name:")
        self.class_name_label.pack()
        self.class_name_entry = tk.Entry(self.class_window)
        self.class_name_entry.pack()

        # Create the "Save" button and bind it to the save_student method
        self.save_button = tk.Button(self.class_window, text="Save", command=self.save_classroom)
        self.save_button.pack()

    def save_classroom(self):
        try:
            cursor = self.conn.cursor()

            class_id = self.class_id_entry.get()
            class_name = self.class_name_entry.get()

            cursor.execute("INSERT INTO class (class_id, class_name) VALUES (?, ?)",
                           (class_id, class_name))

            self.conn.commit()

            self.class_window.destroy()
            messagebox.showinfo("Successful", "Class Created!")
        except sqlite3.Error as error:
            messagebox.showerror("Error", str(error))


def show_class_records():
    # Create a new window for displaying records
    class_records_window = tk.Toplevel()
    class_records_window.title("Class Database")

    # Create a treeview widget to display records
    tree = ttk.Treeview(class_records_window, columns=("Class ID", "Class Name"))
    tree.heading("#0", text="Class Record")
    tree.heading("#1", text="Class ID")
    tree.heading("#2", text="Class Name")

    # Create horizontal scrollbar
    xscroll = ttk.Scrollbar(class_records_window, orient=tk.HORIZONTAL, command=tree.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    tree.configure(xscrollcommand=xscroll.set)

    # Fetch Class records from the database
    try:
        conn = sqlite3.connect("school_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM class")
        class_records = cursor.fetchall()
        conn.close()
    except sqlite3.Error as error:
        messagebox.showerror("Error", str(error))

    # Insert Class records into the treeview
    for record in class_records:
        tree.insert("", "end", values=record)

    # Adjust column widths based on content
    for col in tree["columns"]:
        tree.column(col, width=tkfont.Font().measure(col) + 10)  # Adjust the width as needed

    tree.pack(fill=tk.BOTH, expand=True)


def delete_class(conn):
    # Create a Tkinter window
    class_window = tk.Tk()
    class_window.withdraw()  # Hide the main window

    # Prompt the user for class_id using simpledialog
    class_id = simpledialog.askinteger("Input", "Enter Class ID:")

    if class_id is not None:
        confirmation = messagebox.askquestion("Delete Class",
                                              f"Are you sure you want to delete Class ID {class_id} from the Classes?")
        if confirmation == 'yes':
            try:
                cursor = conn.cursor()

                # Delete the class record for the specified class_id
                cursor.execute("DELETE FROM class WHERE class_id = ?", (class_id,))
                conn.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo("Deletion Successful", f"Class record with ID {class_id} has been deleted.")
                else:
                    messagebox.showerror("Invalid Input", f"No such Class record.")
            except sqlite3.Error as error:
                conn.rollback()  # Rollback the transaction in case of an error
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "Class record has not been deleted.")
    else:
        messagebox.showerror("Invalid Input", "Please provide a valid Class ID.")

    # Close the Tkinter window
    class_window.destroy()


def delete_all_class_records(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM class")
    count = cursor.fetchone()[0]

    if count == 0:
        messagebox.showerror("No Records", "There are no Course records to delete.")
    else:
        confirmation = messagebox.askquestion("Delete All Records",
                                              "Are you sure you want to delete all Class records?")
        if confirmation == 'yes':
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM class")
                conn.commit()
                messagebox.showinfo("Deletion Successful", "All Class records have been deleted.")
            except sqlite3.Error as error:
                conn.rollback()
                messagebox.showerror("Error", str(error))
        else:
            messagebox.showerror("Deletion Canceled", "No Course records have been deleted.")
