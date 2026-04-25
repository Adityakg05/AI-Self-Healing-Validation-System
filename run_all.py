import subprocess
import time
import sys
import os
import threading

def stream_logs(pipe, prefix):
    for line in iter(pipe.readline, ''):
        if line:
            print(f"[{prefix}] {line.strip()}")
    pipe.close()

def run_services():
    print("Starting Self-Healing SRE Agent...")
    
    # Start FastAPI
    print("[1/2] Starting FastAPI backend on port 8000...")
    fastapi_proc = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Start Streamlit
    print("[2/2] Starting Streamlit UI on port 8501...")
    streamlit_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "ui.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Use threads to drain logs without blocking the main loop
    t1 = threading.Thread(target=stream_logs, args=(fastapi_proc.stdout, "FASTAPI"), daemon=True)
    t2 = threading.Thread(target=stream_logs, args=(streamlit_proc.stdout, "STREAMLIT"), daemon=True)
    t1.start()
    t2.start()
    
    print("\nBoth services are live!")
    print("   - API: http://localhost:8000")
    print("   - UI:  http://localhost:8501")
    print("\nUnified Log Monitor is active. Press Ctrl+C to stop.\n" + "-"*50)
    
    try:
        while True:
            if fastapi_proc.poll() is not None:
                print(f"FAILED: FastAPI died with exit code {fastapi_proc.returncode}")
                break
            if streamlit_proc.poll() is not None:
                print(f"FAILED: Streamlit died with exit code {streamlit_proc.poll()}")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping services...")
    finally:
        fastapi_proc.terminate()
        streamlit_proc.terminate()
        print("Cleaned up. Goodbye!")

if __name__ == "__main__":
    run_services()
