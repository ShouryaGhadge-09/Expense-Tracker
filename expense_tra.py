import tkinter as tk
from tkinter import messagebox
import csv

expenses = []

# ---------------- FILE ----------------
def save_to_file():
    with open("expenses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Amount", "Category"])
        writer.writerows(expenses)

def load_from_file():
    try:
        with open("expenses.csv", "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                expenses.append((row[0], float(row[1]), row[2]))
    except:
        pass

# ---------------- FUNCTIONS ----------------
def add_expense():
    name = entry_name.get()
    amount = entry_amount.get()
    category = category_var.get()

    if category == "Others":
        category = entry_other.get()

    if name == "" or amount == "" or category == "":
        messagebox.showwarning("Warning", "Fill all fields")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Enter valid amount")
        return

    expenses.append((name, amount, category))
    save_to_file()
    update_list()

    entry_name.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_other.delete(0, tk.END)

def update_list():
    listbox.delete(0, tk.END)
    for i, e in enumerate(expenses):
        listbox.insert(tk.END, f"{i+1}. {e[0]} - ₹{e[1]} ({e[2]})")

def delete_expense():
    try:
        index = listbox.curselection()[0]
        expenses.pop(index)
        save_to_file()
        update_list()
    except:
        messagebox.showwarning("Warning", "Select an item")

def clear_all():
    expenses.clear()
    save_to_file()
    update_list()

def show_total():
    total = sum(e[1] for e in expenses)
    messagebox.showinfo("Total", f"Total: ₹{total}")

# ---------------- CATEGORY ----------------
def check_other(selected):
    if selected == "Others":
        entry_other.grid(row=1, column=2, padx=5)
    else:
        entry_other.grid_forget()

# ---------------- UI ----------------
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("520x550")
root.configure(bg="#f0f0f0")

# -------- HEADER --------
header = tk.Frame(root, bg="#2e8b57")
header.pack(fill="x")

tk.Label(header, text="Expense Tracker",
         bg="#2e8b57", fg="white",
         font=("Arial", 16, "bold")).pack(pady=5)

tk.Label(header, text="Track every rupee you spend",
         bg="#2e8b57", fg="white",
         font=("Arial", 9)).pack()

# -------- ADD EXPENSE --------
add_frame = tk.LabelFrame(root, text=" Add New Expense ", bg="white", padx=10, pady=10)
add_frame.pack(padx=10, pady=10, fill="x")

# Row 0
tk.Label(add_frame, text="Expense Name:", bg="white").grid(row=0, column=0, sticky="w")
entry_name = tk.Entry(add_frame)
entry_name.grid(row=0, column=1, padx=5)

tk.Label(add_frame, text="Amount (₹):", bg="white").grid(row=0, column=2, sticky="w")
entry_amount = tk.Entry(add_frame)
entry_amount.grid(row=0, column=3, padx=5)

# Row 1
tk.Label(add_frame, text="Category:", bg="white").grid(row=1, column=0, sticky="w")

categories = ["Food", "Travel", "Shopping", "Bills", "Others"]
category_var = tk.StringVar(value="Food")

dropdown = tk.OptionMenu(add_frame, category_var, *categories, command=check_other)
dropdown.grid(row=1, column=1, padx=5, sticky="w")

# "Others" entry (hidden initially)
entry_other = tk.Entry(add_frame)

# Button
tk.Button(add_frame, text="+ Add Expense",
          bg="#2e8b57", fg="white",
          command=add_expense).grid(row=2, column=3, pady=5)

# -------- EXPENSE LIST --------
list_frame = tk.LabelFrame(root, text=" Expense List ", bg="white")
list_frame.pack(padx=10, pady=10, fill="both", expand=True)

listbox = tk.Listbox(list_frame)
listbox.pack(fill="both", expand=True, padx=5, pady=5)

# -------- BUTTONS --------
btn_frame = tk.Frame(root, bg="#f0f0f0")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Delete Selected",
          bg="#d9534f", fg="white",
          command=delete_expense).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Clear All Data",
          bg="#f0ad4e", fg="white",
          command=clear_all).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Total",
          bg="#5bc0de", fg="white",
          command=show_total).grid(row=0, column=2, padx=5)

# -------- LOAD DATA --------
load_from_file()
update_list()

root.mainloop()