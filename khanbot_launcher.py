import os
import sys
import time
import subprocess
import socket
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import threading
import signal
from pathlib import Path

class KhanBotLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KhanBot")
        self.root.geometry("400x300")
        
        # Store process handlers
        self.backend_process = None
        self.dashboard_process = None
        
        # Configure main window
        self.setup_ui()
        
        # Set up cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_ui(self):
        """Initialize the user interface components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress bar and status label
        self.progress = ttk.Progressbar(main_frame, length=300, mode='determinate')
        self.progress.grid(row=1, column=0, pady=10)
        
        self.status_label = ttk.Label(main_frame, text="Initializing...")
        self.status_label.grid(row=2, column=0, pady=5)
        
        # Start button
        self.start_button = ttk.Button(main_frame, text="Launch KhanBot", command=self.start_services)
        self.start_button.grid(row=3, column=0, pady=20)
        
    def check_port_in_use(self, port):
        """Check if a port is already in use"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
            
    def install_dependencies(self):
        """Install required packages using both pip and conda"""
        try:
            self.update_status("Installing dependencies...", 20)
            
            # Install root requirements
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            
            # Install backend requirements
            backend_reqs = Path("backend-api/requirements.txt")
            if backend_reqs.exists():
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(backend_reqs)], check=True)
            
            # Install dashboard requirements
            dashboard_reqs = Path("dashboard/requirements.txt")
            if dashboard_reqs.exists():
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(dashboard_reqs)], check=True)
                
            self.update_status("Dependencies installed successfully", 40)
            return True
            
        except subprocess.CalledProcessError as e:
            self.show_error(f"Failed to install dependencies: {str(e)}")
            return False
            
    def start_backend(self):
        """Start the FastAPI backend service"""
        if self.check_port_in_use(8000):
            self.show_error("Backend port 8000 is already in use")
            return False
            
        try:
            self.update_status("Starting backend service...", 60)
            
            # Use platform-specific script
            if sys.platform == "darwin":  # macOS
                script = "./launch_backend.sh"
            else:
                script = "launch_backend.sh"
                
            self.backend_process = subprocess.Popen(
                script,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for backend to be ready
            time.sleep(5)  # Give the backend time to start
            
            if self.backend_process.poll() is not None:
                self.show_error("Backend failed to start")
                return False
                
            self.update_status("Backend service started", 80)
            return True
            
        except Exception as e:
            self.show_error(f"Failed to start backend: {str(e)}")
            return False
            
    def start_dashboard(self):
        """Start the Streamlit dashboard"""
        if self.check_port_in_use(8501):
            self.show_error("Dashboard port 8501 is already in use")
            return False
            
        try:
            self.update_status("Starting dashboard...", 90)
            
            # Use platform-specific script
            if sys.platform == "darwin":  # macOS
                script = "./launch_dashboard.sh"
            else:
                script = "launch_dashboard.sh"
                
            self.dashboard_process = subprocess.Popen(
                script,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for dashboard to be ready
            time.sleep(5)
            
            if self.dashboard_process.poll() is not None:
                self.show_error("Dashboard failed to start")
                return False
                
            self.update_status("Services started successfully!", 100)
            
            # Open browser after short delay
            self.root.after(1000, lambda: webbrowser.open('http://localhost:8501'))
            return True
            
        except Exception as e:
            self.show_error(f"Failed to start dashboard: {str(e)}")
            return False
            
    def start_services(self):
        """Main service startup sequence"""
        self.start_button.configure(state='disabled')
        
        # Check conda environment
        if not self.verify_conda_env():
            self.start_button.configure(state='normal')
            return
            
        # Install dependencies
        if not self.install_dependencies():
            self.start_button.configure(state='normal')
            return
            
        # Start backend
        if not self.start_backend():
            self.cleanup()
            self.start_button.configure(state='normal')
            return
            
        # Start dashboard
        if not self.start_dashboard():
            self.cleanup()
            self.start_button.configure(state='normal')
            return
            
    def verify_conda_env(self):
        """Verify that we're running in the correct conda environment"""
        try:
            self.update_status("Checking conda environment...", 10)
            
            # Check if we're in a conda environment
            if 'CONDA_DEFAULT_ENV' not in os.environ:
                self.show_error("Please activate the khanbot conda environment first")
                return False
                
            # Verify it's the correct environment
            if os.environ['CONDA_DEFAULT_ENV'] != 'khanbot':
                self.show_error("Please activate the 'khanbot' conda environment")
                return False
                
            return True
            
        except Exception as e:
            self.show_error(f"Failed to verify conda environment: {str(e)}")
            return False
            
    def update_status(self, message, progress=None):
        """Update status message and progress bar"""
        self.status_label.config(text=message)
        if progress is not None:
            self.progress['value'] = progress
        self.root.update()
        
    def show_error(self, message):
        """Show error message to user"""
        messagebox.showerror("Error", message)
        
    def cleanup(self):
        """Clean up processes on shutdown"""
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                
        if self.dashboard_process:
            self.dashboard_process.terminate()
            try:
                self.dashboard_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.dashboard_process.kill()
                
    def on_closing(self):
        """Handle window closing event"""
        if messagebox.askokcancel("Quit", "Do you want to quit KhanBot?"):
            self.cleanup()
            self.root.destroy()
            
    def run(self):
        """Start the launcher application"""
        self.root.mainloop()

if __name__ == "__main__":
    launcher = KhanBotLauncher()
    launcher.run()