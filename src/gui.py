import math
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from crypto_utils import encrypt_file, decrypt_file


selected_file = ""


def choose_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_path_var.set(file_path)
        log_message(f"Selected file: {file_path}")


def toggle_password(entry, button):
    if entry.cget("show") == "*":
        entry.config(show="")
        button.config(text="Hide")
    else:
        entry.config(show="*")
        button.config(text="Show")


def log_message(message):
    activity_log.insert(tk.END, message + "\n")
    activity_log.see(tk.END)


def style_button(button, normal_color, hover_color):
    button.config(
        bg=normal_color,
        fg="white",
        activebackground=hover_color,
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 10, "bold"),
    )

    button.bind("<Enter>", lambda event: button.config(bg=hover_color))
    button.bind("<Leave>", lambda event: button.config(bg=normal_color))
    button.bind("<ButtonPress>", lambda event: button.config(relief="sunken"))
    button.bind("<ButtonRelease>", lambda event: button.config(relief="flat"))


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
            progress_bar.start(10)
            log_message("Encryption started...")
            encrypt_file(input_file, output_file, access_password, encryption_password)
            file_path_var.set(output_file)
            log_message(f"Encrypted successfully: {output_file}")
            messagebox.showinfo("Success", "File encrypted successfully.")
        except Exception as error:
            log_message(f"Error: {error}")
            messagebox.showerror("Error", str(error))
        finally:
            progress_bar.stop()

    threading.Thread(target=task, daemon=True).start()


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

    output_file = input_file[:-4] if input_file.endswith(".enc") else input_file + ".decrypted"

    def task():
        try:
            progress_bar.start(10)
            log_message("Decryption started...")
            decrypt_file(input_file, output_file, access_password, encryption_password)
            file_path_var.set(output_file)
            log_message(f"Decrypted successfully: {output_file}")
            messagebox.showinfo("Success", "File decrypted successfully.")
        except Exception as error:
            log_message(f"Error: {error}")
            messagebox.showerror("Error", str(error))
        finally:
            progress_bar.stop()

    threading.Thread(target=task, daemon=True).start()


def animate_background():
    canvas.delete("circle")

    width = 850
    height = 620

    for i in range(8):
        x = 100 + i * 110
        y = 120 + math.sin(animation_counter[0] / 20 + i) * 45
        size = 45 + math.sin(animation_counter[0] / 15 + i) * 12

        canvas.create_oval(
            x,
            y,
            x + size,
            y + size,
            fill="#1f2a44",
            outline="",
            tags="circle",
        )

    animation_counter[0] += 1
    root.after(40, animate_background)


root = tk.Tk()
root.title("File Encryption Tool")
root.geometry("850x620")
root.resizable(False, False)

canvas = tk.Canvas(root, width=850, height=620, bg="#0f172a", highlightthickness=0)
canvas.place(x=0, y=0)

animation_counter = [0]

main_frame = tk.Frame(root, bg="#111827")
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=720, height=540)

file_path_var = tk.StringVar()
access_password_var = tk.StringVar()
encryption_password_var = tk.StringVar()

title = tk.Label(
    main_frame,
    text="Secure File Encryption Tool",
    font=("Segoe UI", 22, "bold"),
    fg="#ffffff",
    bg="#111827",
)
title.pack(pady=18)

subtitle = tk.Label(
    main_frame,
    text="Encrypt and decrypt files with dual password protection",
    font=("Segoe UI", 10),
    fg="#9ca3af",
    bg="#111827",
)
subtitle.pack(pady=2)

file_frame = tk.Frame(main_frame, bg="#111827")
file_frame.pack(pady=18)

file_entry = tk.Entry(
    file_frame,
    textvariable=file_path_var,
    width=55,
    font=("Segoe UI", 10),
    bg="#1f2937",
    fg="white",
    insertbackground="white",
    relief="flat",
)
file_entry.pack(side=tk.LEFT, ipady=8, padx=5)

browse_button = tk.Button(file_frame, text="Browse", command=choose_file, width=12)
browse_button.pack(side=tk.LEFT, ipady=5)
style_button(browse_button, "#2563eb", "#1d4ed8")

access_frame = tk.Frame(main_frame, bg="#111827")
access_frame.pack(pady=8)

access_label = tk.Label(
    access_frame,
    text="Access Password",
    fg="#e5e7eb",
    bg="#111827",
    width=18,
    anchor="w",
)
access_label.pack(side=tk.LEFT)

access_entry = tk.Entry(
    access_frame,
    textvariable=access_password_var,
    show="*",
    width=35,
    bg="#1f2937",
    fg="white",
    insertbackground="white",
    relief="flat",
)
access_entry.pack(side=tk.LEFT, ipady=7, padx=5)

show_access_button = tk.Button(
    access_frame,
    text="Show",
    width=8,
    command=lambda: toggle_password(access_entry, show_access_button),
)
show_access_button.pack(side=tk.LEFT, ipady=4)
style_button(show_access_button, "#374151", "#4b5563")

encryption_frame = tk.Frame(main_frame, bg="#111827")
encryption_frame.pack(pady=8)

encryption_label = tk.Label(
    encryption_frame,
    text="Encryption Password",
    fg="#e5e7eb",
    bg="#111827",
    width=18,
    anchor="w",
)
encryption_label.pack(side=tk.LEFT)

encryption_entry = tk.Entry(
    encryption_frame,
    textvariable=encryption_password_var,
    show="*",
    width=35,
    bg="#1f2937",
    fg="white",
    insertbackground="white",
    relief="flat",
)
encryption_entry.pack(side=tk.LEFT, ipady=7, padx=5)

show_encryption_button = tk.Button(
    encryption_frame,
    text="Show",
    width=8,
    command=lambda: toggle_password(encryption_entry, show_encryption_button),
)
show_encryption_button.pack(side=tk.LEFT, ipady=4)
style_button(show_encryption_button, "#374151", "#4b5563")

button_frame = tk.Frame(main_frame, bg="#111827")
button_frame.pack(pady=20)

encrypt_button = tk.Button(
    button_frame,
    text="Encrypt File",
    command=run_encrypt,
    width=18,
    height=2,
)
encrypt_button.pack(side=tk.LEFT, padx=12)
style_button(encrypt_button, "#16a34a", "#15803d")

decrypt_button = tk.Button(
    button_frame,
    text="Decrypt File",
    command=run_decrypt,
    width=18,
    height=2,
)
decrypt_button.pack(side=tk.LEFT, padx=12)
style_button(decrypt_button, "#dc2626", "#b91c1c")

progress_bar = ttk.Progressbar(main_frame, mode="indeterminate", length=520)
progress_bar.pack(pady=8)

log_label = tk.Label(
    main_frame,
    text="Activity Log",
    fg="#ffffff",
    bg="#111827",
    font=("Segoe UI", 11, "bold"),
)
log_label.pack(pady=5)

activity_log = tk.Text(
    main_frame,
    height=7,
    width=78,
    bg="#030712",
    fg="#d1d5db",
    insertbackground="white",
    relief="flat",
)
activity_log.pack(pady=8)

animate_background()
root.mainloop()
