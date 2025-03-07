import os
import subprocess
import time
import runpod
from huggingface_hub import snapshot_download

# Constants
MODEL_REPO = "neileko/eko-mistral-small"
MODEL_PATH = "/workspace/model"

def download_from_hf():
    """Download the model from HuggingFace"""
    print(f"Downloading model from {MODEL_REPO}")
    snapshot_download(
        repo_id=MODEL_REPO,
        local_dir=MODEL_PATH,
        local_dir_use_symlinks=False
    )
    print("Download complete")

def setup_ollama():
    """Setup Ollama with the downloaded model"""
    print("Setting up Ollama with the downloaded model")
    os.makedirs("/root/.ollama", exist_ok=True)
    
    # Start Ollama server
    server_process = subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # Give Ollama time to start
    
    # Import the model using the Modelfile
    modelfile_path = os.path.join(MODEL_PATH, "Modelfile")
    if not os.path.exists(modelfile_path):
        raise FileNotFoundError(f"Modelfile not found at {modelfile_path}")
    
    subprocess.run(["ollama", "create", "eko-mistral", "-f", modelfile_path], check=True)
    print("Model setup complete")
    
    return server_process

def handler(event):
    """RunPod handler function"""
    # Extract the prompt from the event
    prompt = event.get("input", {}).get("prompt", "")
    if not prompt:
        return {"error": "No prompt provided"}
    
    try:
        # Generate text using Ollama
        print(f"Generating text for prompt: {prompt}")
        result = subprocess.run(
            ["ollama", "run", "eko-mistral", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        
        return {
            "output": {
                "result": result.stdout.strip(),
                "model": "eko-mistral"
            }
        }
    except Exception as e:
        return {"error": str(e)}

# Initialize: download model and set up Ollama
def init():
    download_from_hf()
    global ollama_process
    ollama_process = setup_ollama()

init()
runpod.serverless.start({"handler": handler})