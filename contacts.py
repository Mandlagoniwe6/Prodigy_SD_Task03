import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# File to store contacts
CONTACTS_FILE = "contacts.json"

# Loading contacts from file
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return {}

# Saving contacts to file
def save_contacts():
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

# Adding a new contact
def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if not name or not phone or not email:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    if name in contacts:
        messagebox.showerror("Duplicate Entry", "Contact already exists!")
        return

    contacts[name] = {"phone": phone, "email": email}
    save_contacts()
    refresh_contacts()
    clear_entries()
    messagebox.showinfo("Success", "Contact added successfully!")

# Viewing selected contact
def view_contact(event):
    selected_item = contacts_tree.selection()
    if selected_item:
        name = contacts_tree.item(selected_item)["values"][0]
        contact = contacts[name]
        name_entry.delete(0, tk.END)
        name_entry.insert(0, name)
        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, contact["phone"])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, contact["email"])

# Editing a contact
def edit_contact():
    selected_item = contacts_tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "No contact selected!")
        return

    confirm = messagebox.askyesno("Confirm Edit", "Are you sure you want to edit this contact?")
    if not confirm:
        return

    old_name = contacts_tree.item(selected_item)["values"][0]
    new_name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if not new_name or not phone or not email:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    del contacts[old_name]
    contacts[new_name] = {"phone": phone, "email": email}
    save_contacts()
    refresh_contacts()
    clear_entries()
    messagebox.showinfo("Success", "Contact updated successfully!")

# Deleting a contact
def delete_contact():
    selected_item = contacts_tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "No contact selected!")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
    if not confirm:
        return

    name = contacts_tree.item(selected_item)["values"][0]
    del contacts[name]
    save_contacts()
    refresh_contacts()
    clear_entries()
    messagebox.showinfo("Success", "Contact deleted successfully!")

# Refreshing contacts display
def refresh_contacts():
    contacts_tree.delete(*contacts_tree.get_children())
    for name, info in contacts.items():
        contacts_tree.insert("", tk.END, values=(name, info["phone"], info["email"]))

# Clearing input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Main application
app = tk.Tk()
app.title("Contact Management System")
app.geometry("600x500")
app.resizable(False, False)

app.configure(bg="#1E1E2F")
frame_bg = "#29293D"
btn_bg = "#3A3A5D"
btn_fg = "#FFFFFF"
entry_bg = "#3A3A5D"
entry_fg = "#FFFFFF"
tree_bg = "#29293D"
tree_fg = "#FFFFFF"
tree_alt_bg = "#35354F"
tree_highlight = "#44445F"

# Contacts dictionary
contacts = load_contacts()

frame = tk.Frame(app, bg=frame_bg, padx=10, pady=10)
frame.pack(fill="both", expand=True)


tk.Label(frame, text="Name", bg=frame_bg, fg=btn_fg).grid(row=0, column=0, padx=5, pady=5, sticky="e")
name_entry = tk.Entry(frame, bg=entry_bg, fg=entry_fg, insertbackground="white")
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Phone", bg=frame_bg, fg=btn_fg).grid(row=1, column=0, padx=5, pady=5, sticky="e")
phone_entry = tk.Entry(frame, bg=entry_bg, fg=entry_fg, insertbackground="white")
phone_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Email", bg=frame_bg, fg=btn_fg).grid(row=2, column=0, padx=5, pady=5, sticky="e")
email_entry = tk.Entry(frame, bg=entry_bg, fg=entry_fg, insertbackground="white")
email_entry.grid(row=2, column=1, padx=5, pady=5)

btn_frame = tk.Frame(frame, bg=frame_bg)
btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(btn_frame, text="Add Contact", command=add_contact, bg=btn_bg, fg=btn_fg, width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Edit Contact", command=edit_contact, bg=btn_bg, fg=btn_fg, width=12).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Contact", command=delete_contact, bg=btn_bg, fg=btn_fg, width=12).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_entries, bg=btn_bg, fg=btn_fg, width=12).grid(row=0, column=3, padx=5)

# Contacts Treeview
columns = ("Name", "Phone", "Email")
contacts_tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
contacts_tree.grid(row=4, column=0, columnspan=2, pady=10)
for col in columns:
    contacts_tree.heading(col, text=col)
    contacts_tree.column(col, anchor="center")
contacts_tree.bind("<Double-1>", view_contact)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background=tree_bg, foreground=tree_fg, fieldbackground=tree_bg)
style.map("Treeview", background=[("selected", tree_highlight)])
style.configure("Treeview.Heading", background=btn_bg, foreground=btn_fg)

refresh_contacts()
app.mainloop()
 
