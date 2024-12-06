import subprocess
import time
import sys
import requests
from pathlib import Path

def wait_for_backend(max_attempts=30):
    """Check if backend API is responding"""
    print("Waiting for backend to start...")
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get('http://localhost:8000/health')
            if response.status_code == 200:
                print("Backend is ready!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        attempts += 1
        time.sleep(1)
    return False

def main():
    # Start backend with Unicorn
    backend_path = Path("backend-api/main.py")
    if not backend_path.exists():
        print("Error: Cannot find backend API file")
        return

    print("Starting backend API...")
    backend_process = subprocess.Popen([
        "uvicorn", 
        "backend-api.main:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])

    # Wait for backend to be ready
    if not wait_for_backend():
        print("Error: Backend failed to start")
        backend_process.terminate()
        return

    # Start Streamlit dashboard
    print("Starting dashboard...")
    dashboard_process = subprocess.Popen([
        "streamlit", 
        "run", 
        "dashboard/main.py"
    ])

    try:
        # Keep the script running
        backend_process.wait()
        dashboard_process.wait()
    except KeyboardInterrupt:
        print("\nShutting down services...")
        backend_process.terminate()
        dashboard_process.terminate()

if __name__ == "__main__":
    main()