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
    def __init__(self, port=19999):  # Change is here - port parameter in init
        self.port = port  # Set the port attribute first
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
        self.root.geometry("400x300")
        self.instance_checker = SingleInstanceChecker()
        
        if self.instance_checker.is_running():
            messagebox.showwarning("KhanBot Already Running", 
                "An instance of KhanBot is already running.\nPlease close it before starting a new one.")
            self.cleanup_existing_processes()
            sys.exit()

        self.setup_ui()
        self.processes = []
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.after(1000, self.check_dependencies)

    def setup_ui(self):
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.progress = ttk.Progressbar(self.frame, length=300, mode='determinate')
        self.progress.grid(row=1, column=0, pady=20)
        
        self.status_label = ttk.Label(self.frame, text="Checking dependencies...")
        self.status_label.grid(row=2, column=0)
        
        self.detail_label = ttk.Label(self.frame, text="", wraplength=350)
        self.detail_label.grid(row=3, column=0, pady=10)

    def check_dependencies(self):
        try:
            self.status_label["text"] = "Checking conda environment..."
            self.progress["value"] = 10
            
            # Check if required packages are installed
            self.detail_label["text"] = "Checking required packages..."
            
            # Use current Python environment since we're already in the conda env
            try:
                import streamlit
                import fastapi
                import uvicorn
                self.detail_label["text"] = "Required packages found"
            except ImportError as e:
                self.detail_label["text"] = f"Installing missing package: {str(e)}"
                subprocess.run(['pip', 'install', 'streamlit', 'fastapi', 'uvicorn'], check=True)
            
            self.progress["value"] = 50
            self.start_services()
            
        except Exception as e:
            self.handle_error("Dependency check failed", e)

    def start_services(self):
        try:
            # Start backend
            self.status_label["text"] = "Starting Backend Service..."
            self.progress["value"] = 70
            
            backend_process = subprocess.Popen(
                ['bash', 'launch_backend.sh'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes.append(backend_process)
            
            # Wait for backend to initialize
            time.sleep(3)
            
            # Start dashboard
            self.status_label["text"] = "Starting Dashboard Service..."
            self.progress["value"] = 90
            
            dashboard_process = subprocess.Popen(
                ['bash', 'launch_dashboard.sh'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes.append(dashboard_process)
            
            # Wait for dashboard to initialize
            time.sleep(3)
            
            # Open browser
            self.launch_browser()
            
        except Exception as e:
            self.handle_error("Failed to start services", e)

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
                if proc.name() in ['python', 'Python'] and \
                   any(x in str(proc.cmdline()) for x in ['backend-api', 'streamlit']):
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