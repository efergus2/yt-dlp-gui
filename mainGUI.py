import customtkinter as ctk
from tkinter import filedialog
import subprocess
import threading
import os
import re
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class YTDLP_GUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("yt-dlp Studio")
        self.geometry("950x600")
        self.resizable(False, False)

        self.font_title = ("Segoe UI Variable", 28, "bold")
        self.font_body = ("Segoe UI Variable", 14)
        self.font_small = ("Segoe UI Variable", 12)

        # ================= SIDEBAR =================
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#111111")
        self.sidebar.pack(side="left", fill="y")

        self.logo = ctk.CTkLabel(
            self.sidebar,
            text="YT-DLP\nSTUDIO",
            font=("Segoe UI Variable", 24, "bold"),
            text_color="#4da6ff"
        )
        self.logo.pack(pady=(40, 30))

        self.download_btn = ctk.CTkButton(
            self.sidebar,
            text="Download",
            height=45,
            corner_radius=12,
            command=self.start_download
        )
        self.download_btn.pack(pady=10, padx=25, fill="x")

        self.update_btn = ctk.CTkButton(
            self.sidebar,
            text="Update yt-dlp",
            height=45,
            corner_radius=12,
            fg_color="#1f6aa5",
            hover_color="#155a8a",
            command=self.update_ytdlp
        )
        self.update_btn.pack(pady=10, padx=25, fill="x")

        self.clear_btn = ctk.CTkButton(
            self.sidebar,
            text="Clear Log",
            height=45,
            corner_radius=12,
            fg_color="#333333",
            hover_color="#444444",
            command=self.clear_log
        )
        self.clear_btn.pack(pady=10, padx=25, fill="x")

        # ================= MAIN AREA =================
        self.main = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.main.pack(side="right", expand=True, fill="both")

        self.title_label = ctk.CTkLabel(
            self.main,
            text="Download Video or Audio",
            font=self.font_title
        )
        self.title_label.pack(pady=(40, 20))

        # URL
        self.url_entry = ctk.CTkEntry(
            self.main,
            width=650,
            height=45,
            corner_radius=12,
            font=self.font_body,
            placeholder_text="Paste YouTube URL..."
        )
        self.url_entry.pack(pady=15)

        # Options Card
        self.options_card = ctk.CTkFrame(self.main, corner_radius=18, fg_color="#202020")
        self.options_card.pack(pady=15, padx=40, fill="x")

        row = ctk.CTkFrame(self.options_card, fg_color="transparent")
        row.pack(pady=20)

        self.format_var = ctk.StringVar(value="best")

        self.format_menu = ctk.CTkOptionMenu(
            row,
            values=["best", "mp4", "mp3", "wav", "m4a"],
            variable=self.format_var,
            width=150,
            height=40,
            corner_radius=10
        )
        self.format_menu.pack(side="left", padx=15)

        self.output_path = ctk.StringVar()

        self.folder_entry = ctk.CTkEntry(
            row,
            textvariable=self.output_path,
            width=350,
            height=40,
            corner_radius=10,
            placeholder_text="Select output folder..."
        )
        self.folder_entry.pack(side="left", padx=15)

        self.browse_btn = ctk.CTkButton(
            row,
            text="Browse",
            width=110,
            height=40,
            corner_radius=10,
            command=self.choose_folder
        )
        self.browse_btn.pack(side="left", padx=15)

        # Progress
        self.progress = ctk.CTkProgressBar(
            self.main,
            width=700,
            height=18,
            corner_radius=10
        )
        self.progress.pack(pady=25)
        self.progress.set(0)

        # Log Area
        self.log_box = ctk.CTkTextbox(
            self.main,
            width=750,
            height=200,
            corner_radius=12,
            font=self.font_small
        )
        self.log_box.pack(pady=10)

        self.log("Ready.")

    # ================= FUNCTIONS =================

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")

    def clear_log(self):
        self.log_box.delete("1.0", "end")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)

    def disable_buttons(self):
        self.download_btn.configure(state="disabled")
        self.update_btn.configure(state="disabled")

    def enable_buttons(self):
        self.download_btn.configure(state="normal")
        self.update_btn.configure(state="normal")

    def start_download(self):
        threading.Thread(target=self.download).start()

    def download(self):
        url = self.url_entry.get().strip()
        folder = self.output_path.get()
        file_type = self.format_var.get()

        if not url or not folder:
            self.log("⚠ Missing URL or output folder.")
            return

        self.disable_buttons()
        self.progress.set(0)

        output_template = os.path.join(folder, "%(title)s.%(ext)s")
        command = ["yt-dlp", "-o", output_template]

        if file_type in ["mp3", "wav", "m4a"]:
            command += ["-x", "--audio-format", file_type]
        elif file_type == "mp4":
            command += ["-f", "mp4"]
        else:
            command += ["-f", "bestvideo+bestaudio/best"]

        command.append(url)

        self.log("Starting download...")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            self.log(line.strip())
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

        self.enable_buttons()

    def update_ytdlp(self):
        self.disable_buttons()
        self.log("Checking for updates...")

        process = subprocess.Popen(
            [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            self.log(line.strip())

        process.wait()
        self.log("Update finished.")
        self.enable_buttons()


if __name__ == "__main__":
    app = YTDLP_GUI()
    app.mainloop()