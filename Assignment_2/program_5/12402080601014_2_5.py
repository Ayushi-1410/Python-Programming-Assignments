import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=password.get(),
            database="college_db"
        )
    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))
        return None

def valid_email(email):
    pattern = r'^[A-Za-z0-9._+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$'
    return re.fullmatch(pattern, email) is not None

def add_contact():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    category = category_box.get()
    notes = notes_entry.get().strip()

    if not name or not valid_email(email):
        messagebox.showwarning("Validation", "Enter a name and valid email.")
        return

    db = connect_db()
    if db is None:
        return

    try:
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO Contact
            (name,email,phone,category,notes)
            VALUES (%s,%s,%s,%s,%s)""",
            (name, email, phone, category, notes)
        )
        db.commit()
        messagebox.showinfo("Success", "Contact added.")
        show_contacts()
    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))
    finally:
        db.close()

def show_contacts():
    db = connect_db()
    if db is None:
        return

    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT id,name,email,phone,category,notes FROM Contact ORDER BY name"
        )
        rows = cursor.fetchall()

        for item in table.get_children():
            table.delete(item)

        for row in rows:
            table.insert("", "end", values=row)

        cursor.close()
    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))
    finally:
        db.close()

def delete_contact():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Select", "Select a contact first.")
        return

    contact_id = table.item(selected[0], "values")[0]
    db = connect_db()

    if db is None:
        return

    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM Contact WHERE id=%s", (contact_id,))
        db.commit()
        show_contacts()
    except mysql.connector.Error as error:
        messagebox.showerror("Error", str(error))
    finally:
        db.close()

root = tk.Tk()
root.title("Contact Manager")
root.geometry("850x500")

tk.Label(root, text="MySQL Password").pack()
password = tk.Entry(root, show="*")
password.pack()

tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Phone").pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

tk.Label(root, text="Category").pack()
category_box = ttk.Combobox(
    root, values=["Friend", "Family", "Faculty", "Work"]
)
category_box.pack()

tk.Label(root, text="Notes").pack()
notes_entry = tk.Entry(root)
notes_entry.pack()

tk.Button(root, text="Add Contact", command=add_contact).pack()
tk.Button(root, text="Show Contacts", command=show_contacts).pack()
tk.Button(root, text="Delete Selected", command=delete_contact).pack()

table = ttk.Treeview(
    root,
    columns=("id", "name", "email", "phone", "category", "notes"),
    show="headings"
)

for column in ("id", "name", "email", "phone", "category", "notes"):
    table.heading(column, text=column.title())
    table.column(column, width=120)

table.pack(fill="both", expand=True)

root.mainloop()