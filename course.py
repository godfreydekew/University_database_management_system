import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from time import sleep

class Course:import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from time import sleep

class Course:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Course Management System")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the window dimensions to match the screen resolution
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.configure(bg="#2E4374")
        self.frame = tk.Frame(self.root, bg="#2E4374", bd=2, relief=tk.GROOVE)
        self.frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Create or open the databas
        self.db = sqlite3.connect('university.db')
        self.cursor = self.db.cursor()
        self.closew = False
        # Create or open the student table

        labels_bg_color = "#4B527E"
        entry_bg_color = "#7C81AD"
        buttons_bg_color = "#4B527E"


        # GUI elements
        self.label_id = tk.Label(self.frame, text="  Course ID:", bg=labels_bg_color, fg="white")
        self.label_id.grid(row=0, column=0, padx=10, pady=(10, 10), sticky='w')

        self.entry_id = tk.Entry(self.frame, width=20)
        self.entry_id.grid(row=0, column=1, padx=50, pady=(30, 10))

        self.title = tk.Label(self.frame, text="Course Title:", bg=labels_bg_color, fg="white")
        self.title.grid(row=1, column=0, padx=10, pady=10)

        self.entry_title = tk.Entry(self.frame, width=20)
        self.entry_title.grid(row=1, column=1, padx=10, pady=10)

        self.label_dept = tk.Label(self.frame, text="Department:", bg=labels_bg_color, fg="white")
        self.label_dept.grid(row=2, column=0, padx=10, pady=10)

        self.entry_dept = tk.Entry(self.frame, width=20)
        self.entry_dept.grid(row=2, column=1, padx=10, pady=10)

        self.label_cred = tk.Label(self.frame, text="        Credits:", bg=labels_bg_color, fg="white")
        self.label_cred.grid(row=3, column=0, padx=10, pady=10)

        self.entry_cred = tk.Entry(self.frame, width=20)
        self.entry_cred.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        button_fg_color = "white"
        self.btn_insert = tk.Button(self.frame, text="Insert Course", command=self.insert_course, bg=buttons_bg_color,
                                    fg=button_fg_color, relief=tk.GROOVE, bd=2, padx=10, pady=5, borderwidth=7,
                                    highlightthickness=0, cursor="hand2")
        self.btn_insert.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_search = tk.Button(self.frame, text="Search Course", command=self.search_course, bg=buttons_bg_color,
                                    fg=button_fg_color, relief=tk.GROOVE, bd=2, padx=10, pady=5, borderwidth=7,
                                    highlightthickness=0, cursor="hand2")
        self.btn_search.grid(row=5, column=0, columnspan=2, pady=10)

        self.btn_delete = tk.Button(self.frame, text="Delete Course", command=self.delete_course, bg=buttons_bg_color,
                                    fg=button_fg_color, relief=tk.GROOVE, bd=2, padx=10, pady=5, borderwidth=7,
                                    highlightthickness=0, cursor="hand2")
        self.btn_delete.grid(row=6, column=0, columnspan=2, pady=10)

        self.btn_list = tk.Button(self.frame, text="List All Courses", command=self.list_courses, bg=buttons_bg_color,
                                    fg=button_fg_color, relief=tk.GROOVE, bd=2, padx=10, pady=5, borderwidth=7,
                                    highlightthickness=0, cursor="hand2")
        self.btn_list.grid(row=8, column=0, columnspan=2, pady=10)

        self.btn_delete = tk.Button(self.frame, text="Update Course", command=self.update_course,bg=buttons_bg_color,
                                    fg=button_fg_color, relief=tk.GROOVE, bd=2, padx=10, pady=5, borderwidth=7,
                                    highlightthickness=0, cursor="hand2")
        self.btn_delete.grid(row=7, column=0, columnspan=2, pady=10)


        self.tree = ttk.Treeview(self.frame, columns=("Course_ID", "Title", "Department", "Credits"), show="headings", height=40)
        self.tree.heading("Course_ID", text="Course_ID",  anchor="w")
        self.tree.heading("Title", text="Title",  anchor="w")
        self.tree.heading("Department", text="Department",  anchor="w")
        self.tree.heading("Credits", text="Credits",  anchor="w")
        self.tree.grid(row=0, column=2, columnspan=2, rowspan=20, padx=(200, 0), pady=10, sticky='e')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
    def close(self):
        self.root.mainloop()

    def on_close(self):
        result = messagebox.askokcancel("Close", "Do you really want to close the window?")
        if result:
            self.closew = True
            self.root.destroy()

    def r(self):
        return self.closew
    def insert_course(self):
        # Get values from entry fields
        course_id = self.entry_id.get()
        course_title = self.entry_title.get()
        dept_name = self.entry_dept.get()
        cred = self.entry_cred.get()

        # Validate  ID
        if not course_id:
            messagebox.showerror("Error", "Enter a course id .")
            return
        if len(course_id) > 8:
            messagebox.showerror("Error", "Course id too long enter at most 7 characters.")
            return
        # Validate credit
        if not cred.isdigit() or int(cred) < 0:
            messagebox.showerror("Error", "credit must be a non-negative numeric value.")
            return

        # Check for empty values
        if not course_title or not dept_name:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if the department exists
        self.cursor.execute("SELECT * FROM department WHERE dept_name=?", (dept_name,))
        existing_dept = self.cursor.fetchone()

        if not existing_dept:
            messagebox.showerror("Error", "Department does not exist. Please choose a valid department.")
            return

        # Check if the student ID already exists
        self.cursor.execute("SELECT * FROM course WHERE course_id=?", (course_id,))
        existing_course = self.cursor.fetchone()

        if existing_course:
            messagebox.showerror("Error", "Course with the given ID already exists. Please choose a different ID.")
        else:
            # Insert the new student
            self.cursor.execute("INSERT INTO course VALUES (?, ?, ?, ?)",
                                (course_id, course_title, dept_name, cred))
            self.db.commit()

            messagebox.showinfo("Success", "Course inserted successfully!")
            self.clear_entries()
            self.list_courses()

    def search_course(self):
        course_id = self.entry_id.get()

        if not course_id:
            messagebox.showerror("Error", "Please specify a course ID TO search.")
            return
        self.cursor.execute("SELECT * FROM course WHERE course_id=?", (course_id,))
        course = self.cursor.fetchone()

        if course:
            self.entry_title.delete(0, tk.END)
            self.entry_title.insert(0, course[1])

            self.entry_dept.delete(0, tk.END)
            self.entry_dept.insert(0, course[2])

            self.entry_cred.delete(0, tk.END)
            self.entry_cred.insert(0, course[3])
        else:
            messagebox.showinfo("Course Not Found", "Course with given ID not found.")
        # if course:
        #     info_message = f"Student ID: {course[0]}\nName: {course[1]}\nDepartment: {course[2]}\nCredits: {course[3]}"
        #     messagebox.showinfo("Student Information", info_message)
        # else:
        #     messagebox.showinfo("Student Not Found", "Student with given ID not found.")

    def delete_course(self):
        course_id = self.entry_id.get()

        # Check if the student ID is not specified
        if not course_id:
            messagebox.showerror("Error", "Please specify a Course ID for deletion.")
            return

        # Check if the student ID exists
        self.cursor.execute("SELECT * FROM course WHERE course_id=?", (course_id,))
        existing_course = self.cursor.fetchone()

        if not existing_course:
            messagebox.showerror("Error", f"Course with ID {course_id} does not exist.")
            return

        # Ask for confirmation before deletion
        confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete course with ID {course_id}?")

        if confirmation:
            self.cursor.execute("DELETE FROM course WHERE course_id=?", (course_id,))
            self.db.commit()
            messagebox.showinfo("Success", "Course deleted successfully!")
            self.clear_entries()
            self.list_courses()
    def update_course(self):
        course_id = self.entry_id.get()

        if not course_id:
            messagebox.showerror("Error", "Please specify a Student ID , and press the Search button,\nand then modify the fields as needed TO update.")
            return
        self.cursor.execute("SELECT * FROM course WHERE course_id=?", (course_id,))
        course = self.cursor.fetchone()
        if course:
            new_id = self.entry_id.get()
            course_title = self.entry_title.get()
            dept_name = self.entry_dept.get()
            cred = self.entry_cred.get()

            self.cursor.execute("SELECT * FROM department WHERE dept_name=?", (dept_name,))
            existing_dept = self.cursor.fetchone()

            if not existing_dept:
                messagebox.showerror("Error", "Department does not exist. Please choose a valid department.")
                return

            self.cursor.execute("UPDATE course SET course_id = ?, title = ?, dept_name = ?, credits = ?  WHERE course_id = ? ",
                                (new_id, course_title, dept_name, cred, course_id))
            self.db.commit()

            messagebox.showinfo("Success", "Course updated successfully!")
            self.clear_entries()
            self.list_courses()
        else:
            messagebox.showerror("Error", " The course with this id is not int the system")
            return

    def list_courses(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing data in the Treeview

        self.cursor.execute("SELECT * FROM course")
        courses = self.cursor.fetchall()

        for course in courses:
            self.tree.insert("", "end", values=course)

    def clear_entries(self):
        self.entry_id.delete(0, tk.END)
        self.entry_title.delete(0, tk.END)
        self.entry_dept.delete(0, tk.END)
        self.entry_cred.delete(0, tk.END)


if __name__ == "__main__":
    app = Course()
    app.close()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Course Management System")
        self.root.iconbitmap('icons/eul.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Set background colors
        label_bg_color = "#2E4374"
        entry_bg_color = "#4B527E"
        button_bg_color = "#7C81AD"
        tree_bg_color = "#7C81AD"

        # Create or open the database
        self.db = sqlite3.connect('test3.db')
        self.cursor = self.db.cursor()
        self.closew = False

        # GUI elements
        self.label_id = tk.Label(self.root, text="  Course ID:", bg=label_bg_color, fg="white")
        self.label_id.grid(row=0, column=0, padx=10, pady=(30, 10), sticky='w')

        self.entry_id = tk.Entry(self.root, width=20, bg=entry_bg_color)
        self.entry_id.grid(row=0, column=1, padx=10, pady=(30, 10))

        self.title = tk.Label(self.root, text="Course Title:", bg=label_bg_color, fg="white")
        self.title.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        self.entry_title = tk.Entry(self.root, width=20, bg=entry_bg_color)
        self.entry_title.grid(row=1, column=1, padx=10, pady=10)

        self.label_dept = tk.Label(self.root, text="Department:", bg=label_bg_color, fg="white")
        self.label_dept.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        self.entry_dept = tk.Entry(self.root, width=20, bg=entry_bg_color)
        self.entry_dept.grid(row=2, column=1, padx=10, pady=10)

        self.label_cred = tk.Label(self.root, text="        Credits:", bg=label_bg_color, fg="white")
        self.label_cred.grid(row=3, column=0, padx=10, pady=10, sticky='w')

        self.entry_cred = tk.Entry(self.root, width=20, bg=entry_bg_color)
        self.entry_cred.grid(row=3, column=1, padx=10, pady=10)

        # Buttons
        button_fg_color = "white"
        self.btn_insert = tk.Button(self.root, text="Insert Course", command=self.insert_course, bg=button_bg_color,
                                    fg=button_fg_color)
        self.btn_insert.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_search = tk.Button(self.root, text="Search Course", command=self.search_course, bg=button_bg_color,
                                    fg=button_fg_color)
        self.btn_search.grid(row=5, column=0, columnspan=2, pady=10)

        self.btn_delete = tk.Button(self.root, text="Delete Course", command=self.delete_course, bg=button_bg_color,
                                    fg=button_fg_color)
        self.btn_delete.grid(row=6, column=0, columnspan=2, pady=10)

        self.btn_list = tk.Button(self.root, text="List All Courses", command=self.list_courses, bg=button_bg_color,
                                  fg=button_fg_color)
        self.btn_list.grid(row=8, column=0, columnspan=2, pady=10)

        self.btn_delete = tk.Button(self.root, text="Update Course", command=self.update_course, bg=button_bg_color,
                                    fg=button_fg_color)
        self.btn_delete.grid(row=7, column=0, columnspan=2, pady=10)

        # Treeview
        self.tree = ttk.Treeview(self.root, columns=("Course_ID", "Title", "Department", "Credits"), show="headings",
                                 height=20, selectmode="browse", style="Treeview")
        self.tree.heading("Course_ID", text="Course_ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Credits", text="Credits")
        self.tree.grid(row=0, column=2, rowspan=10, padx=10, pady=50, sticky='nsew')

        # Configure Treeview style
        style = ttk.Style(self.root)
        style.configure("Treeview", background=tree_bg_color, fieldbackground=tree_bg_color, foreground="white")

        # Set weights for grid resizing
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
    def close(self):
        self.root.mainloop()

    def on_close(self):
        result = messagebox.askokcancel("Close", "Do you really want to close the window?")
        if result:
            self.closew = True
            self.root.destroy()

    def r(self):
        return self.closew
    def insert_course(self):
        # Get values from entry fields
        course_id = self.entry_id.get()
        course_title = self.entry_title.get()
        dept_name = self.entry_dept.get()
        cred = self.entry_cred.get()

        # Validate  ID
        if not course_id:
            messagebox.showerror("Error", "Enter a course id .")
            return
        if len(course_id) > 8:
            messagebox.showerror("Error", "Course id too long enter at most 7 characters.")
            return
        # Validate credit
        if not cred.isdigit() or int(cred) < 0:
            messagebox.showerror("Error", "credit must be a non-negative numeric value.")
            return

        # Check for empty values
        if not course_title or not dept_name:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if the department exists
        self.cursor.execute("SELECT * FROM department WHERE dept_name=?", (dept_name,))
        existing_dept = self.cursor.fetchone()

        if not existing_dept:
            messagebox.showerror("Error", "Department does not exist. Please choose a valid department.")
            return

        # Check if the student ID already exists
        self.cursor.execute("SELECT * FROM course WHERE course_id=?", (course_id,))
        existing_course = self.cursor.fetchone()

        if existing_course:
            messagebox.showerror("Error", "Course with the given ID already exists. Please choose a different ID.")
        else:
            # Insert the new student
            self.cursor.execute("INSERT INTO course VALUES (?, ?, ?, ?)",
                                (course_id, course_title, dept_name, cred))
            self.db.commit()

            messagebox.showinfo("Success", "Course inserted successfully!")
            self.clear_entries()
            self.list_courses()

    def search_course(self):
        course_id = self.entry_id.get()

        if not course_id:
            messagebox.showerror("Error", "Please specify a course ID TO search.")
            return
        self.cursor.execute("SELECT * FROM course WHERE course_id=?", (course_id,))
        course = self.cursor.fetchone()

        if course:
            self.entry_title.delete(0, tk.END)
            self.entry_title.insert(0, course[1])

            self.entry_dept.delete(0, tk.END)
            self.entry_dept.insert(0, course[2])

            self.entry_cred.delete(0, tk.END)
            self.entry_cred.insert(0, course[3])
        else:
            messagebox.showinfo("Course Not Found", "Course with given ID not found.")
        # if course:
        #     info_message = f"Student ID: {course[0]}\nName: {course[1]}\nDepartment: {course[2]}\nCredits: {course[3]}"
        #     messagebox.showinfo("Student Information", info_message)
        # else:
        #     messagebox.showinfo("Student Not Found", "Student with given ID not found.")

    def delete_course(self):
        course_id = self.entry_id.get()

        # Check if the student ID is not specified
        if not course_id:
            messagebox.showerror("Error", "Please specify a Course ID for deletion.")
            return

        # Check if the student ID exists
        self.cursor.execute("SELECT * FROM course WHERE course_id=?", (course_id,))
        existing_course = self.cursor.fetchone()

        if not existing_course:
            messagebox.showerror("Error", f"Course with ID {course_id} does not exist.")
            return

        # Ask for confirmation before deletion
        confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete course with ID {course_id}?")

        if confirmation:
            self.cursor.execute("DELETE FROM course WHERE course_id=?", (course_id,))
            self.db.commit()
            messagebox.showinfo("Success", "Course deleted successfully!")
            self.clear_entries()
            self.list_courses()
    def update_course(self):
        course_id = self.entry_id.get()

        if not course_id:
            messagebox.showerror("Error", "Please specify a Student ID , and press the Search button,\nand then modify the fields as needed TO update.")
            return
        self.cursor.execute("SELECT * FROM course WHERE course_id=?", (course_id,))
        course = self.cursor.fetchone()
        if course:
            new_id = self.entry_id.get()
            course_title = self.entry_title.get()
            dept_name = self.entry_dept.get()
            cred = self.entry_cred.get()

            self.cursor.execute("SELECT * FROM department WHERE dept_name=?", (dept_name,))
            existing_dept = self.cursor.fetchone()

            if not existing_dept:
                messagebox.showerror("Error", "Department does not exist. Please choose a valid department.")
                return

            self.cursor.execute("UPDATE course SET course_id = ?, title = ?, dept_name = ?, credits = ?  WHERE course_id = ? ",
                                (new_id, course_title, dept_name, cred, course_id))
            self.db.commit()

            messagebox.showinfo("Success", "Course updated successfully!")
            self.clear_entries()
            self.list_courses()
        else:
            messagebox.showerror("Error", " The course with this id is not int the system")
            return

    def list_courses(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing data in the Treeview

        self.cursor.execute("SELECT * FROM course")
        courses = self.cursor.fetchall()

        for course in courses:
            self.tree.insert("", "end", values=course)

    def clear_entries(self):
        self.entry_id.delete(0, tk.END)
        self.entry_title.delete(0, tk.END)
        self.entry_dept.delete(0, tk.END)
        self.entry_cred.delete(0, tk.END)


if __name__ == "__main__":
    app = Course()
    app.close()
