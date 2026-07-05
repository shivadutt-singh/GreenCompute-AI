import sys
import os

# Adjust path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ast_parser import extract_heavy_logic

def run_tests():
    print("Running AST Parser unit tests...")

    # Test 1: Simple For Loop
    code_1 = """
def simple_loop(n):
    result = 0
    for i in range(n):
        result += i
    return result
"""
    print("\n--- Test 1: Simple For Loop ---")
    nodes_1 = extract_heavy_logic(code_1)
    for idx, node in enumerate(nodes_1, 1):
        print(f"Node {idx}:\n{node}")
    assert len(nodes_1) == 1
    assert "for i in range(n):" in nodes_1[0]

    # Test 2: Nested Loops
    code_2 = """
def nested_loops(matrix):
    total = 0
    for row in matrix:
        for val in row:
            total += val
    return total
"""
    print("\n--- Test 2: Nested Loops ---")
    nodes_2 = extract_heavy_logic(code_2)
    for idx, node in enumerate(nodes_2, 1):
        print(f"Node {idx}:\n{node}")
    # Nested loops should return 2 nodes (outer for_statement and inner for_statement)
    assert len(nodes_2) == 2
    assert "for row in matrix:" in nodes_2[0]
    assert "for val in row:" in nodes_2[1]

    # Test 3: While Loop
    code_3 = """
def while_loop(limit):
    count = 0
    while count < limit:
        count += 1
    return count
"""
    print("\n--- Test 3: While Loop ---")
    nodes_3 = extract_heavy_logic(code_3)
    for idx, node in enumerate(nodes_3, 1):
        print(f"Node {idx}:\n{node}")
    assert len(nodes_3) == 1
    assert "while count < limit:" in nodes_3[0]

    # Test 4: No Loops
    code_4 = """
def no_loops(a, b):
    if a > b:
        return a
    return b
"""
    print("\n--- Test 4: No Loops ---")
    nodes_4 = extract_heavy_logic(code_4)
    print(f"Extracted: {nodes_4}")
    assert len(nodes_4) == 0

    print("\nAll unit tests passed successfully!")

if __name__ == "__main__":
    run_tests()
