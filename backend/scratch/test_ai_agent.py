import sys
import os
import asyncio
from unittest.mock import MagicMock, patch

# Adjust path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agent import optimize_for_carbon, print_side_by_side

async def main():
    print("Testing print_side_by_side formatting layout:")
    old_code = "for i in range(10):\n    for j in range(10):\n        print(i, j)"
    new_code = "import itertools\nfor i, j in itertools.product(range(10), range(10)):\n    print(i, j)"
    print_side_by_side(old_code, new_code)
    
    print("Testing optimize_for_carbon:")
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("GEMINI_API_KEY is available. Running a real API call...")
        unoptimized = "for x in items:\n    if x in other_items:\n        count += 1"
        optimized = await optimize_for_carbon(unoptimized)
        print_side_by_side(unoptimized, optimized)
    else:
        print("GEMINI_API_KEY is NOT set. Running a mocked API call...")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": '{"optimized_code": "other_set = set(other_items)\\nfor x in items:\\n    if x in other_set:\\n        count += 1"}'
                            }
                        ]
                    }
                }
            ]
        }
        
        with patch("httpx.AsyncClient.post", return_value=mock_response):
            # Temporarily set a dummy key to bypass the early exit check
            os.environ["GEMINI_API_KEY"] = "dummy_key"
            try:
                unoptimized = "for x in items:\n    if x in other_items:\n        count += 1"
                optimized = await optimize_for_carbon(unoptimized)
                print_side_by_side(unoptimized, optimized)
            finally:
                del os.environ["GEMINI_API_KEY"]
                
    print("AI Agent unit tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
