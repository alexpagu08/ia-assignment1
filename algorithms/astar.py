from queue import PriorityQueue

def a_star(start, goal, h, neighbors):
    """
    A* Search Algorithm
    Finds the lowest-cost path from start to goal using f(n) = g(n) + h(n).
    
    :param start: Initial node
    :param goal: Goal node
    :param h: Heuristic function h(node)
    :param neighbors: Function neighbors(node) -> list of (neighbor, cost)
    :return: (path, total_cost)
    """

    open_set = PriorityQueue()
    open_set.put((0, start))
    open_set_nodes = {start}  # per verificació ràpida

    came_from = {}
    g_score = {start: 0}
    f_score = {start: h(start)}
    closed_set = set()

    while not open_set.empty():
        current = open_set.get()[1]
        open_set_nodes.remove(current)

        if current == goal:
            return reconstruct_path(came_from, current), g_score[current]

        closed_set.add(current)

        for neighbor, cost in neighbors(current):
            if neighbor in closed_set:
                continue

            tentative_g = g_score[current] + cost
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + h(neighbor)

                if neighbor not in open_set_nodes:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_nodes.add(neighbor)

    return [], float('inf')


def reconstruct_path(came_from, current):
    """Reconstrueix el camí òptim a partir del diccionari came_from."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


if __name__ == "__main__":
    # Definició del grafo com diccionari
    graph = {
        "A": [("B", 1), ("E", 3)],
        "B": [("C", 1), ("E", 1)],
        "C": [("D", 1)],
        "D": [],
        "E": [("F", 1)],
        "F": [("D", 1)]
    }

    def neighbors(node):
        return graph.get(node, [])

    # Heurística admissible: distància estimada al goal (D)
    h_values = {"A": 3, "B": 2, "C": 1, "D": 0, "E": 2, "F": 1}

    def h(node):
        return h_values.get(node, 0)

    path, cost = a_star("A", "D", h, neighbors)
    print("✅ Path found:", path)
    print("💰 Total cost:", cost)
