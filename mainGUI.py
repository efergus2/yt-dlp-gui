import customtkinter as ctk
from tkinter import filedialog
import subprocess
import threading
import os
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class YTDLP_GUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("yt-dlp Studio")
        self.geometry("900x550")
        self.resizable(False, False)

        # -------- Layout Frames --------
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.main = ctk.CTkFrame(self)
        self.main.pack(side="right", expand=True, fill="both")

        # -------- Sidebar --------
        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="YT-DLP\nSTUDIO",
            font=("Segoe UI Variable", 22, "bold")
        )
        self.logo.pack(pady=(30, 20))

        self.download_btn = ctk.CTkButton(
            self.sidebar,
            text="Download",
            height=40,
            command=self.start_download
        )
        self.download_btn.pack(pady=10, padx=20, fill="x")

        self.update_btn = ctk.CTkButton(
            self.sidebar,
            text="Update yt-dlp",
            height=40,
            fg_color="#2E8BFF",
            command=self.update_ytdlp
        )
        self.update_btn.pack(pady=10, padx=20, fill="x")

        # -------- Main Panel --------
        self.title_label = ctk.CTkLabel(
            self.main,
            text="Download Video or Audio",
            font=("Segoe UI Variable", 26, "bold")
        )
        self.title_label.pack(pady=(30, 20))

        self.url_entry = ctk.CTkEntry(
            self.main,
            width=550,
            height=40,
            placeholder_text="Paste YouTube URL..."
        )
        self.url_entry.pack(pady=10)

        # Format + Folder Row
        row = ctk.CTkFrame(self.main, fg_color="transparent")
        row.pack(pady=10)

        self.format_var = ctk.StringVar(value="best")
        self.format_menu = ctk.CTkOptionMenu(
            row,
            values=["best", "mp4", "mp3", "wav", "m4a"],
            variable=self.format_var,
            width=150,
            height=35
        )
        self.format_menu.pack(side="left", padx=10)

        self.output_path = ctk.StringVar()
        self.folder_entry = ctk.CTkEntry(
            row,
            textvariable=self.output_path,
            width=300,
            height=35,
            placeholder_text="Choose output folder..."
        )
        self.folder_entry.pack(side="left", padx=10)

        self.browse_btn = ctk.CTkButton(
            row,
            text="Browse",
            width=100,
            command=self.choose_folder
        )
        self.browse_btn.pack(side="left", padx=10)

        # Progress Bar
        self.progress = ctk.CTkProgressBar(self.main, width=600)
        self.progress.pack(pady=20)
        self.progress.set(0)

        # Log Output
        self.log_box = ctk.CTkTextbox(self.main, width=650, height=180)
        self.log_box.pack(pady=10)
        self.log("Ready.")

    # -------- Utility --------
    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)

    # -------- Download --------
    def start_download(self):
        threading.Thread(target=self.download).start()

    def download(self):
        url = self.url_entry.get().strip()
        folder = self.output_path.get()
        file_type = self.format_var.get()

        if not url or not folder:
            self.log("⚠ Missing URL or folder.")
            return

        output_template = os.path.join(folder, "%(title)s.%(ext)s")
        command = ["yt-dlp", "-o", output_template]

        if file_type in ["mp3", "wav", "m4a"]:
            command += ["-x", "--audio-format", file_type]
        elif file_type == "mp4":
            command += ["-f", "mp4"]
        else:
            command += ["-f", "bestvideo+bestaudio/best"]

        command.append(url)

        self.progress.set(0)
        self.log("Starting download...")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            self.log(line.strip())

            # Parse percentage
            match = re.search(r"(\d+(\.\d+)?)%", line)
            if match:
                percent = float(match.group(1)) / 100
                self.progress.set(percent)

        process.wait()

        if process.returncode == 0:
            self.progress.set(1)
            self.log("✅ Download complete.")
        else:
            self.log("❌ Download failed.")

    # -------- Update --------
    def update_ytdlp(self):
        self.log("Checking for updates...")
        process = subprocess.Popen(
            ["yt-dlp", "-U"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            self.log(line.strip())

        process.wait()
        self.log("Update finished.")

if __name__ == "__main__":
    app = YTDLP_GUI()
    app.mainloop()