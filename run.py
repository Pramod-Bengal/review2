import subprocess
import sys
import os

def install_dependencies():
    """
    Ensures all dependencies in requirements.txt are installed.
    """
    print("Checking and installing dependencies...")
    req_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req_file):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
            print("Dependencies successfully verified.")
        except Exception as e:
            print(f"Warning: Failed to auto-install dependencies: {e}")
            print("Please ensure you run: pip install -r requirements.txt manually if startup fails.")
    else:
        print("requirements.txt not found. Skipping auto-install.")

def start_server():
    """
    Launches the FastAPI application using Uvicorn.
    """
    import uvicorn
    print("\n" + "="*60)
    print("AI Financial & Website Intelligence Hub is booting up...")
    print("Dashboard local URL: http://127.0.0.1:8000")
    print("="*60 + "\n")
    
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    install_dependencies()
    start_server()
