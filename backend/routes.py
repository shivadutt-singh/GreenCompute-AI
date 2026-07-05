from fastapi import APIRouter, status
import httpx
import os

try:
    from backend.schemas import GitHubPRPayload
    from backend.ast_parser import extract_heavy_logic
    from backend.ai_agent import optimize_for_carbon, print_side_by_side
except ModuleNotFoundError:
    from schemas import GitHubPRPayload
    from ast_parser import extract_heavy_logic
    from ai_agent import optimize_for_carbon, print_side_by_side

router = APIRouter()

@router.post("/webhook/github", status_code=status.HTTP_200_OK)
async def github_webhook(payload: GitHubPRPayload):
    # Extract details
    action = payload.action
    pr_number = payload.number
    repo_name = payload.repository.full_name
    
    # Extract URLs for modified files
    diff_url = payload.pull_request.diff_url
    files_url = payload.pull_request.files_url
    
    print("\n==================================================")
    print("RECEIVED GITHUB WEBHOOK PAYLOAD")
    print(f"Action: {action}")
    print(f"PR Number: {pr_number}")
    print(f"Repository: {repo_name}")
    print(f"Modified Files URL (Diff): {diff_url}")
    print(f"Modified Files URL (API): {files_url}")
    print("==================================================\n")
    
    # Fetch raw file content and extract heavy logic when a PR comes in
    if files_url:
        try:
            # Configure headers for GitHub API
            headers = {"User-Agent": "GreenCompute-AI-Agentic-Engine"}
            token = os.getenv("GITHUB_TOKEN")
            if token:
                headers["Authorization"] = f"Bearer {token}"
                
            async with httpx.AsyncClient(follow_redirects=True) as client:
                files_resp = await client.get(files_url, headers=headers)
                if files_resp.status_code == 200:
                    files_data = files_resp.json()
                    # Iterate through files in the PR
                    for file_info in files_data:
                        filename = file_info.get("filename", "")
                        # Process python files
                        if filename.endswith(".py"):
                            raw_url = file_info.get("raw_url")
                            if raw_url:
                                raw_resp = await client.get(raw_url, headers=headers)
                                if raw_resp.status_code == 200:
                                    raw_code = raw_resp.text
                                    # Extract heavy logic
                                    heavy_nodes = extract_heavy_logic(raw_code)
                                    # Print to console
                                    print(f"--- Isolated Heavy Nodes in {filename} ---")
                                    if heavy_nodes:
                                        for idx, node in enumerate(heavy_nodes, 1):
                                            print(f"Running GreenOps AI optimization on Node {idx}...")
                                            optimized_node = await optimize_for_carbon(node)
                                            # Print side-by-side
                                            print_side_by_side(node, optimized_node)
                                    else:
                                        print("No computationally heavy loops found.")
                                    print("=" * 40)
                                else:
                                    print(f"Failed to fetch raw file content for {filename}. Status: {raw_resp.status_code}")
                            else:
                                print(f"No raw_url found for {filename}")
                else:
                    print(f"Failed to fetch PR files from {files_url}. Status: {files_resp.status_code}")
        except Exception as e:
            print(f"Error processing webhook PR files: {e}")
            
    return {
        "status": "success",
        "message": "Webhook received successfully",
        "data": {
            "action": action,
            "pr_number": pr_number,
            "repository": repo_name,
            "modified_files_url": diff_url
        }
    }

# Mock dataset of the last 3 PR fixes for Phase 5 integration
MOCK_PR_FIXES = [
    {
        "id": 1,
        "pr_number": 101,
        "repo_name": "google/jax",
        "pr_title": "Optimize attention matrix multiplication",
        "author": "octocat",
        "file_path": "jax/layers.py",
        "start_line": 12,
        "end_line": 18,
        "original_code": "def matmul(A, B):\n    result = []\n    for i in range(len(A)):\n        row = []\n        for j in range(len(B[0])):\n            val = 0\n            for k in range(len(B)):\n                val += A[i][k] * B[k][j]\n            row.append(val)\n        result.append(row)\n    return result",
        "optimized_code": "import numpy as np\n\ndef matmul(A, B):\n    # Optimized using NumPy to reduce CPU execution cycles\n    return np.dot(A, B).tolist()",
        "explanation": "Replaced manual O(N^3) matrix multiplication loops with NumPy dot product to optimize performance and reduce carbon footprint.",
        "cpu_cycles_saved": 850000,
        "co2_saved_g": 0.45,
        "status": "OPTIMIZED",
        "created_at": "2026-07-05T21:40:00Z"
    },
    {
        "id": 2,
        "pr_number": 102,
        "repo_name": "facebook/react",
        "pr_title": "Improve state rendering lookup efficiency",
        "author": "dan_abramov",
        "file_path": "packages/react-reconciler/src/ReactFiberWorkLoop.js",
        "start_line": 85,
        "end_line": 95,
        "original_code": "function findNode(nodes, targetId) {\n  for (let i = 0; i < nodes.length; i++) {\n    if (nodes[i].id === targetId) {\n      return nodes[i];\n    }\n  }\n  return null;\n}",
        "optimized_code": "const nodeMap = new Map(nodes.map(n => [n.id, n]));\nfunction findNode(nodes, targetId) {\n  // Optimized lookup to O(1) using Map cache\n  return nodeMap.get(targetId) || null;\n}",
        "explanation": "Converted linear search O(N) into map lookup O(1) to avoid redundant iterations and save CPU computation.",
        "cpu_cycles_saved": 1200000,
        "co2_saved_g": 0.63,
        "status": "OPTIMIZED",
        "created_at": "2026-07-05T21:42:00Z"
    },
    {
        "id": 3,
        "pr_number": 103,
        "repo_name": "tensorflow/tensorflow",
        "pr_title": "Optimize constant tensor calculation",
        "author": "mrry",
        "file_path": "tensorflow/python/ops/math_ops.py",
        "start_line": 210,
        "end_line": 218,
        "original_code": "def calculate_squares(items):\n    squares = []\n    for item in items:\n        squares.append(item * item)\n    return squares",
        "optimized_code": "def calculate_squares(items):\n    # Optimized list comprehension which executes faster in CPython\n    return [item * item for item in items]",
        "explanation": "Converted manual list appending loop into a list comprehension to leverage optimized C bytecode compilation.",
        "cpu_cycles_saved": 340000,
        "co2_saved_g": 0.18,
        "status": "OPTIMIZED",
        "created_at": "2026-07-05T21:44:00Z"
    }
]

# Cumulative statistics state
STATS_DATA = {
    "total_cpu_cycles_saved": 4210984,
    "total_co2_prevented_g": 143.25,
    "total_prs_intercepted": 3,
    "optimized_prs_count": 3
}

@router.get("/prs/fixes", status_code=status.HTTP_200_OK)
def get_pr_fixes():
    return MOCK_PR_FIXES

@router.get("/stats", status_code=status.HTTP_200_OK)
def get_stats():
    return STATS_DATA

@router.post("/simulate", status_code=status.HTTP_200_OK)
def simulate_webhook():
    STATS_DATA["total_prs_intercepted"] += 1
    STATS_DATA["optimized_prs_count"] += 1
    STATS_DATA["total_cpu_cycles_saved"] += 350000
    STATS_DATA["total_co2_prevented_g"] += 0.15
    return {"status": "success", "message": "Simulation triggered", "pr_number": 104}

