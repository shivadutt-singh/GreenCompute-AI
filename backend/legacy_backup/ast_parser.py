import os
import re

# We will lazily load tree-sitter since we want the module importable even if tree-sitter isn't fully installed yet
PY_LANGUAGE = None
parser = None

def get_parser():
    global PY_LANGUAGE, parser
    if parser is None:
        try:
            import tree_sitter_python as tspython
            from tree_sitter import Language, Parser
            PY_LANGUAGE = Language(tspython.language())
            parser = Parser(PY_LANGUAGE)
        except Exception as e:
            # Fallback if tree-sitter is still installing or not available
            print(f"Tree-sitter loading error (using fallback regex-based parser): {e}")
            parser = "fallback"
    return parser

def find_nested_loops_ast(node, code_bytes, results):
    """
    Recursively search for nested loops in the tree-sitter AST.
    """
    if node.type in ("for_statement", "while_statement"):
        # Helper to search for a loop in the body of this loop
        def search_loop_in_body(n):
            for child in n.children:
                if child.type in ("for_statement", "while_statement"):
                    return child
                res = search_loop_in_body(child)
                if res:
                    return res
            return None

        # Look in the block/body of the loop
        nested_node = None
        for child in node.children:
            if child.type == "block":
                nested_node = search_loop_in_body(child)
                break

        if nested_node:
            snippet = code_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="ignore")
            results.append({
                "type": "nested_loops",
                "message": "Nested loop detected: potentially O(n²) complexity. Consider vectorization, list comprehensions, or hash-maps to optimize CPU cycles.",
                "snippet": snippet,
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1
            })

    # Continue traversing children
    for child in node.children:
        find_nested_loops_ast(child, code_bytes, results)

def find_inefficient_ops_ast(node, code_bytes, results, inside_loop=False):
    """
    Look for:
    - String concatenation in a loop (e.g. var += string)
    - Membership checks in a loop (e.g. x in list)
    """
    is_loop = node.type in ("for_statement", "while_statement")
    
    if inside_loop:
        # String concatenation check: augmented_assignment like var += ...
        if node.type == "augmented_assignment":
            children_types = [c.type for c in node.children]
            # augmented_assignment children are typically: expression, operator (+=), expression
            if "+=" in code_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="ignore"):
                snippet = code_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="ignore")
                results.append({
                    "type": "string_concatenation_in_loop",
                    "message": "String concatenation using '+=' inside a loop can be O(n²). Consider appending to a list and using ''.join() for better memory efficiency.",
                    "snippet": snippet,
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1
                })

        # Membership check: in operator inside comparison_operator
        if node.type == "comparison_operator":
            expr = code_bytes[node.start_byte:node.end_byte].decode("utf-8", errors="ignore")
            if " in " in expr:
                # We flag membership checks inside loops as potential O(n) lookups if the target is a list.
                results.append({
                    "type": "membership_check_in_loop",
                    "message": "Membership check ('in') inside a loop. If the container is a list, this is an O(n) scan. Consider using a set or dict for O(1) lookups.",
                    "snippet": expr,
                    "start_line": node.start_point[0] + 1,
                    "end_line": node.end_point[0] + 1
                })

    for child in node.children:
        find_inefficient_ops_ast(child, code_bytes, results, inside_loop or is_loop)

def fallback_regex_parse(content: str) -> list[dict]:
    """
    Regex fallback in case tree-sitter package is unavailable or fails.
    """
    results = []
    lines = content.splitlines()
    
    # 1. Look for simple nested loops (indented loops)
    for i, line in enumerate(lines):
        for_match = re.match(r"^(\s+)(for|while)\s", line)
        if for_match:
            indent = len(for_match.group(1))
            # Scan following lines for a deeper indent loop
            for j in range(i + 1, min(i + 30, len(lines))):
                sub_line = lines[j]
                if not sub_line.strip():
                    continue
                sub_match = re.match(r"^(\s+)(for|while)\s", sub_line)
                if sub_match:
                    sub_indent = len(sub_match.group(1))
                    if sub_indent > indent:
                        snippet = "\n".join(lines[i:j+2])
                        results.append({
                            "type": "nested_loops",
                            "message": "[Fallback Regex] Nested loop detected. Consider vectorization or dict lookups to reduce O(n²) complexity.",
                            "snippet": snippet,
                            "start_line": i + 1,
                            "end_line": j + 2
                        })
                        break
                # If we hit a line with less or equal indent, we left the parent loop
                sub_indent_match = re.match(r"^(\s+)\S", sub_line)
                if sub_indent_match and len(sub_indent_match.group(1)) <= indent:
                    break

    # 2. Look for string concat "+=" inside indented blocks
    for i, line in enumerate(lines):
        if "+=" in line and ("for " in line or any("for " in lines[k] for k in range(max(0, i-5), i))):
            results.append({
                "type": "string_concatenation_in_loop",
                "message": "[Fallback Regex] Potential string concatenation using '+=' in a loop. Consider using list.append() and ''.join().",
                "snippet": line.strip(),
                "start_line": i + 1,
                "end_line": i + 1
            })

    return results

