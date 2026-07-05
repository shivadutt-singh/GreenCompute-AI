import httpx
import json
import time

def trigger_mock_webhook():
    url = "http://localhost:8000/api/webhook/github"
    
    payload = {
        "action": "opened",
        "number": 12,
        "repository": {
            "full_name": "google/jax",
            "name": "jax"
        },
        "pull_request": {
            "number": 12,
            "title": "Optimize transformer attention logic",
            "url": "https://api.github.com/repos/google/jax/pulls/12",
            "html_url": "https://github.com/google/jax/pull/12",
            "diff_url": "https://github.com/google/jax/pull/12.diff",
            "user": {
                "login": "octocat"
            },
            "head": {
                "sha": "a1b2c3d4e5f6g7h8i9j0"
            }
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request"
    }
    
    print(f"Sending mock Pull Request webhook event to {url}...")
    try:
        response = httpx.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Webhook processed successfully!")
            print("Response:", response.json())
        else:
            print(f"Server returned status code {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"Error connecting to FastAPI backend: {e}")
        print("Make sure uvicorn is running on http://localhost:8000!")

if __name__ == "__main__":
    trigger_mock_webhook()
