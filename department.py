import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from time import sleep


class Department:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Department Management System")
        self.root.iconbitmap('icons/eul.ico')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the window dimensions to match the screen resolution
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        # self.root.geometry("1000x600")
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
        # Create or open the student table

        # GUI elements
        # GUI elements
        self.dep_name = tk.Label(self.frame, text="Department name:", bg=labels_bg_color, fg="white")
        self.dep_name.grid(row=0, column=0, padx=10, pady=(10, 10), sticky='w')

        self.entry_name = tk.Entry(self.frame, width=20)
        self.entry_name.grid(row=0, column=1, padx=50, pady=(30, 10))

        self.building = tk.Label(self.frame, text="   Building name:", bg=labels_bg_color, fg="white")
        self.building.grid(row=1, column=0, padx=10, pady=10)

        self.entry_build = tk.Entry(self.frame, width=20)
        self.entry_build.grid(row=1, column=1, padx=10, pady=10)

        self.label_budget = tk.Label(self.frame, text="Budget:", bg=labels_bg_color ,fg="white")
        self.label_budget.grid(row=2, column=0, padx=10, pady=10)

        self.entry_budget = tk.Entry(self.frame, width=20)
        self.entry_budget.grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        button_fg_color = "white"
        self.btn_insert = tk.Button(self.frame, text="Insert Department", command=self.insert_dep, bg=buttons_bg_color,
                                    fg=button_fg_color, relief=tk.GROOVE, bd=2, padx=10, pady=5, borderwidth=7,
                                    highlightthickness=0, cursor="hand2")
        self.btn_insert.grid(row=4, column=0, columnspan=2, pady=10)

        self.btn_search = tk.Button(self.frame, text="Search Department", command=self.search_dept, bg=buttons_bg_color,
                                    fg=button_fg_color, relief=tk.GROOVE, bd=2, padx=10, pady=5, borderwidth=7,
                                    highlightthickness=0, cursor="hand2")
        self.btn_search.grid(row=5, column=0, columnspan=2, pady=10)

        self.btn_delete = tk.Button(self.frame, text="Delete Department", command=self.delete_dept, bg=buttons_bg_color,
                                    fg=button_fg_color, relief=tk.GROOVE, bd=2, padx=10, pady=5, borderwidth=7,
                                    highlightthickness=0, cursor="hand2")
        self.btn_delete.grid(row=6, column=0, columnspan=2, pady=10)

        self.btn_list = tk.Button(self.frame, text="List All Departments", command=self.list_depts, bg=buttons_bg_color,
                                    fg=button_fg_color, relief=tk.GROOVE, bd=2, padx=10, pady=5, borderwidth=7, highlightthickness=0, cursor="hand2")
        self.btn_list.grid(row=8, column=0, columnspan=2, pady=10)

        self.btn_delete = tk.Button(self.frame, text="Update Department", command=self.update_dept, bg=buttons_bg_color,
                                    fg=button_fg_color, relief=tk.GROOVE, bd=2, padx=10, pady=5, borderwidth=7,
                                    highlightthickness=0, cursor="hand2")
        self.btn_delete.grid(row=7, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.frame, columns=("dept_name", "building", "budget"), show="headings", height=40)
        self.tree.heading("dept_name", text="Department name",  anchor="w")
        self.tree.heading("building", text="Building Name",  anchor="w")
        self.tree.heading("budget", text="Department budget ",  anchor="w")

        self.tree.grid(row=0, column=2, columnspan=2, rowspan=20, padx=(200, 0), pady=10, sticky='e')

    def close(self):
        self.root.mainloop()

    def on_close(self):
        result = messagebox.askokcancel("Close", "Do you really want to close the window?")
        if result:
            self.closew = True
            self.root.destroy()

    def r(self):
        return self.closew
    def insert_dep(self):
        # Get values from entry fields
        dept_name = self.entry_name.get()
        build_name = self.entry_build.get()
        dept_budget = self.entry_budget.get()


        if dept_name.isdigit() or len(dept_name) == 0:
            messagebox.showerror("Error", "Enter Department name and it  must be a non-digit value.")
            return


        if not build_name:
            messagebox.showerror("Error", " Please Enter building name.")
            return

        dept_budget = self.entry_budget.get()

        if not dept_budget.isdigit() or int(dept_budget) <= 0:
            messagebox.showerror("Error", "Please enter a valid budget greater than zero.")
            return

        # Check if the department exists

        self.cursor.execute("SELECT * FROM department WHERE dept_name=?", (dept_name,))
        existing_dept = self.cursor.fetchone()

        if existing_dept:
            messagebox.showerror("Error",
                                 "Department with the given name already exists. Please choose a different ID.")
        else:
            # Insert the new student
            self.cursor.execute("INSERT INTO department VALUES (?, ?, ?)",
                                (dept_name, build_name, dept_budget))
            self.db.commit()

            messagebox.showinfo("Success", "Department inserted successfully!")
            self.clear_entries()
            self.list_depts()

    def search_dept(self):
        dept_name = self.entry_name.get()
        if dept_name:
            self.cursor.execute("SELECT * FROM department WHERE dept_name=?", (dept_name,))
            department = self.cursor.fetchone()

            if department:
                self.entry_build.delete(0, tk.END)
                self.entry_build.insert(0, department[1])

                self.entry_budget.delete(0, tk.END)
                self.entry_budget.insert(0, department[2])
            else:
                messagebox.showinfo("Department Not Found", "Department with given name not found.")

        else:
            messagebox.showinfo("Enter Department name", "Please Enter Department name to search")
        # if student:
        #     info_message = f"Student ID: {student[0]}\nName: {student[1]}\nDepartment: {student[2]}\nCredits: {student[3]}"
        #     messagebox.showinfo("Student Information", info_message)
        # else:
        #     messagebox.showinfo("Student Not Found", "Student with given ID not found.")

    def delete_dept(self):
        dept_name = self.entry_budget.get()

        # Check if the  DEPT NAME is not specified
        if not dept_name:
            messagebox.showerror("Error", "Please specify a Department name for deletion.")
            return

        # Check if the DEPT   exists
        self.cursor.execute("SELECT * FROM department WHERE dept_name=?", (dept_name,))
        existing_dept = self.cursor.fetchone()

        if not existing_dept:
            messagebox.showerror("Error", f"Department with Name: {dept_name} does not exist.")
            return

        # Ask for confirmation before deletion
        confirmation = messagebox.askyesno("Confirmation", f"Do you want to delete this Department : {dept_name}?")

        if confirmation:
            self.cursor.execute("DELETE FROM department WHERE dept_name=?", (dept_name,))
            self.db.commit()
            messagebox.showinfo("Success", "Department deleted successfully!")
            self.clear_entries()
            self.list_depts()

    def update_dept(self):
        dept_name = self.entry_name.get()

        if not dept_name:
            messagebox.showerror("Error", "Please specify a Department name TO UPDATE.")
            return
        self.cursor.execute("SELECT * FROM department WHERE dept_name=?", (dept_name,))
        dept = self.cursor.fetchone()
        if dept:
            new_name = self.entry_name.get()
            building = self.entry_build.get()
            budget = self.entry_budget.get()

            self.cursor.execute("SELECT * FROM department WHERE dept_name=?", (new_name,))
            existing_dept = self.cursor.fetchone()

            if not existing_dept:
                messagebox.showerror("Error", "Department does not exist. Please choose a valid department name.")
                return

            self.cursor.execute("UPDATE department SET building = ?, budget = ?  WHERE dept_name = ? ",
                                (building, budget, dept_name))
            self.db.commit()

            messagebox.showinfo("Success", "Department updated successfully!")
            self.clear_entries()
            self.list_depts()
        else:
            messagebox.showerror("Error", "you can not update a non existing the department")
            return

    def list_depts(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing data in the Treeview

        self.cursor.execute("SELECT * FROM department")
        departments = self.cursor.fetchall()

        for dept in departments:
            self.tree.insert("", "end", values=dept)

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_build.delete(0, tk.END)
        self.entry_budget.delete(0, tk.END)


if __name__ == "__main__":
    app = Department()
    app.close()

