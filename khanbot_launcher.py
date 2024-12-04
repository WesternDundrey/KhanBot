import subprocess
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
from pathlib import Path
import socket
import psutil
import time

class SingleInstanceChecker:
    def __init__(self, port=12345):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def is_running(self):
        try:
            self.sock.bind(('localhost', self.port))
            return False
        except socket.error:
            return True

    def cleanup(self):
        try:
            self.sock.close()
        except:
            pass

class KhanBotLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("KhanBot")
        self.root.geometry("400x250")
        self.instance_checker = SingleInstanceChecker()

        if self.instance_checker.is_running():
            messagebox.showwarning("KhanBot Already Running",
                "An instance of KhanBot is already running.\nPlease close it before starting a new one.")
            self.cleanup_existing_processes()
            sys.exit()

        self.setup_ui()
        self.processes = []
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.after(1000, self.check_wsl_and_start)

    def setup_ui(self):
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.progress = ttk.Progressbar(self.frame, length=300, mode='determinate')
        self.progress.grid(row=1, column=0, pady=20)

        self.status_label = ttk.Label(self.frame, text="Initializing KhanBot...")
        self.status_label.grid(row=2, column=0)

        self.detail_label = ttk.Label(self.frame, text="", wraplength=350)
        self.detail_label.grid(row=3, column=0, pady=10)

    def check_wsl_and_start(self):
        try:
            self.status_label["text"] = "Checking WSL Environment..."
            self.progress["value"] = 10

            # Check if WSL is installed and running
            result = subprocess.run(['wsl', '--status'],
                                 capture_output=True,
                                 text=True)

            if result.returncode != 0:
                self.detail_label["text"] = "WSL not found. Running setup script..."
                self.run_setup_script()
            else:
                self.start_services()

        except Exception as e:
            self.handle_error("Failed to check WSL status", e)

    def run_setup_script(self):
        try:
            self.status_label["text"] = "Running Setup Script..."
            self.progress["value"] = 20

            setup_process = subprocess.Popen(
                ['setup_khanbot.bat'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            self.detail_label["text"] = "Setting up WSL environment... This may take a few minutes."
            setup_process.wait()

            if setup_process.returncode == 0:
                self.start_services()
            else:
                raise Exception("Setup script failed")

        except Exception as e:
            self.handle_error("Failed to run setup script", e)

    def start_services(self):
        try:
            self.status_label["text"] = "Starting Backend Service..."
            self.progress["value"] = 40

            # Start backend in WSL
            backend_process = subprocess.Popen(
                ['wsl', 'bash', '-ic', 'cd backend-api && python3 main.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.processes.append(backend_process)

            # Wait for backend to initialize
            time.sleep(5)

            self.start_dashboard_service()

        except Exception as e:
            self.handle_error("Failed to start backend service", e)

    def start_dashboard_service(self):
        try:
            self.status_label["text"] = "Starting Dashboard Service..."
            self.progress["value"] = 70

            # Start dashboard in WSL
            dashboard_process = subprocess.Popen(
                ['wsl', 'bash', '-ic', 'cd dashboard && streamlit run main.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            self.processes.append(dashboard_process)

            self.root.after(3000, self.launch_browser)

        except Exception as e:
            self.handle_error("Failed to start dashboard service", e)

    def launch_browser(self):
        try:
            self.status_label["text"] = "Opening KhanBot..."
            self.progress["value"] = 100
            webbrowser.open('http://localhost:8501')
            self.status_label["text"] = "KhanBot is running"
            self.detail_label["text"] = "Access the dashboard at http://localhost:8501"
        except Exception as e:
            self.handle_error("Failed to open dashboard", e)

    def cleanup_existing_processes(self):
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if ('python' in proc.name().lower() and
                    any(x in str(proc.cmdline()) for x in ['backend-api', 'streamlit'])):
                    proc.terminate()

                # Also cleanup WSL processes
                subprocess.run(['wsl', '--terminate', 'Ubuntu'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def handle_error(self, message, error):
        messagebox.showerror("Error", f"{message}:\n{str(error)}")
        self.on_closing()

    def on_closing(self):
        self.cleanup_existing_processes()
        self.instance_checker.cleanup()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = KhanBotLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
