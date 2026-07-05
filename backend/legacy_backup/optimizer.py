import os
import json
import re

# We will lazily load google-generativeai to prevent import errors if installation is still running
genai = None

def get_gemini_client():
    global genai
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        import google.generativeai as google_genai
        google_genai.configure(api_key=api_key)
        genai = google_genai
        return genai
    except Exception as e:
        print(f"Failed to load or configure google-generativeai: {e}")
        return None

def get_simulated_optimization(problem_type: str, original_code: str) -> dict:
    """
    Returns high-quality, realistic optimized code, explanation, and metrics
    when API keys are not present, enabling instant local testing.
    """
    if problem_type == "nested_loops":
        # Check if we can do a smart lookup simulation
        optimized = (
            "# Optimized using a hash map lookup (O(n) instead of O(n²))\n"
            "lookup_map = {item.id: item for item in items_b}\n"
            "results = []\n"
            "for item_a in items_a:\n"
            "    if item_a.foreign_key in lookup_map:\n"
            "        results.append((item_a, lookup_map[item_a.foreign_key]))"
        )
        explanation = (
            "Replaced a nested loop lookup (O(n²)) with a hash map lookup (O(1) average lookup time).\n"
            "This reduces the time complexity to O(n + m), saving millions of CPU instruction cycles "
            "when processing large datasets."
        )
        return {
            "optimized_code": optimized,
            "explanation": explanation,
            "estimated_cpu_cycles_saved": 2500000.0,
            "estimated_co2_saved_g": 0.45
        }
        
    elif problem_type == "string_concatenation_in_loop":
        optimized = (
            "# Optimized using list joining (O(n) instead of O(n²))\n"
            "parts = []\n"
            "for item in data:\n"
            "    parts.append(str(item))\n"
            "result_str = ''.join(parts)"
        )
        explanation = (
            "String concatenation via `+=` inside loops causes python to re-allocate memory for strings "
            "repeatedly. Appending to a list and joining at the end is memory-efficient and runs in linear O(n) time."
        )
        return {
            "optimized_code": optimized,
            "explanation": explanation,
            "estimated_cpu_cycles_saved": 850000.0,
            "estimated_co2_saved_g": 0.15
        }

    elif problem_type == "heavy_base_image":
        # Replace FROM python:3.12 with python:3.12-slim
        optimized = original_code.replace("FROM python:3.12", "FROM python:3.12-slim")
        if optimized == original_code:
            optimized = "FROM python:3.12-slim"
            
        explanation = (
            "Switched base image from standard Python to python:3.12-slim. This decreases base image footprint "
            "from ~1GB to ~120MB, saving network transfer CPU cycles and registry storage energy."
        )
        return {
            "optimized_code": optimized,
            "explanation": explanation,
            "estimated_cpu_cycles_saved": 15000000.0,
            "estimated_co2_saved_g": 2.70
        }

    elif problem_type == "unchained_run_commands":
        # Mock chained run
        optimized = (
            "RUN apt-get update && apt-get install -y --no-install-recommends \\\n"
            "    git \\\n"
            "    curl \\\n"
            "    && rm -rf /var/lib/apt/lists/*"
        )
        explanation = (
            "Chained multiple RUN layers into a single layered instruction and cleaned up package cache. "
            "This limits Docker build cache footprint, decreases storage allocations, and saves processing overhead."
        )
        return {
            "optimized_code": optimized,
            "explanation": explanation,
            "estimated_cpu_cycles_saved": 8000000.0,
            "estimated_co2_saved_g": 1.44
        }

    elif problem_type == "missing_resource_limits":
        # Mock limits added
        optimized = (
            "          resources:\n"
            "            requests:\n"
            "              memory: '256Mi'\n"
            "              cpu: '100m'\n"
            "            limits:\n"
            "              memory: '512Mi'\n"
            "              cpu: '500m'"
        )
        explanation = (
            "Added CPU and memory requests/limits. This prevents cluster resources from being over-provisioned "
            "and stops runaway pods from starving other workloads, ensuring maximum resource efficiency."
        )
        return {
            "optimized_code": optimized,
            "explanation": explanation,
            "estimated_cpu_cycles_saved": 12000000.0,
            "estimated_co2_saved_g": 2.16
        }

    else:
        # Fallback simulation
        return {
            "optimized_code": original_code,
            "explanation": "No optimizations suggested.",
            "estimated_cpu_cycles_saved": 0.0,
            "estimated_co2_saved_g": 0.0
        }

def optimize_code_snippet(problem_type: str, original_code: str, file_path: str) -> dict:
    """
    Main driver to optimize code. If GEMINI_API_KEY is available, queries Gemini API.
    Otherwise, returns high-quality simulation data.
    """
    client = get_gemini_client()
    if not client:
        print("GEMINI_API_KEY not configured. Using high-quality Simulated Optimization.")
        return get_simulated_optimization(problem_type, original_code)
        
    try:
        # We query Gemini model (gemini-2.5-flash or gemini-1.5-flash)
        model = client.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
You are an Elite Enterprise Full-Stack and DevOps Engineer. Your task is to optimize the following computationally heavy or carbon-heavy code block.
File Path: {file_path}
Problem Type: {problem_type}

Original Code Snippet:
```
{original_code}
```

Please output a JSON response containing the optimized replacement code, a detailed explanation of why it is more CPU or carbon efficient, and an estimate of the CPU cycles saved and estimated CO2 prevented (in grams).

Your response MUST follow this exact JSON structure and nothing else:
{{
  "optimized_code": "the replacement code block only",
  "explanation": "a concise technical explanation",
  "estimated_cpu_cycles_saved": 1500000.0,
  "estimated_co2_saved_g": 0.27
}}
"""
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        data = json.loads(response.text.strip())
        return {
            "optimized_code": data.get("optimized_code", original_code),
            "explanation": data.get("explanation", ""),
            "estimated_cpu_cycles_saved": float(data.get("estimated_cpu_cycles_saved", 0.0)),
            "estimated_co2_saved_g": float(data.get("estimated_co2_saved_g", 0.0))
        }
        
    except Exception as e:
        print(f"Gemini API optimization error: {e}. Falling back to simulation.")
        return get_simulated_optimization(problem_type, original_code)
