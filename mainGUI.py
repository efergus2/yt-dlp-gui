import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os

def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_path.set(folder)

def download():
    url = url_entry.get().strip()
    folder = output_path.get()
    file_type = format_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    if not folder:
        messagebox.showerror("Error", "Please choose an output folder.")
        return

    output_template = os.path.join(folder, "%(title)s.%(ext)s")

    command = ["yt-dlp", "-o", output_template]

    if file_type == "mp3":
        command += ["-x", "--audio-format", "mp3"]
    elif file_type == "wav":
        command += ["-x", "--audio-format", "wav"]
    elif file_type == "m4a":
        command += ["-x", "--audio-format", "m4a"]
    elif file_type == "mp4":
        command += ["-f", "mp4"]
    elif file_type == "best":
        command += ["-f", "bestvideo+bestaudio/best"]

    command.append(url)

    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "Download completed!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Download failed. Check console.")

# GUI Setup
root = tk.Tk()
root.title("yt-dlp GUI")
root.geometry("500x250")

# URL
tk.Label(root, text="Video URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack()

# Format Dropdown
tk.Label(root, text="Choose Format:").pack(pady=5)
format_var = tk.StringVar(value="best")
format_dropdown = ttk.Combobox(
    root,
    textvariable=format_var,
    values=["best", "mp4", "mp3", "wav", "m4a"],
    state="readonly"
)
format_dropdown.pack()

# Output Folder
output_path = tk.StringVar()
tk.Label(root, text="Output Folder:").pack(pady=5)
tk.Entry(root, textvariable=output_path, width=50).pack()
tk.Button(root, text="Browse", command=choose_folder).pack(pady=5)

# Download Button
tk.Button(root, text="Download", command=download, bg="green", fg="white").pack(pady=15)

root.mainloop()