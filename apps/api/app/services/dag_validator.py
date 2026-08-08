from typing import List, Dict, Any, Set, Tuple

MAX_NODES = 50
MAX_DEPS_PER_NODE = 10
MAX_GRAPH_DEPTH = 20

VALID_NODE_TYPES = {
    "context_retrieval",
    "analysis",
    "tool_call",
    "content_generation",
    "approval",
    "merge",
    "completion"
}

class DAGValidationError(Exception):
    pass

def validate_dag_plan(nodes: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    errors: List[str] = []

    if len(nodes) > MAX_NODES:
        errors.append(f"Plan exceeds maximum node count limit ({len(nodes)} > {MAX_NODES}).")
        return False, errors

    node_keys: Set[str] = set()
    node_map: Dict[str, Dict[str, Any]] = {}

    for node in nodes:
        key = node.get("node_key")
        if not key:
            errors.append("All plan nodes must have a non-empty 'node_key'.")
            continue
        if key in node_keys:
            errors.append(f"Duplicate node key '{key}' detected.")
        node_keys.add(key)
        node_map[key] = node

        ntype = node.get("type", "tool_call")
        if ntype not in VALID_NODE_TYPES:
            errors.append(f"Node '{key}' has invalid node type '{ntype}'.")

        deps = node.get("dependencies", [])
        if len(deps) > MAX_DEPS_PER_NODE:
            errors.append(f"Node '{key}' exceeds maximum dependency count ({len(deps)} > {MAX_DEPS_PER_NODE}).")

    if errors:
        return False, errors

    # Check dependency references & self-dependencies
    for key, node in node_map.items():
        deps = node.get("dependencies", [])
        for dep in deps:
            if dep == key:
                errors.append(f"Self-dependency detected on node '{key}'.")
            if dep not in node_map:
                errors.append(f"Node '{key}' references non-existent dependency '{dep}'.")

    if errors:
        return False, errors

    # Cycle Detection & Depth Calculation via DFS
    visited: Set[str] = set()
    rec_stack: Set[str] = set()
    depth_cache: Dict[str, int] = {}

    def get_node_depth(curr: str) -> int:
        if curr in rec_stack:
            raise DAGValidationError(f"Cycle detected involving node '{curr}'.")
        if curr in depth_cache:
            return depth_cache[curr]

        rec_stack.add(curr)
        deps = node_map[curr].get("dependencies", [])
        max_dep_d = 0
        for dep in deps:
            d = get_node_depth(dep)
            if d > max_dep_d:
                max_dep_d = d

        rec_stack.remove(curr)
        depth_cache[curr] = max_dep_d + 1
        return depth_cache[curr]

    max_graph_d = 0
    try:
        for k in node_map:
            d = get_node_depth(k)
            if d > max_graph_d:
                max_graph_d = d
    except DAGValidationError as exc:
        errors.append(str(exc))
        return False, errors

    if max_graph_d > MAX_GRAPH_DEPTH:
        errors.append(f"Plan graph depth exceeds maximum limit ({max_graph_d} > {MAX_GRAPH_DEPTH}).")
        return False, errors

    return True, []
