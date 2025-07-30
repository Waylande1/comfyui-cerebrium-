# main.py
from flask import Flask
import subprocess
import threading
import time
import os

app = Flask(__name__)

@app.route('/')
def health():
    return """
    <h1>🔧 ComfyUI Starting on Cerebrium</h1>
    <p>Downloading models and starting server...</p>
    <p><strong>Refresh in 2–3 minutes.</strong></p>
    <meta http-equiv="refresh" content="10">
    """, 200

def run_startup_commands():
    """Run bash-like setup commands"""
    print("🛠️ Running startup commands...")

    # 1. Update system and install tools
    print("📦 Installing git, wget...")
    subprocess.run("apt-get update && apt-get install -y git wget", shell=True)

    # 2. Create model directories
    print("📁 Creating model folders...")
    subprocess.run(["mkdir", "-p", "models/checkpoints"])
    subprocess.run(["mkdir", "-p", "ComfyUI/custom_nodes"])

    # 3. Clone ComfyUI if not exists
    if not os.path.exists("ComfyUI"):
        print("⬇️ Cloning ComfyUI...")
        subprocess.run([
            "git", "clone", "https://github.com/comfyanonymous/ComfyUI.git"
        ], check=True)

    # 4. (Optional) Download a small test model
    checkpoint_path = "models/checkpoints/v1-5-pruned-emaonly.ckpt"
    if not os.path.exists(checkpoint_path):
        print("⏬ Downloading Stable Diffusion 1.5 model...")
        subprocess.run([
            "wget", "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt",
            "-O", checkpoint_path
        ])

    # 5. (Optional) Clone a popular custom node: ComfyUI-Manager
    if not os.path.exists("ComfyUI/custom_nodes/ComfyUI-Manager"):
        print("🧩 Installing ComfyUI-Manager...")
        subprocess.run([
            "git", "clone",
            "https://github.com/ltdrdata/ComfyUI-Manager",
            "ComfyUI/custom_nodes/ComfyUI-Manager"
        ])

    # 6. Symlink models into ComfyUI
    print("🔗 Linking models...")
    subprocess.run("ln -sf ../models/checkpoints/* ComfyUI/models/checkpoints/", shell=True)

    # 7. Start ComfyUI
    print("🚀 Starting ComfyUI...")
    cmd = [
        "python", "ComfyUI/main.py",
        "--listen", "0.0.0.0",
        "--port", "8080",
        "--enable-cors-header"
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    # Run setup in background thread
    thread = threading.Thread(target=run_startup_commands, daemon=True)
    thread.start()

    # Keep Flask alive for health checks
    app.run(host="0.0.0.0", port=8080)
