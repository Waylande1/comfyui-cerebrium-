# main.py
from flask import Flask
import threading
import subprocess
import time
import os

app = Flask(__name__)

# Simple health check endpoint
@app.route('/')
def health():
    return """
    <h1>🔧 ComfyUI is Starting...</h1>
    <p>Waiting for ComfyUI to launch on port 8080...</p>
    <p>Check back in 2–3 minutes. This page will update once ready.</p>
    <meta http-equiv="refresh" content="10">
    """, 200

@app.route('/status')
def status():
    return "ComfyUI backend is loading... see logs for progress.", 200

def wait_and_start():
    """Delay to let health check pass, then start ComfyUI"""
    print("⏳ Waiting 10 seconds before launching ComfyUI...")
    time.sleep(10)

    # Clone ComfyUI if not exists
    if not os.path.exists("ComfyUI"):
        print("📦 Cloning ComfyUI from GitHub...")
        subprocess.run([
            "git", "clone", "https://github.com/comfyanonymous/ComfyUI.git"
        ], check=True)

    print("🚀 Starting ComfyUI server...")
    cmd = [
        "python", "ComfyUI/main.py",
        "--listen", "0.0.0.0",
        "--port", "8080",
        "--enable-cors-header"
    ]
    subprocess.run(cmd)

# Run Flask in main thread for health checks
if __name__ == "__main__":
    # Start ComfyUI in background thread
    thread = threading.Thread(target=wait_and_start, daemon=True)
    thread.start()

    # Keep Flask alive for Cerebrium health checks
    app.run(host="0.0.0.0", port=8080)
