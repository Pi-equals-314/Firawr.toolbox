import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import os
import shutil

# ------------------ MAIN WINDOW ------------------ #
root = tk.Tk()
root.title("Python Multi-Tool App")
root.geometry("500x400")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ------------------ CALCULATOR TAB ------------------ #
calc_frame = ttk.Frame(notebook)
notebook.add(calc_frame, text="Calculator")

calc_entry = tk.Entry(calc_frame, font=("Arial", 16))
calc_entry.pack(pady=20)

def calculate():
    try:
        result = eval(calc_entry.get())
        calc_entry.delete(0, tk.END)
        calc_entry.insert(0, str(result))
    except:
        messagebox.showerror("Error", "Invalid Expression")

tk.Button(calc_frame, text="Calculate", command=calculate).pack()

# ------------------ PASSWORD GENERATOR TAB ------------------ #
pass_frame = ttk.Frame(notebook)
notebook.add(pass_frame, text="Password Generator")

tk.Label(pass_frame, text="Password Length:").pack(pady=10)
length_entry = tk.Entry(pass_frame)
length_entry.pack()

def generate_password():
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%"
    try:
        length = int(length_entry.get())
        password = ''.join(random.choice(chars) for _ in range(length))
        result_label.config(text=password)
    except:
        messagebox.showerror("Error", "Enter a valid number")

tk.Button(pass_frame, text="Generate", command=generate_password).pack(pady=10)
result_label = tk.Label(pass_frame, text="", font=("Arial", 12))
result_label.pack()

# ------------------ FILE ORGANIZER TAB ------------------ #
file_frame = ttk.Frame(notebook)
notebook.add(file_frame, text="File Organizer")

def organize_files():
    path = filedialog.askdirectory()
    if not path:
        return

    try:
        for file in os.listdir(path):
            full_path = os.path.join(path, file)

            if os.path.isfile(full_path):
                ext = file.split('.')[-1]
                folder = os.path.join(path, ext)

                if not os.path.exists(folder):
                    os.mkdir(folder)

                shutil.move(full_path, os.path.join(folder, file))

        messagebox.showinfo("Success", "Files Organized!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

tk.Button(file_frame, text="Select Folder & Organize", command=organize_files).pack(pady=50)

# ------------------ RUN APP ------------------ #
root.mainloop()