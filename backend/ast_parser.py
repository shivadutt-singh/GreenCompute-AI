import tree_sitter_python as tspython
from tree_sitter import Language, Parser

def extract_heavy_logic(raw_code_string: str) -> list[str]:
    """
    Parses the incoming code string into an Abstract Syntax Tree (AST)
    and traverses it to find computationally heavy nodes (specifically,
    for_statement and while_statement).
    
    Returns a list of raw string representations of these isolated heavy nodes.
    """
    if not raw_code_string:
        return []
        
    try:
        # Initialize the Python language and parser
        PY_LANGUAGE = Language(tspython.language())
        parser = Parser(PY_LANGUAGE)
        
        # Parse the raw code (must be in bytes for tree-sitter)
        tree = parser.parse(bytes(raw_code_string, "utf-8"))
        
        heavy_nodes = []
        
        def traverse(node):
            if node.type in ("for_statement", "while_statement"):
                # Extract the text and decode it to a string
                node_text = node.text.decode("utf-8", errors="ignore")
                heavy_nodes.append(node_text)
            
            # Recursively traverse child nodes
            for child in node.children:
                traverse(child)
                
        traverse(tree.root_node)
        return heavy_nodes
    except Exception as e:
        print(f"Error parsing AST: {e}")
        return []
