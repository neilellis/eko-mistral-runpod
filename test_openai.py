import argparse
import json
import requests

def test_openai_api(endpoint_url, prompt):
    """Test the OpenAI-compatible API endpoint"""
    
    # First, check available models
    models_url = f"{endpoint_url}/v1/models"
    print(f"Checking models at {models_url}")
    
    try:
        models_response = requests.get(models_url)
        if models_response.status_code == 200:
            print("Models available:")
            print(json.dumps(models_response.json(), indent=2))
        else:
            print(f"Error: {models_response.status_code}")
            print(models_response.text)
            return
    except Exception as e:
        print(f"Error connecting to API: {str(e)}")
        return
    
    # Create chat completion
    completions_url = f"{endpoint_url}/v1/chat/completions"
    
    payload = {
        "model": "eko-mistral",
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"\nSending request to {completions_url} with prompt: {prompt}")
    try:
        response = requests.post(completions_url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            result = response.json()
            print("\nResponse:")
            print(json.dumps(result, indent=2))
            
            # Extract and print the actual message content
            if result.get("choices") and len(result["choices"]) > 0:
                message = result["choices"][0].get("message", {})
                print("\nAssistant's response:")
                print(message.get("content", "No content"))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Eko Mistral OpenAI-compatible API")
    parser.add_argument("--url", default="http://localhost:8000", help="The base URL of the API (without /v1)")
    parser.add_argument("--prompt", default="What is climate change?", help="The prompt to send to the model")
    
    args = parser.parse_args()
    test_openai_api(args.url, args.prompt)