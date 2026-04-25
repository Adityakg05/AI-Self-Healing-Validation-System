import subprocess
import time
import sys
import os
import signal

def run_services():
    print("🚀 Starting Self-Healing SRE Agent...")
    
    # Start FastAPI
    print("📦 [1/2] Starting FastAPI backend on port 8000...")
    fastapi_proc = subprocess.Popen(
        [sys.executable, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    # Wait for FastAPI to warm up
    time.sleep(3)
    
    # Start Streamlit
    print("📊 [2/2] Starting Streamlit UI on port 8501...")
    streamlit_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "ui.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    print("\n✅ Both services are backgrounded!")
    print("   - API: http://localhost:8000")
    print("   - UI:  http://localhost:8501")
    print("\nStarting Unified Log Monitor (Ctrl+C to stop both)...\n" + "-"*50)
    
    try:
        while True:
            # Poll both processes
            for proc, name in [(fastapi_proc, "FASTAPI"), (streamlit_proc, "STREAMLIT")]:
                line = proc.stdout.readline()
                if line:
                    print(f"[{name}] {line.strip()}")
                
                if proc.poll() is not None:
                    print(f"❌ {name} process died with exit code {proc.returncode}")
                    sys.exit(1)
            
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        fastapi_proc.terminate()
        streamlit_proc.terminate()
        print("✅ Cleaned up. Goodbye!")

if __name__ == "__main__":
    run_services()
