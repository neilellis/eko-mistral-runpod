import subprocess
import runpod

def start_ollama_server():
    """Start the Ollama server"""
    print("Starting Ollama server")
    server_process = subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Ollama server started")
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

# Initialize: just start the Ollama server
global ollama_process
ollama_process = start_ollama_server()

# Start the serverless handler
runpod.serverless.start({"handler": handler})