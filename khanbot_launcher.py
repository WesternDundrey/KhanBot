import webbrowser
import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

class KhanBotLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("KhanBot")
        self.root.geometry("300x150")

        # Center the window
        self.center_window()

        # Create and configure the main frame
        self.frame = ttk.Frame(root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Progress bar
        self.progress = ttk.Progressbar(self.frame, length=200, mode='determinate')
        self.progress.grid(row=1, column=0, pady=20)

        # Status label
        self.status_label = ttk.Label(self.frame, text="Starting KhanBot...")
        self.status_label.grid(row=2, column=0)

        # Begin launch sequence
        self.root.after(1000, self.launch_sequence)

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 300) // 2
        y = (screen_height - 150) // 2
        self.root.geometry(f"300x150+{x}+{y}")

    def launch_sequence(self):
        try:
            # Open the website
            self.status_label["text"] = "Opening KhanBot..."
            self.progress["value"] = 50
            webbrowser.open('http://localhost:8501')
            self.progress["value"] = 100

            # Close launcher after successful launch
            self.root.after(2000, self.root.destroy)

        except Exception as e:
            self.status_label["text"] = f"Launch failed: {str(e)}"

def main():
    root = tk.Tk()
    app = KhanBotLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
