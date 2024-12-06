import subprocess
import os
import time
import webbrowser


def main():
    try:
        # Start backend from backend-api environment
        print("Starting backend API...")
        os.chdir("backend-api")

        # Run uvicorn directly in the backend-api environment
        backend_process = subprocess.Popen(
            ["conda", "run", "-n", "backend-api", "uvicorn", "main:app", "--reload"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        os.chdir("..")  # Move back to the root directory

        # Start dashboard from dashboard environment
        print("Starting dashboard...")
        os.chdir("dashboard")

        dashboard_process = subprocess.Popen(
            ["conda", "run", "-n", "dashboard", "make", "run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Open the dashboard after a short delay to allow startup
        time.sleep(10)
        webbrowser.open("http://localhost:8501")
        print("Dashboard is available at http://localhost:8501")

        # Keep the script running and display output
        while True:
            backend_output = backend_process.stdout.readline()
            if backend_output:
                print(f"[Backend] {backend_output.strip()}")

            dashboard_output = dashboard_process.stdout.readline()
            if dashboard_output:
                print(f"[Dashboard] {dashboard_output.strip()}")

    except KeyboardInterrupt:
        print("\nShutting down services...")
        backend_process.terminate()
        dashboard_process.terminate()
    finally:
        os.chdir("..")


if __name__ == "__main__":
    main()