def analyze_python_code(content: str) -> list[dict]:
    """
    Analyzes python code for inefficient AST patterns.
    """
    parser_obj = get_parser()
    if parser_obj == "fallback" or parser_obj is None:
        return fallback_regex_parse(content)

    try:
        code_bytes = content.encode("utf-8")
        tree = parser_obj.parse(code_bytes)
        results = []
        find_nested_loops_ast(tree.root_node, code_bytes, results)
        find_inefficient_ops_ast(tree.root_node, code_bytes, results)
        return results
    except Exception as e:
        print(f"AST Parsing error: {e}. Falling back to regex.")
        return fallback_regex_parse(content)

def analyze_dockerfile(content: str) -> list[dict]:
    """
    Analyze Dockerfile for carbon-heavy or size-heavy configurations.
    """
    results = []
    lines = content.splitlines()
    
    # 1. Base image check (e.g. heavy images)
    for i, line in enumerate(lines):
        from_match = re.match(r"^\s*FROM\s+([\w\-\./:]+)", line, re.IGNORECASE)
        if from_match:
            image = from_match.group(1)
            # Flag if it's a heavy base image when alpine/slim is usually preferred
            if any(pkg in image.lower() for pkg in ["python", "node", "ubuntu", "debian"]) and not any(s in image.lower() for s in ["slim", "alpine", "distroless"]):
                results.append({
                    "type": "heavy_base_image",
                    "message": f"Dockerfile uses heavy base image '{image}'. Switching to a '-slim' or '-alpine' variant reduces transfer bandwidth, storage overhead, and build-time carbon emissions.",
                    "snippet": line,
                    "start_line": i + 1,
                    "end_line": i + 1
                })

    # 2. RUN chain check
    run_lines = []
    for i, line in enumerate(lines):
        if re.match(r"^\s*RUN\s+", line, re.IGNORECASE):
            run_lines.append(i + 1)
            
    if len(run_lines) > 2:
        # If we have multiple individual RUN commands, advise chaining to minimize layers
        snippet = "\n".join([lines[idx-1] for idx in run_lines[:3]])
        results.append({
            "type": "unchained_run_commands",
            "message": "Multiple separate RUN instructions detected. Chaining commands using '&&' and combining updates (e.g. apt-get update && apt-get install -y --no-install-recommends ...) reduces the number of image layers and final image size, saving storage and network CPU cycles.",
            "snippet": snippet,
            "start_line": run_lines[0],
            "end_line": run_lines[-1]
        })

    return results

def analyze_k8s_yaml(content: str) -> list[dict]:
    """
    Analyze Kubernetes manifests for resource limits.
    """
    results = []
    
    # Simple check for missing resource requests/limits in deployment/pod specs
    if "apiVersion:" in content and "kind:" in content:
        # Check if resources blocks are missing
        if "resources:" not in content:
            results.append({
                "type": "missing_resource_limits",
                "message": "Kubernetes manifest is missing container 'resources' configuration. Specifying CPU/Memory requests and limits prevents cluster resources from being over-provisioned or throttled, optimizing cloud efficiency.",
                "snippet": content[:300] + "\n...",
                "start_line": 1,
                "end_line": len(content.splitlines())
            })
            
    return results

def analyze_code(file_path: str, content: str) -> list[dict]:
    """
    Main entrypoint for parsing and analyzing file contents based on file type.
    """
    filename = os.path.basename(file_path).lower()
    
    if filename.endswith(".py"):
        return analyze_python_code(content)
    elif filename == "dockerfile" or filename.endswith(".dockerfile"):
        return analyze_dockerfile(content)
    elif filename.endswith(".yaml") or filename.endswith(".yml"):
        # Check if it looks like a Kubernetes spec
        if "apiversion:" in content.lower() and "kind:" in content.lower():
            return analyze_k8s_yaml(content)
            
    return []
