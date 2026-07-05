import os
import json
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def optimize_for_carbon(ast_node_code: str) -> str:
    """
    Optimizes a block of code (an AST loop node) to reduce CPU cycles/carbon footprint
    using the Google Gemini API.
    
    Returns the optimized code (as a string) or the original code if an error occurs.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY is not set in environment or .env file.")
        return ast_node_code
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    system_prompt = (
        "You are an expert GreenOps AI. Optimize the following code block to reduce CPU cycles "
        "(e.g., change O(n^2) to O(n)). You MUST return ONLY a valid JSON object with the key "
        "'optimized_code'. Do not include markdown formatting or explanations."
    )
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": ast_node_code}
                ]
            }
        ],
        "systemInstruction": {
            "parts": [
                {"text": system_prompt}
            ]
        },
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                resp_data = response.json()
                try:
                    candidate_text = resp_data["candidates"][0]["content"]["parts"][0]["text"]
                    
                    # Clean potential markdown JSON wrapping
                    clean_text = candidate_text.strip()
                    if clean_text.startswith("```json"):
                        clean_text = clean_text[7:]
                    if clean_text.endswith("```"):
                        clean_text = clean_text[:-3]
                    clean_text = clean_text.strip()
                    
                    parsed_json = json.loads(clean_text)
                    return parsed_json.get("optimized_code", ast_node_code)
                except (KeyError, IndexError, json.JSONDecodeError) as e:
                    print(f"Error parsing Gemini response JSON: {e}")
                    print(f"Raw Gemini text: {candidate_text if 'candidate_text' in locals() else 'N/A'}")
                    return ast_node_code
            else:
                print(f"Gemini API request failed with status: {response.status_code}")
                print(f"Response: {response.text}")
                return ast_node_code
    except Exception as e:
        print(f"Exception during Gemini API request: {e}")
        return ast_node_code

def print_side_by_side(old_code: str, new_code: str, width: int = 50):
    """
    Prints old_code and new_code side-by-side in the terminal console.
    """
    old_lines = old_code.splitlines()
    new_lines = new_code.splitlines()
    max_lines = max(len(old_lines), len(new_lines))
    
    print("\n" + "=" * (width * 2 + 3))
    print(f"{'ORIGINAL CODE (AST Loop Node)'.center(width)} | {'OPTIMIZED CODE (GreenOps AI)'.center(width)}")
    print("=" * (width * 2 + 3))
    
    for i in range(max_lines):
        left = old_lines[i] if i < len(old_lines) else ""
        right = new_lines[i] if i < len(new_lines) else ""
        
        # Format columns with padding and truncation
        left_padded = left.ljust(width)[:width]
        right_padded = right.ljust(width)[:width]
        print(f"{left_padded} | {right_padded}")
        
    print("=" * (width * 2 + 3) + "\n")
