import sys
import os
import asyncio
from unittest.mock import MagicMock, patch

# Adjust path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

def test_webhook_integration():
    print("Starting integration test for /api/webhook/github endpoint...")
    client = TestClient(app)
    
    # Set up mock response for the files list request using MagicMock
    mock_files_response = MagicMock()
    mock_files_response.status_code = 200
    mock_files_response.json.return_value = [
        {
            "filename": "heavy_code.py",
            "raw_url": "https://raw.githubusercontent.com/test/repo/main/heavy_code.py"
        },
        {
            "filename": "README.md",
            "raw_url": "https://raw.githubusercontent.com/test/repo/main/README.md"
        }
    ]
    
    # Set up mock response for the raw python file content request using MagicMock
    mock_raw_code_response = MagicMock()
    mock_raw_code_response.status_code = 200
    mock_raw_code_response.text = """
def process_data(items):
    for item in items:
        print(item)
        while item.has_more():
            item.process()
"""
    
    # Helper function to mock HTTP GET requests based on URL
    async def mock_get(url, *args, **kwargs):
        print(f"[Mock Client GET] -> {url}")
        if "files" in url:
            return mock_files_response
        elif "heavy_code.py" in url:
            return mock_raw_code_response
        # Return a 404 response
        res = MagicMock()
        res.status_code = 404
        return res
        
    payload = {
        "action": "opened",
        "number": 42,
        "repository": {
            "full_name": "test/repo",
            "name": "repo"
        },
        "pull_request": {
            "number": 42,
            "title": "Add loop extraction features",
            "url": "https://api.github.com/repos/test/repo/pulls/42",
            "html_url": "https://github.com/test/repo/pull/42",
            "diff_url": "https://github.com/test/repo/pull/42.diff"
        }
    }
    
    # Patch httpx.AsyncClient.get to intercept outgoing HTTP calls
    with patch("httpx.AsyncClient.get", side_effect=mock_get):
        response = client.post("/api/webhook/github", json=payload)
        
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    print("\nIntegration test passed successfully!")
    
if __name__ == "__main__":
    test_webhook_integration()
