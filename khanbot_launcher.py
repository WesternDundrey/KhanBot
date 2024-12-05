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
        self.root.geometry("400x200")
        self.instance_checker = SingleInstanceChecker()
        
        if self.instance_checker.is_running():
            messagebox.showwarning("KhanBot Already Running", 
                "An instance of KhanBot is already running.\nPlease close it before starting a new one.")
            self.cleanup_existing_processes()
            sys.exit()

        self.setup_ui()
        self.processes = []
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.after(1000, self.safe_start_services)

    def setup_ui(self):
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.progress = ttk.Progressbar(self.frame, length=300, mode='determinate')
        self.progress.grid(row=1, column=0, pady=20)
        
        self.status_label = ttk.Label(self.frame, text="Starting KhanBot...")
        self.status_label.grid(row=2, column=0)

    def safe_start_services(self):
        try:
            self.status_label["text"] = "Checking WSL..."
            self.progress["value"] = 20
            
            # Check WSL
            wsl_check = subprocess.run(['wsl', '--status'], capture_output=True)
            if wsl_check.returncode != 0:
                raise Exception("WSL is not properly installed")

            self.status_label["text"] = "Starting Backend Service..."
            self.progress["value"] = 40
            
            # Start backend in WSL
            backend_process = subprocess.Popen(
                ['wsl', '-e', 'bash', '-ic', './wsl_backend.sh'],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes.append(backend_process)
            
            # Wait for backend to initialize
            time.sleep(5)
            
            self.status_label["text"] = "Starting Dashboard Service..."
            self.progress["value"] = 60
            
            # Start dashboard in WSL
            dashboard_process = subprocess.Popen(
                ['wsl', '-e', 'bash', '-ic', './wsl_dashboard.sh'],
                cwd=os.path.dirname(os.path.abspath(__file__)),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes.append(dashboard_process)
            
            self.progress["value"] = 80
            self.launch_browser()
            
        except Exception as e:
            self.handle_error("Failed to start services", e)

    def launch_browser(self):
        try:
            self.status_label["text"] = "Opening KhanBot..."
            self.progress["value"] = 100
            webbrowser.open('http://localhost:8501')
            self.status_label["text"] = "KhanBot is running..."
        except Exception as e:
            self.handle_error("Failed to open dashboard", e)

    def cleanup_existing_processes(self):
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if ('python' in proc.name().lower() or 'wsl' in proc.name().lower()) and \
                   any(x in str(proc.cmdline()) for x in ['backend-api', 'streamlit', 'wsl_backend.sh', 'wsl_dashboard.sh']):
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def handle_error(self, message, error):
        messagebox.showerror("Error", f"{message}:\n{str(error)}")
        self.on_closing()

    def on_closing(self):
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        
        self.instance_checker.cleanup()
        self.root.destroy()

def main():
    root = tk.Tk()
    KhanBotLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()