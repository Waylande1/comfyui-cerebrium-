# main.py
import threading
import subprocess
import time
import os

def start_comfyui():
    print("Starting ComfyUI...")
    
    # Clone ComfyUI if not exists (optional: better to use requirements.txt)
    if not os.path.exists("ComfyUI"):
        subprocess.run([
            "git", "clone", "https://github.com/comfyanonymous/ComfyUI.git"
        ])

    # Run ComfyUI
    cmd = [
        "python", "ComfyUI/main.py",
        "--listen", "0.0.0.0",
        "--port", "8080",           # Cerebrium uses port 8080
        "--enable-cors-header",     # Allow cross-origin requests
        "--quick-test-for-ci"       # Optional: speeds up startup for health checks
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    # Run ComfyUI in the main thread (Cerebrium expects long-running process)
    start_comfyui()
