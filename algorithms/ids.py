# algorithms/ids.py
# --------------------------------------------
# Implementació de l'algorisme Iterative Deepening Search (IDS)
# amb un petit exemple per provar-lo directament.
# --------------------------------------------

def ids(start, is_goal_state, get_successors, max_depth=10):
    """Iterative Deepening Search (IDS)"""
    for depth in range(max_depth):
        print(f"🔍 Depth limit = {depth}")
        result = dfs_limited(start, is_goal_state, get_successors, depth)
        if result is not None and result != "cutoff":
            return result
    return None


def dfs_limited(node, is_goal_state, get_successors, limit):
    """Depth-Limited Search (DLS)"""
    print(f"  Exploring {node} (limit={limit})")

    if is_goal_state(node):
        return node
    elif limit == 0:
        return "cutoff"

    cutoff_occurred = False
    for successor in get_successors(node):
        result = dfs_limited(successor, is_goal_state, get_successors, limit - 1)
        if result == "cutoff":
            cutoff_occurred = True
        elif result is not None:
            return result
    return "cutoff" if cutoff_occurred else None


# ===============================
# === Exemple de prova ==========
# ===============================
if __name__ == "__main__":
    # Grafo simple de prova
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["E"],
        "D": ["G"],
        "E": [],
        "G": []
    }

    def get_successors(node):
        """Devuelve los sucesores del nodo."""
        return graph.get(node, [])

    def is_goal_state(node):
        """Verifica si el nodo es el objetivo."""
        return node == "G"

    start = "A"
    print(f"🚀 Starting IDS from {start} to goal 'G'\n")
    result = ids(start, is_goal_state, get_successors, max_depth=5)

    if result:
        print(f"\n✅ Goal found: {result}")
    else:
        print("\n❌ Goal not found within depth limit.")
