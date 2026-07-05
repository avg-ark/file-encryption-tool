import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from crypto_utils import encrypt_file, decrypt_file


selected_file = ""


def choose_file():
    global selected_file
    selected_file = filedialog.askopenfilename()
    file_path_var.set(selected_file)


def toggle_access_password():
    if access_entry.cget("show") == "*":
        access_entry.config(show="")
        show_access_button.config(text="Hide")
    else:
        access_entry.config(show="*")
        show_access_button.config(text="Show")


def toggle_encryption_password():
    if encryption_entry.cget("show") == "*":
        encryption_entry.config(show="")
        show_encryption_button.config(text="Hide")
    else:
        encryption_entry.config(show="*")
        show_encryption_button.config(text="Show")


def log_message(message):
    activity_log.insert(tk.END, message + "\n")
    activity_log.see(tk.END)


def run_encrypt():
    input_file = file_path_var.get()
    access_password = access_password_var.get()
    encryption_password = encryption_password_var.get()

    if not input_file:
        messagebox.showerror("Error", "Please select a file.")
        return

    if not access_password or not encryption_password:
        messagebox.showerror("Error", "Both passwords are required.")
        return

    output_file = input_file + ".enc"

    def task():
        try:
            progress_bar.start()
            encrypt_file(input_file, output_file, access_password, encryption_password)
            log_message(f"Encrypted successfully: {output_file}")
            file_path_var.set(output_file)
            messagebox.showinfo("Success", "File encrypted successfully.")
        except Exception as error:
            messagebox.showerror("Error", str(error))
        finally:
            progress_bar.stop()

    threading.Thread(target=task).start()


def run_decrypt():
    input_file = file_path_var.get()
    access_password = access_password_var.get()
    encryption_password = encryption_password_var.get()

    if not input_file:
        messagebox.showerror("Error", "Please select a file.")
        return

    if not access_password or not encryption_password:
        messagebox.showerror("Error", "Both passwords are required.")
        return

    if input_file.endswith(".enc"):
        output_file = input_file[:-4]
    else:
        output_file = input_file + ".decrypted"

    def task():
        try:
            progress_bar.start()
            decrypt_file(input_file, output_file, access_password, encryption_password)
            log_message(f"Decrypted successfully: {output_file}")
            file_path_var.set(output_file)
            messagebox.showinfo("Success", "File decrypted successfully.")
        except Exception as error:
            messagebox.showerror("Error", str(error))
        finally:
            progress_bar.stop()

    threading.Thread(target=task).start()


root = tk.Tk()
root.title("File Encryption Tool")
root.geometry("700x520")
root.configure(bg="#121212")

file_path_var = tk.StringVar()
access_password_var = tk.StringVar()
encryption_password_var = tk.StringVar()

title = tk.Label(
    root,
    text="File Encryption Tool",
    font=("Arial", 22, "bold"),
    fg="white",
    bg="#121212"
)
title.pack(pady=20)

file_frame = tk.Frame(root, bg="#121212")
file_frame.pack(pady=10)

file_entry = tk.Entry(
    file_frame,
    textvariable=file_path_var,
    width=55,
    font=("Arial", 11)
)
file_entry.pack(side=tk.LEFT, padx=5)

browse_button = tk.Button(
    file_frame,
    text="Browse",
    command=choose_file,
    width=12
)
browse_button.pack(side=tk.LEFT)

access_frame = tk.Frame(root, bg="#121212")
access_frame.pack(pady=10)

access_label = tk.Label(
    access_frame,
    text="Access Password:",
    fg="white",
    bg="#121212",
    width=18,
    anchor="w"
)
access_label.pack(side=tk.LEFT)

access_entry = tk.Entry(
    access_frame,
    textvariable=access_password_var,
    show="*",
    width=35
)
access_entry.pack(side=tk.LEFT, padx=5)

show_access_button = tk.Button(
    access_frame,
    text="Show",
    command=toggle_access_password,
    width=8
)
show_access_button.pack(side=tk.LEFT)

encryption_frame = tk.Frame(root, bg="#121212")
encryption_frame.pack(pady=10)

encryption_label = tk.Label(
    encryption_frame,
    text="Encryption Password:",
    fg="white",
    bg="#121212",
    width=18,
    anchor="w"
)
encryption_label.pack(side=tk.LEFT)

encryption_entry = tk.Entry(
    encryption_frame,
    textvariable=encryption_password_var,
    show="*",
    width=35
)
encryption_entry.pack(side=tk.LEFT, padx=5)

show_encryption_button = tk.Button(
    encryption_frame,
    text="Show",
    command=toggle_encryption_password,
    width=8
)
show_encryption_button.pack(side=tk.LEFT)

button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=20)

encrypt_button = tk.Button(
    button_frame,
    text="Encrypt File",
    command=run_encrypt,
    width=18,
    height=2
)
encrypt_button.pack(side=tk.LEFT, padx=10)

decrypt_button = tk.Button(
    button_frame,
    text="Decrypt File",
    command=run_decrypt,
    width=18,
    height=2
)
decrypt_button.pack(side=tk.LEFT, padx=10)

progress_bar = ttk.Progressbar(
    root,
    mode="indeterminate",
    length=500
)
progress_bar.pack(pady=10)

log_label = tk.Label(
    root,
    text="Activity Log",
    fg="white",
    bg="#121212",
    font=("Arial", 12, "bold")
)
log_label.pack(pady=5)

activity_log = tk.Text(
    root,
    height=8,
    width=75,
    bg="#1e1e1e",
    fg="white"
)
activity_log.pack(pady=10)

root.mainloop()