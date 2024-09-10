import pymysql
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Database connection setup
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='yourpassword',
        database='student_db'  # Correct database name
    )

# Main Application Class
class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")  # Light background color for the whole window

        # Title Label
        self.title_label = tk.Label(root, text="Student Management System", font=("Helvetica", 24), fg="#0052cc", bg="#f0f0f0")
        self.title_label.pack(pady=20)

        # Button Frame for better layout
        self.button_frame = tk.Frame(root, bg="#f0f0f0")
        self.button_frame.pack(pady=20)

        # Buttons with ttk for a modern look
        self.add_button = ttk.Button(self.button_frame, text="Add New Student", width=30, command=self.add_student_gui)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.view_button = ttk.Button(self.button_frame, text="View Students", width=30, command=self.view_students)
        self.view_button.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = ttk.Button(self.button_frame, text="Search Student", width=30, command=self.search_student_gui)
        self.search_button.grid(row=1, column=0, padx=10, pady=10)

        self.update_button = ttk.Button(self.button_frame, text="Update Student", width=30, command=self.update_student_gui)
        self.update_button.grid(row=1, column=1, padx=10, pady=10)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Student", width=30, command=self.delete_student_gui)
        self.delete_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # GUI for Adding Student
    def add_student_gui(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Add New Student")
        self.new_window.geometry("400x400")

        # Labels and Entry widgets with padding
        labels = ['Student Name', 'Father Name', 'Class', 'Roll No', 'Sex (M/F/T)', 'Phone No (+91)']
        self.entries = []

        for label in labels:
            frame = tk.Frame(self.new_window)
            frame.pack(pady=10)
            tk.Label(frame, text=label, font=("Helvetica", 12)).pack(side="left", padx=10)
            entry = ttk.Entry(frame)
            entry.pack(side="right")
            self.entries.append(entry)

        # Submit Button
        submit_btn = ttk.Button(self.new_window, text="Submit", command=self.add_student_to_db)
        submit_btn.pack(pady=20)

    # Add student to the database
    def add_student_to_db(self):
        stu_name = self.entries[0].get()
        stu_father = self.entries[1].get()
        stu_class = self.entries[2].get()
        roll_num = self.entries[3].get()
        sex = self.entries[4].get()
        phone = self.entries[5].get()

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO students (name, father, class, roll_no, sex, phone)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (stu_name, stu_father, stu_class, roll_num, sex, phone))
            connection.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            self.new_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {e}")
        finally:
            connection.close()

    # View Students with scrollable table
    def view_students(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("View Students")
        self.new_window.geometry("600x400")

        # Scrollable Treeview
        tree_frame = tk.Frame(self.new_window)
        tree_frame.pack(pady=10)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")

        columns = ['ID', 'Student', 'Father', 'Class', 'Roll No', 'Sex', 'Phone']
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', yscrollcommand=tree_scroll.set)

        tree_scroll.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=80)
        tree.pack()

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM students"
                cursor.execute(sql)
                result = cursor.fetchall()

                for row in result:
                    tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch students: {e}")
        finally:
            connection.close()

   # GUI for Searching Student
    def search_student_gui(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Search Student")

        tk.Label(self.new_window, text="Enter Roll No:").pack(pady=5)
        self.search_entry = tk.Entry(self.new_window)
        self.search_entry.pack(pady=5)

        search_btn = tk.Button(self.new_window, text="Search", command=self.search_student)
        search_btn.pack(pady=10)

    # Search Student by Roll No
    def search_student(self):
        roll_num = self.search_entry.get()
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM students WHERE roll_no = %s"
                cursor.execute(sql, (roll_num,))
                result = cursor.fetchone()

                if result:
                    columns = ['ID', 'Student', 'Father', 'Class', 'Roll No', 'Sex', 'Phone']
                    tree = ttk.Treeview(self.new_window, columns=columns, show='headings')

                    for col in columns:
                        tree.heading(col, text=col)
                    tree.pack()

                    tree.insert("", "end", values=result)
                else:
                    messagebox.showinfo("Not Found", "Student not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search student: {e}")
        finally:
            connection.close()

    # GUI for Updating Student
    def update_student_gui(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Update Student")

        tk.Label(self.new_window, text="Enter Roll No to Update:").pack(pady=5)
        self.update_entry = tk.Entry(self.new_window)
        self.update_entry.pack(pady=5)

        search_btn = tk.Button(self.new_window, text="Search", command=self.update_student)
        search_btn.pack(pady=10)

    # Update Student
    def update_student(self):
        roll_num = self.update_entry.get()
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM students WHERE roll_no = %s"
                cursor.execute(sql, (roll_num,))
                result = cursor.fetchone()

                if result:
                    labels = ['Student Name', 'Father Name', 'Class', 'Roll No', 'Sex (M/F/T)', 'Phone No (+91)']
                    self.update_entries = []

                    for i, label in enumerate(labels):
                        frame = tk.Frame(self.new_window)
                        frame.pack(pady=5)
                        tk.Label(frame, text=label).pack(side="left")
                        entry = tk.Entry(frame)
                        entry.insert(0, result[i+1])  # Start from index 1 to skip ID
                        entry.pack(side="right")
                        self.update_entries.append(entry)

                    update_btn = tk.Button(self.new_window, text="Update", command=lambda: self.save_updated_student(roll_num))
                    update_btn.pack(pady=10)
                else:
                    messagebox.showinfo("Not Found", "Student not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch student: {e}")
        finally:
            connection.close()

    def save_updated_student(self, roll_num):
        stu_name = self.update_entries[0].get()
        stu_father = self.update_entries[1].get()
        stu_class = self.update_entries[2].get()
        sex = self.update_entries[4].get()
        phone = self.update_entries[5].get()

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = """UPDATE students SET name=%s, father=%s, class=%s, sex=%s, phone=%s WHERE roll_no=%s"""
                cursor.execute(sql, (stu_name, stu_father, stu_class, sex, phone, roll_num))
            connection.commit()
            messagebox.showinfo("Success", "Student updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {e}")
        finally:
            connection.close()

    # GUI for Deleting Student
    def delete_student_gui(self):
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("Delete Student")

        tk.Label(self.new_window, text="Enter Roll No to Delete:").pack(pady=5)
        self.delete_entry = tk.Entry(self.new_window)
        self.delete_entry.pack(pady=5)

        delete_btn = tk.Button(self.new_window, text="Delete", command=self.delete_student)
        delete_btn.pack(pady=10)

    # Delete Student by Roll No
    def delete_student(self):
        roll_num = self.delete_entry.get()
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM students WHERE roll_no = %s"
                cursor.execute(sql, (roll_num,))
                connection.commit()
                messagebox.showinfo("Success", "Student deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {e}")
        finally:
            connection.close()

# Initialize the GUI Application
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.mainloop()
