"""Utility functions for BRAID-DSPy integration."""

from typing import Dict, List, Any, Optional
import re


def extract_mermaid_code(text: str) -> Optional[str]:
    """
    Extract Mermaid diagram code from text that may contain markdown code blocks.

    Args:
        text: Text that may contain Mermaid code in markdown code blocks

    Returns:
        Extracted Mermaid code or None if not found
    """
    # Try to find mermaid code block
    mermaid_pattern = r"```(?:mermaid)?\s*\n(.*?)```"
    match = re.search(mermaid_pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # If no code block, check if it's already mermaid code
    if text.strip().startswith(("graph", "flowchart", "sequenceDiagram")):
        return text.strip()

    return None


def validate_mermaid_syntax(mermaid_code: str) -> bool:
    """
    Basic validation of Mermaid syntax.

    Args:
        mermaid_code: Mermaid diagram code to validate

    Returns:
        True if syntax appears valid, False otherwise
    """
    if not mermaid_code:
        return False

    # Check for basic flowchart/graph declaration
    if not re.search(r"^\s*(graph|flowchart)", mermaid_code, re.MULTILINE):
        return False

    # Check for at least one node definition
    if not re.search(r"\w+\s*\[.*?\]|\w+\s*\(.*?\)|\w+\s*\{.*?\}|\w+\s*-->|\w+\s*--", mermaid_code):
        return False

    return True


def parse_grd_structure(mermaid_code: str) -> Dict[str, Any]:
    """
    Parse Mermaid code to extract GRD structure information.

    Args:
        mermaid_code: Mermaid diagram code

    Returns:
        Dictionary containing structure information (nodes, edges, etc.)
    """
    nodes = []
    edges = []

    # Extract node definitions
    node_pattern = r"(\w+)\s*\[(.*?)\]|(\w+)\s*\((.*?)\)|(\w+)\s*\{(.*?)\}"
    for match in re.finditer(node_pattern, mermaid_code):
        node_id = match.group(1) or match.group(3) or match.group(5)
        node_label = match.group(2) or match.group(4) or match.group(6)
        nodes.append({"id": node_id, "label": node_label.strip()})

    # Extract edges
    edge_pattern = r"(\w+)\s*(-->|--)\s*(\w+)"
    for match in re.finditer(edge_pattern, mermaid_code):
        edges.append(
            {
                "from": match.group(1),
                "to": match.group(3),
                "type": "directed" if "-->" in match.group(2) else "undirected",
            }
        )

    return {"nodes": nodes, "edges": edges, "node_count": len(nodes), "edge_count": len(edges)}


def format_grd_prompt(problem: str, examples: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Format a prompt for GRD generation.

    Args:
        problem: The problem to solve
        examples: Optional few-shot examples

    Returns:
        Formatted prompt string
    """
    prompt = """You are tasked with solving a problem using structured reasoning.

First, create a Guided Reasoning Diagram (GRD) in Mermaid flowchart format that maps out the solution steps.
Then, execute the plan step by step.

Problem: {problem}

Generate a Mermaid flowchart that shows:
1. Problem analysis
2. Solution steps
3. Decision points (if any)
4. Final answer derivation

Use this format:
```mermaid
flowchart TD
    Start[Problem Analysis] --> Step1[Step 1 Description]
    Step1 --> Step2[Step 2 Description]
    Step2 --> Answer[Final Answer]
```
"""

    if examples:
        prompt += "\n\nExamples:\n"
        for i, example in enumerate(examples, 1):
            prompt += f"\nExample {i}:\n"
            prompt += f"Problem: {example.get('problem', '')}\n"
            prompt += f"GRD:\n{example.get('grd', '')}\n"

    return prompt.format(problem=problem)
