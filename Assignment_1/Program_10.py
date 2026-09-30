import tkinter as tk
from tkinter import messagebox
import json
import csv

data = []


def load_data():
    global data

    try:
        with open("assignments.json", "r") as file:
            data = json.load(file)
    except:
        data = []


def save_data():
    with open("assignments.json", "w") as file:
        json.dump(data, file)


def add_assignment():

    enrollment = enrollment_entry.get()
    name = name_entry.get()
    assignment = assignment_entry.get()
    marks = marks_entry.get()
    status = status_var.get()

    if enrollment == "" or name == "" or assignment == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        marks = int(marks)
    except:
        messagebox.showerror("Error", "Marks must be a number")
        return

    if marks < 0 or marks > 20:
        messagebox.showerror("Error", "Marks must be between 0 and 20")
        return

    record = {
        "enrollment": enrollment,
        "name": name,
        "assignment": assignment,
        "status": status,
        "marks": marks
    }

    data.append(record)

    save_data()
    show_data()

    enrollment_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    assignment_entry.delete(0, tk.END)
    marks_entry.delete(0, tk.END)


def show_data():

    listbox.delete(0, tk.END)

    selected = filter_var.get()

    for record in data:

        if selected != "ALL" and record["status"] != selected:
            continue

        text = (
            record["enrollment"] + " | " +
            record["name"] + " | " +
            record["assignment"] + " | " +
            record["status"] + " | " +
            str(record["marks"]) + "/20"
        )

        listbox.insert(tk.END, text)


def export_csv():

    with open("assignments.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Enrollment",
            "Name",
            "Assignment",
            "Status",
            "Marks"
        ])

        for record in data:

            writer.writerow([
                record["enrollment"],
                record["name"],
                record["assignment"],
                record["status"],
                record["marks"]
            ])

    messagebox.showinfo(
        "Success",
        "CSV file created successfully"
    )


load_data()

root = tk.Tk()
root.title("Assignment Tracker")
root.geometry("500x500")
root.resizable(False, False)

tk.Label(
    root,
    text="Assignment Tracker",
    font=("Arial", 16, "bold")
).pack(pady=8)

tk.Label(root, text="Enrollment Number").pack()

enrollment_entry = tk.Entry(root, width=35)
enrollment_entry.pack()

tk.Label(root, text="Student Name").pack()

name_entry = tk.Entry(root, width=35)
name_entry.pack()

tk.Label(root, text="Assignment Name").pack()

assignment_entry = tk.Entry(root, width=35)
assignment_entry.pack()

tk.Label(root, text="Marks (0-20)").pack()

marks_entry = tk.Entry(root, width=35)
marks_entry.pack()

status_var = tk.StringVar()
status_var.set("Pending")

tk.Label(root, text="Status").pack()

tk.Radiobutton(
    root,
    text="Pending",
    variable=status_var,
    value="Pending"
).pack()

tk.Radiobutton(
    root,
    text="Completed",
    variable=status_var,
    value="Completed"
).pack()

tk.Button(
    root,
    text="Add Assignment",
    command=add_assignment,
    width=18
).pack(pady=5)

filter_var = tk.StringVar()
filter_var.set("ALL")

tk.Label(root, text="Filter").pack()

tk.OptionMenu(
    root,
    filter_var,
    "ALL",
    "Pending",
    "Completed",
    command=lambda x: show_data()
).pack()

listbox = tk.Listbox(
    root,
    width=65,
    height=7
)

listbox.pack(pady=8)

tk.Button(
    root,
    text="Show Data",
    command=show_data,
    width=18
).pack(pady=2)

tk.Button(
    root,
    text="Export CSV",
    command=export_csv,
    width=18
).pack(pady=2)

show_data()

root.mainloop()