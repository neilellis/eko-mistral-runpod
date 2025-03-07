import subprocess
import runpod
import threading
import uvicorn
import importlib.util
import os
import sys

def start_ollama_server():
    """Start the Ollama server"""
    print("Starting Ollama server")
    server_process = subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Ollama server started")
    return server_process

def handler(event):
    """RunPod handler function"""
    # Check if this is an OpenAI API request
    if event.get("path", "").startswith("/v1/"):
        # This is handled by the FastAPI server running on port 8000
        # Just return a message indicating where the OpenAI API is available
        return {
            "output": {
                "message": "OpenAI compatible API is available at http://localhost:8000/v1/",
                "docs": "OpenAI API documentation at http://localhost:8000/docs"
            }
        }
    
    # Regular Ollama prompt handling
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

def start_openai_api_server():
    """Start the OpenAI-compatible API server"""
    try:
        # Import the OpenAI API module
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from openai_api import app
        
        # Start the FastAPI server
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"Error starting OpenAI API server: {str(e)}")

# Initialize: start the Ollama server
global ollama_process
ollama_process = start_ollama_server()

# Start the OpenAI API server in a separate thread
api_thread = threading.Thread(target=start_openai_api_server, daemon=True)
api_thread.start()
print("OpenAI-compatible API server started on port 8000")

# Start the RunPod serverless handler
print("Starting RunPod serverless handler")
runpod.serverless.start({"handler": handler})