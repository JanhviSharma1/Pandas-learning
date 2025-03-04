import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk
import matplotlib.pyplot as plt
from tkcalendar import DateEntry

# Initialize DataFrame
columns = ["Date", "Category", "Amount"]
data = pd.DataFrame(columns=columns)

def add_transaction():
    global data
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    
    try:
        amount = float(amount)
        new_entry = pd.DataFrame([[date, category, amount]], columns=columns)
        data = pd.concat([data, new_entry], ignore_index=True)
        update_display()
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.")

def update_transaction():
    global data
    try:
        index = int(index_entry.get())
        if 0 <= index < len(data):
            data.at[index, "Date"] = date_entry.get()
            data.at[index, "Category"] = category_entry.get()
            data.at[index, "Amount"] = float(amount_entry.get())
            update_display()
        else:
            messagebox.showerror("Invalid Index", "No entry at this index.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid index and amount.")

def delete_transaction():
    global data
    try:
        index = int(index_entry.get())
        if 0 <= index < len(data):
            data = data.drop(index).reset_index(drop=True)
            update_display()
        else:
            messagebox.showerror("Invalid Index", "No entry at this index.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid index.")

def update_display():
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, data.to_string(index=True))

def filter_transactions():
    global data
    filter_text = filter_entry.get().strip().lower()
    if filter_text:
        filtered_data = data[data['Category'].str.lower().str.contains(filter_text, na=False)]
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, filtered_data.to_string(index=True))

def show_expense_chart():
    if data.empty:
        messagebox.showwarning("No Data", "No expenses recorded yet!")
        return
    
    category_totals = data.groupby("Category")["Amount"].sum()
    
    plt.figure(figsize=(6, 4))
    plt.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%', startangle=90)
    plt.title("Expense Distribution")
    plt.show()

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        data.to_csv(file_path, index=False)
        messagebox.showinfo("Export Successful", f"Data exported to {file_path}")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Personal Budget Planner")
root.geometry("880x500")

# Frames
left_frame = tk.Frame(root, padx=10, pady=10)
left_frame.grid(row=0, column=0, sticky="n")

right_frame = tk.Frame(root, padx=10, pady=10)
right_frame.grid(row=0, column=1, sticky="n")

# Left Frame - Adding Entries
tk.Label(left_frame, text="Date:").grid(row=0, column=0, padx=7, pady=5)
date_entry = DateEntry(left_frame)
date_entry.grid(row=0, column=1)

tk.Label(left_frame, text="Category:").grid(row=1, column=0,padx=7, pady=5)
category_entry = tk.Entry(left_frame)
category_entry.grid(row=1, column=1)

tk.Label(left_frame, text="Amount:").grid(row=2, column=0,padx=7, pady=5)
amount_entry = tk.Entry(left_frame)
amount_entry.grid(row=2, column=1)

tk.Label(left_frame, text="Index (for update/delete):").grid(row=3, column=0, padx=7, pady=5)
index_entry = tk.Entry(left_frame)
index_entry.grid(row=3, column=1)

tk.Button(left_frame, text="Add Transaction", command=add_transaction).grid(row=4, column=0, columnspan=2, padx=7, pady=5)
tk.Button(left_frame, text="Update Transaction", command=update_transaction).grid(row=5, column=0, columnspan=2, padx=7, pady=5)
tk.Button(left_frame, text="Delete Transaction", command=delete_transaction).grid(row=6, column=0, columnspan=2, padx=7, pady=5)

tk.Label(left_frame, text="Filter by Category:").grid(row=7, column=0, padx=7, pady=5)
filter_entry = tk.Entry(left_frame)
filter_entry.grid(row=7, column=1)
tk.Button(left_frame, text="Filter", command=filter_transactions).grid(row=8, column=0, columnspan=2, padx=7, pady=5)

tk.Button(left_frame, text="Show Expense Chart", command=show_expense_chart).grid(row=9, column=0, columnspan=2, padx=7, pady=5)
tk.Button(left_frame, text="Export to CSV", command=export_to_csv).grid(row=10, column=0, columnspan=2, padx=7, pady=5)

# Right Frame - Display Data
text_widget = scrolledtext.ScrolledText(right_frame, width=80, height=40)
text_widget.grid(row=0, column=0)

root.mainloop()
