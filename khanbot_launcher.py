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
from importlib.metadata import distributions

class SingleInstanceChecker:
    def __init__(self, port=19999):
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

    def update_status(self, status, progress, detail=""):
        self.status_label["text"] = status
        self.progress["value"] = progress
        if detail:
            self.detail_label["text"] = detail
        self.root.update()

    def get_required_packages(self):
        packages = set()
        
        # Read backend requirements
        try:
            with open('backend-api/requirements.txt', 'r') as f:
                packages.update(line.strip() for line in f if line.strip() and not line.startswith('#'))
        except FileNotFoundError:
            pass

        # Read dashboard requirements
        try:
            with open('dashboard/requirements.txt', 'r') as f:
                packages.update(line.strip() for line in f if line.strip() and not line.startswith('#'))
        except FileNotFoundError:
            pass
            
        # Add essential packages
        essential_packages = ['streamlit', 'fastapi', 'uvicorn', 'python-dotenv']
        packages.update(essential_packages)
        
        return packages

    def check_dependencies(self):
        try:
            self.update_status("Installing required packages...", 10)
            
            # Install packages directly
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
                                'streamlit', 'fastapi', 'uvicorn', 'python-dotenv'])
            
            self.update_status("Checking additional dependencies...", 30)
            
            # Get required packages
            required_packages = self.get_required_packages()
            
            # Check installed packages
            installed_packages = {dist.metadata['Name'] for dist in distributions()}
            
            # Find missing packages
            missing_packages = [pkg for pkg in required_packages if pkg.split('==')[0] not in installed_packages]
            
            if missing_packages:
                self.update_status("Installing missing packages...", 50, 
                                 f"Installing: {', '.join(missing_packages)}")
                
                # Install missing packages
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
                except subprocess.CalledProcessError as e:
                    raise Exception(f"Failed to install packages: {str(e)}")
            
            self.update_status("All dependencies installed", 70, "Starting services...")
            self.root.after(1000, self.start_services)
            
        except Exception as e:
            self.handle_error("Dependency check failed", e)

    def start_services(self):
        try:
            # Start backend
            self.update_status("Starting Backend Service...", 80)
            
            backend_process = subprocess.Popen(
                ['bash', 'launch_backend.sh'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes.append(backend_process)
            
            # Wait for backend to initialize
            time.sleep(3)
            
            # Start dashboard
            self.update_status("Starting Dashboard Service...", 90)
            
            dashboard_process = subprocess.Popen(
                ['bash', 'launch_dashboard.sh'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.processes.append(dashboard_process)
            
            # Open browser
            self.root.after(3000, self.launch_browser)
            
        except Exception as e:
            self.handle_error("Failed to start services", e)

    def launch_browser(self):
        try:
            self.update_status("Opening KhanBot...", 100)
            webbrowser.open('http://localhost:8501')
            self.update_status("KhanBot is running", 100, 
                             "Access the dashboard at http://localhost:8501")
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