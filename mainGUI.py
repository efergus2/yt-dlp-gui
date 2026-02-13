import customtkinter as ctk
from tkinter import filedialog
import subprocess
import threading
import os
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class YTDLP_GUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("yt-dlp Pro GUI")
        self.geometry("720x500")
        self.resizable(False, False)

        # Title
        self.title_label = ctk.CTkLabel(self, text="yt-dlp Downloader", font=("Segoe UI", 24, "bold"))
        self.title_label.pack(pady=15)

        # URL Entry
        self.url_entry = ctk.CTkEntry(self, width=600, placeholder_text="Paste YouTube URL here...")
        self.url_entry.pack(pady=10)

        # Format Selection
        self.format_var = ctk.StringVar(value="best")
        self.format_menu = ctk.CTkOptionMenu(
            self,
            values=["best", "mp4", "mp3", "wav", "m4a"],
            variable=self.format_var
        )
        self.format_menu.pack(pady=10)

        # Folder Selection
        self.output_path = ctk.StringVar()

        folder_frame = ctk.CTkFrame(self)
        folder_frame.pack(pady=10)

        self.folder_entry = ctk.CTkEntry(folder_frame, textvariable=self.output_path, width=500)
        self.folder_entry.pack(side="left", padx=5)

        self.browse_button = ctk.CTkButton(folder_frame, text="Browse", command=self.choose_folder)
        self.browse_button.pack(side="left", padx=5)

        # Buttons Frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=15)

        self.download_button = ctk.CTkButton(button_frame, text="Download", command=self.start_download)
        self.download_button.pack(side="left", padx=10)

        self.update_button = ctk.CTkButton(button_frame, text="Update yt-dlp", command=self.update_ytdlp)
        self.update_button.pack(side="left", padx=10)

        # Log Box
        self.log_box = ctk.CTkTextbox(self, width=650, height=150)
        self.log_box.pack(pady=10)
        self.log("Ready.")

    def log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)

    def start_download(self):
        thread = threading.Thread(target=self.download)
        thread.start()

    def download(self):
        url = self.url_entry.get().strip()
        folder = self.output_path.get()
        file_type = self.format_var.get()

        if not url:
            self.log("⚠ Please enter a URL.")
            return

        if not folder:
            self.log("⚠ Please select output folder.")
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

        self.log("Starting download...")
        self.log(" ".join(command))

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            self.log(line.strip())

        process.wait()

        if process.returncode == 0:
            self.log("✅ Download completed.")
        else:
            self.log("❌ Download failed.")

    def update_ytdlp(self):
        self.log("Checking for updates...")

        try:
            process = subprocess.Popen(
                ["yt-dlp", "-U"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            for line in process.stdout:
                self.log(line.strip())

            process.wait()

            if process.returncode == 0:
                self.log("✅ yt-dlp updated successfully.")
            else:
                self.log("❌ Update failed.")

        except Exception as e:
            self.log(f"Error: {e}")


if __name__ == "__main__":
    app = YTDLP_GUI()
    app.mainloop()