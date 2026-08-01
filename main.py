import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Database connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    course TEXT,
    email TEXT
)
""")

conn.commit()


# Main Window
root = tk.Tk()
root.title("Student Management System")
root.geometry("700x650")
root.resizable(False, False)


# Title
title = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 20, "bold")
)
title.pack(pady=10)


# Frame
frame = tk.Frame(root)
frame.pack(pady=10)


# Labels and Entries

tk.Label(frame, text="Name").grid(row=0, column=0, padx=10, pady=5)
name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1)


tk.Label(frame, text="Age").grid(row=1, column=0, padx=10, pady=5)
age_entry = tk.Entry(frame)
age_entry.grid(row=1, column=1)


tk.Label(frame, text="Gender").grid(row=2, column=0, padx=10, pady=5)

gender = tk.StringVar()

gender_box = ttk.Combobox(
    frame,
    textvariable=gender,
    values=["Male", "Female", "Other"]
)

gender_box.grid(row=2, column=1)


tk.Label(frame, text="Course").grid(row=3, column=0, padx=10, pady=5)
course_entry = tk.Entry(frame)
course_entry.grid(row=3, column=1)


tk.Label(frame, text="Email").grid(row=4, column=0, padx=10, pady=5)
email_entry = tk.Entry(frame)
email_entry.grid(row=4, column=1)



# Add Student Function

def add_student():

    name = name_entry.get()
    age = age_entry.get()
    gen = gender.get()
    course = course_entry.get()
    email = email_entry.get()


    if name == "" or age == "" or course == "":
        messagebox.showerror(
            "Error",
            "Please fill required fields"
        )
        return


    cursor.execute(
        """
        INSERT INTO students(name,age,gender,course,email)
        VALUES(?,?,?,?,?)
        """,
        (name, age, gen, course, email)
    )

    conn.commit()

    messagebox.showinfo(
        "Success",
        "Student Added Successfully"
    )


    name_entry.delete(0,tk.END)
    age_entry.delete(0,tk.END)
    course_entry.delete(0,tk.END)
    email_entry.delete(0,tk.END)



# Add Button

add_btn = tk.Button(
    root,
    text="Add Student",
    width=20,
    command=lambda: [add_student(), view_students()]

)

add_btn.pack(pady=10)



# ==========================
# View Student Table
# ==========================

columns = ("ID", "Name", "Age", "Gender", "Course", "Email")

student_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=8
)

for col in columns:
    student_table.heading(col, text=col)
    student_table.column(col, width=100)

student_table.pack(pady=20)



# Display Students Function

def view_students():

    for row in student_table.get_children():
        student_table.delete(row)

    cursor.execute("SELECT * FROM students")

    data = cursor.fetchall()

    for row in data:
        student_table.insert("", tk.END, values=row)



# ==========================
# Search Student
# ==========================

search_frame = tk.Frame(root)
search_frame.pack()


tk.Label(
    search_frame,
    text="Search Name"
).grid(row=0,column=0,padx=5)


search_entry = tk.Entry(search_frame)
search_entry.grid(row=0,column=1,padx=5)



def search_student():

    name = search_entry.get()

    for row in student_table.get_children():
        student_table.delete(row)


    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        ('%'+name+'%',)
    )

    result = cursor.fetchall()


    for row in result:
        student_table.insert(
            "",
            tk.END,
            values=row
        )



search_btn = tk.Button(
    search_frame,
    text="Search",
    command=search_student
)

search_btn.grid(row=0,column=2,padx=5)



# ==========================
# Delete Student
# ==========================

def delete_student():

    selected = student_table.focus()

    if selected == "":
        messagebox.showerror(
            "Error",
            "Select a student first"
        )
        return


    values = student_table.item(selected)["values"]

    student_id = values[0]


    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )

    conn.commit()


    messagebox.showinfo(
        "Deleted",
        "Student Deleted Successfully"
    )

    view_students()



# Buttons

button_frame = tk.Frame(root)
button_frame.pack(pady=10)


view_btn = tk.Button(
    button_frame,
    text="View Students",
    width=15,
    command=view_students
)

view_btn.grid(row=0,column=0,padx=10)



delete_btn = tk.Button(
    button_frame,
    text="Delete Student",
    width=15,
    command=delete_student
)

delete_btn.grid(row=0,column=1,padx=10)



# Run Application

# ==========================
# Update Student
# ==========================

def select_student(event):

    selected = student_table.focus()

    if selected:

        values = student_table.item(selected)["values"]

        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])

        age_entry.delete(0, tk.END)
        age_entry.insert(0, values[2])

        gender.set(values[3])

        course_entry.delete(0, tk.END)
        course_entry.insert(0, values[4])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, values[5])



student_table.bind(
    "<ButtonRelease-1>",
    select_student
)



def update_student():

    selected = student_table.focus()

    if selected == "":
        messagebox.showerror(
            "Error",
            "Select a student first"
        )
        return


    values = student_table.item(selected)["values"]

    student_id = values[0]


    name = name_entry.get()
    age = age_entry.get()
    gen = gender.get()
    course = course_entry.get()
    email = email_entry.get()


    cursor.execute(
        """
        UPDATE students
        SET name=?, age=?, gender=?, course=?, email=?
        WHERE id=?
        """,
        (
            name,
            age,
            gen,
            course,
            email,
            student_id
        )
    )

    conn.commit()


    messagebox.showinfo(
        "Updated",
        "Student Updated Successfully"
    )


    view_students()



# ==========================
# Clear Fields
# ==========================

def clear_fields():

    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

    gender.set("")



# ==========================
# Update & Clear Buttons
# ==========================

update_btn = tk.Button(
    button_frame,
    text="Update Student",
    width=15,
    command=update_student
)

update_btn.grid(row=0,column=2,padx=10)



clear_btn = tk.Button(
    button_frame,
    text="Clear",
    width=15,
    command=clear_fields
)

clear_btn.grid(row=0,column=3,padx=10)



# Start Application
view_students()
root.mainloop()