import subprocess
import sys
import os
import signal
import time
from pathlib import Path
import logging
import threading

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def stream_process_output(process, name):
    """Stream process output to console"""
    for line in iter(process.stdout.readline, b''):
        logging.info(f"{name}: {line.decode().strip()}")
    for line in iter(process.stderr.readline, b''):
        logging.error(f"{name} ERROR: {line.decode().strip()}")

class AppLauncher:
    def __init__(self):
        self.backend_process = None
        self.streamlit_process = None
        self.backend_path = Path("backend-api")
        self.dashboard_path = Path("dashboard")
        self.backend_port = 8000
        self.streamlit_port = 8501
        self.output_threads = []
        
        # Get conda executable path
        self.conda_path = self._get_conda_path()

    def _get_conda_path(self):
        """Get the path to conda executable"""
        if 'CONDA_EXE' in os.environ:
            return os.environ['CONDA_EXE']
        
        # Try common locations
        conda_locations = [
            os.path.expanduser('~/miniconda3/bin/conda'),
            os.path.expanduser('~/anaconda3/bin/conda'),
            '/opt/conda/bin/conda',
            'conda'  # if it's in PATH
        ]
        
        for loc in conda_locations:
            try:
                subprocess.run([loc, '--version'], capture_output=True)
                return loc
            except (FileNotFoundError, subprocess.CalledProcessError):
                continue
        
        raise RuntimeError("Could not find conda executable")

    def check_port_available(self, port):
        """Check if a port is available"""
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        available = True
        try:
            sock.bind(('localhost', port))
        except OSError:
            available = False
        finally:
            sock.close()
        return available

    def start_backend(self):
        """Start the FastAPI backend server"""
        if not self.check_port_available(self.backend_port):
            raise RuntimeError(f"Port {self.backend_port} is already in use")

        os.chdir(self.backend_path)
        logging.info("Starting backend server...")
        
        # Construct the command to run in backend-api environment
        activate_cmd = f"source $(dirname $(dirname {self.conda_path}))/etc/profile.d/conda.sh && "
        activate_cmd += "conda activate backend-api && "
        activate_cmd += "source set_environment.sh && "
        cmd = activate_cmd + f"uvicorn main:app --reload --port {self.backend_port}"
        
        self.backend_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable='/bin/bash',
            preexec_fn=os.setsid,
            bufsize=1,
            universal_newlines=True
        )
        
        # Start output streaming thread
        backend_thread = threading.Thread(
            target=stream_process_output,
            args=(self.backend_process, "Backend"),
            daemon=True
        )
        backend_thread.start()
        self.output_threads.append(backend_thread)
        
        logging.info(f"Backend server started on http://localhost:{self.backend_port}")
        os.chdir("..")

    def start_streamlit(self):
        """Start the Streamlit dashboard using make run"""
        if not self.check_port_available(self.streamlit_port):
            raise RuntimeError(f"Port {self.streamlit_port} is already in use")

        os.chdir(self.dashboard_path)
        logging.info("Starting Streamlit dashboard...")
        
        # Construct the command to run in dashboard environment
        activate_cmd = f"source $(dirname $(dirname {self.conda_path}))/etc/profile.d/conda.sh && "
        activate_cmd += "conda activate dashboard && "
        cmd = activate_cmd + "make run"
        
        self.streamlit_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable='/bin/bash',
            preexec_fn=os.setsid,
            bufsize=1,
            universal_newlines=True
        )
        
        # Start output streaming thread
        streamlit_thread = threading.Thread(
            target=stream_process_output,
            args=(self.streamlit_process, "Streamlit"),
            daemon=True
        )
        streamlit_thread.start()
        self.output_threads.append(streamlit_thread)
        
        logging.info(f"Streamlit dashboard started on http://localhost:{self.streamlit_port}")
        os.chdir("..")

    def stop_processes(self):
        """Stop all running processes"""
        logging.info("Stopping all processes...")
        
        def kill_process(process):
            if process:
                try:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                except (ProcessLookupError, OSError):
                    pass  # Process already terminated

        kill_process(self.backend_process)
        kill_process(self.streamlit_process)
        
        # Wait for output threads to finish
        for thread in self.output_threads:
            thread.join(timeout=1)
            
        logging.info("All processes stopped")

    def check_environments(self):
        """Check if required conda environments exist"""
        try:
            # Check backend-api environment
            result = subprocess.run(
                f"{self.conda_path} env list",
                shell=True,
                capture_output=True,
                text=True
            )
            
            envs = result.stdout.lower()
            if 'backend-api' not in envs:
                raise RuntimeError("backend-api conda environment not found")
            if 'dashboard' not in envs:
                raise RuntimeError("dashboard conda environment not found")
                
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error checking conda environments: {e}")

    def run(self):
        """Run the complete application"""
        try:
            # Check environments first
            self.check_environments()
            
            # Start both servers
            self.start_backend()
            self.start_streamlit()
            
            logging.info("\nApplication is running!")
            logging.info(f"Backend API: http://localhost:{self.backend_port}")
            logging.info(f"Dashboard: http://localhost:{self.streamlit_port}")
            logging.info("\nPress Ctrl+C to stop the application")
            
            # Keep the script running and monitor processes
            while True:
                time.sleep(1)
                # Check if either process has ended
                if (self.backend_process.poll() is not None or 
                    self.streamlit_process.poll() is not None):
                    raise RuntimeError("One or more processes stopped unexpectedly")
                
        except KeyboardInterrupt:
            logging.info("\nShutdown requested...")
            self.stop_processes()
            logging.info("Application stopped successfully")
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            self.stop_processes()
            sys.exit(1)

if __name__ == "__main__":
    try:
        launcher = AppLauncher()
        launcher.run()
    except Exception as e:
        logging.error(f"Failed to start application: {e}")
        sys.exit(1)