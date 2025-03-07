import json
import requests
import argparse

def test_endpoint(endpoint_url, prompt):
    """Test the RunPod serverless endpoint"""
    
    payload = {
        "input": {
            "prompt": prompt
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Sending request to {endpoint_url} with prompt: {prompt}")
    response = requests.post(endpoint_url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        result = response.json()
        print("\nResponse:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Eko Mistral RunPod endpoint")
    parser.add_argument("--url", required=True, help="The RunPod endpoint URL")
    parser.add_argument("--prompt", default="What is climate change?", help="The prompt to send to the model")
    
    args = parser.parse_args()
    test_endpoint(args.url, args.prompt)