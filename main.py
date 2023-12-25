import tkinter as tk
from tkinter import messagebox, PhotoImage
from student import StudentManagementApp
from department import Department
from course import Course
from instructor import Instructor



def w_close():
    result = messagebox.askokcancel("Close", "Do you really want to close the window?")
    if result:
        root.destroy()

root = tk.Tk()
root.title("Student Management System")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window dimensions to match the screen resolution
root.geometry(f"{screen_width}x{screen_height}+0+0")
# Set the background color to blue
root.protocol("WM_DELETE_WINDOW", w_close)
background_image = PhotoImage(file="pic.png")  # Change "background.png" to your image file
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)
def open_app(app_class):
    global close
    root.withdraw()
    app = app_class()

    # Wait for the app window to be closed
    app.root.wait_window(app.root)

    if app.r():
        root.deiconify()


def open_student_management():
    messagebox.showinfo("Instructions",
                        "Welcome to the Student Management System!\n\n"
                        "Instructions:\n"
                        "1. Insert Student: Click 'Insert Student' button to add a new student.\n"
                        "2. Search Student: Click 'Search Student' button to find a student by ID.\n"
                        "3. Delete Student: Click 'Delete Student' button to remove a student by ID.\n"
                        "4. List All Students: Click 'List All Students' button to view all students.\n"
                        "5. Update Student: Click 'Update Student' button to modify student information.\n\n"
                        "Note: Please enter the Student ID before performing search, delete, or update operations."
                        )

    open_app(StudentManagementApp)


def open_course():
    messagebox.showinfo("Instructions",
                        "Welcome to the Course Management System!\n\n"
                        "Instructions:\n"
                        "1. Insert Course: Click 'Insert Course' button to add a new course.\n"
                        "2. Search Course: Click 'Search Course' button to find a course by ID.\n"
                        "3. Delete Course: Click 'Delete Course' button to remove a course by ID.\n"
                        "4. List All Courses: Click 'List All Courses' button to view all courses.\n"
                        "5. Update Course: Click 'Update Course' button to modify course information.\n\n"
                        "Note: Please enter the Course ID before performing search, delete, or update operations."
                        )

    open_app(Course)


def open_department():
    messagebox.showinfo("Instructions",
                        "Welcome to the Department Management System!\n\n"
                        "Instructions:\n"
                        "1. Insert Department: Click 'Insert Department' button to add a new department.\n"
                        "2. Search Department: Click 'Search Department' button to find a department by name.\n"
                        "3. Delete Department: Click 'Delete Department' button to remove a department by name.\n"
                        "4. List All Departments: Click 'List All Departments' button to view all departments.\n\n"
                        "Note: Please enter the Department Name before performing search or delete operations."
                        )

    open_app(Department)


def open_instructor():
    messagebox.showinfo("Instructions",
                        "Welcome to the Instructor Management System!\n\n"
                        "Instructions:\n"
                        "1. Insert Instructor: Click 'Insert Instructor' button to add a new instructor.\n"
                        "2. Search Instructor: Click 'Search Instructor' button to find an instructor by ID.\n"
                        "3. Delete Instructor: Click 'Delete Instructor' button to remove an instructor by ID.\n"
                        "4. List All Instructors: Click 'List All Instructors' button to view all instructors.\n"
                        "5. Update Instructor: Click 'Update Instructor' button to modify instructor information.\n\n"
                        "Note: Please enter the Instructor ID before performing search, delete, or update operations."
                        )

    open_app(Instructor)



main_frame = tk.Frame(root, bg="#3498db")  # Frame to hold the buttons
main_frame.grid(row=1, column=0, padx=50, pady=50)

welcome_label = tk.Label(root, text="WELCOME TO THE UNIVERSITY MANAGEMENT SYSTEM \n PRESS ANY BUTTON TO LOGIN", font=("Arial", 14), bg="#3498db", fg="white")
welcome_label.grid(row=0, column=0, pady=20)

btn_insert = tk.Button(main_frame, text="Student", command=open_student_management, bg="#8e44ad", fg="white", padx=20, pady=5, width=20)
btn_insert.grid(row=0, column=0, pady=10)

btn_search = tk.Button(main_frame, text="Course", command=open_course, bg="#8e44ad", fg="white", padx=20, pady=5, width=20)
btn_search.grid(row=1, column=0, pady=10)

btn_delete = tk.Button(main_frame, text="Department", command=open_department, bg="#8e44ad", fg="white", padx=20, pady=5, width=20)
btn_delete.grid(row=2, column=0, pady=10)

btn_list = tk.Button(main_frame, text="Instructor", command=open_instructor, bg="#8e44ad", fg="white", padx=20, pady=5, width=20)
btn_list.grid(row=3, column=0, pady=10)

root.mainloop()
