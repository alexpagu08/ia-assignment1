from hlogedu.search.algorithm import Algorithm, Node, Solution
from hlogedu.search.containers import PriorityQueue


class TreeAstar(Algorithm):
    NAME = "my-tree-astar"

    def __init__(self, problem):
        super().__init__(problem)
        self.fringe = PriorityQueue()  # Cola de prioridad por f(n)

    def run(self):
        expand_counter = 0
        roots = [Node(s) for s in self.problem.get_start_states()]

        # Inicializar con los nodos raíz
        for n in roots:
            f_n = n.cost + self.problem.heuristic(n.state)
            self.fringe.push(n, f_n)

        expanded = set()

        while not self.fringe.is_empty():
            n = self.fringe.pop()  # Nodo con menor f(n)

            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)

            if n.state in expanded:
                continue
            expanded.add(n.state)

            expand_counter += 1
            n.expand_order = expand_counter
            n.location = Node.Location.EXPANDED

            # Expandir sucesores ordenados lexicográficamente (solo para consistencia visual)
            for s, a, c in sorted(self.problem.get_successors(n.state), key=lambda x: x[0]):
                ns = Node(s, a, cost=n.cost + c, parent=n)
                n.add_successor(ns)

                if self.problem.is_goal_state(ns.state):
                    return Solution(self.problem, roots, solution_node=ns)

                f_ns = ns.cost + self.problem.heuristic(ns.state)
                self.fringe.push(ns, f_ns)

        # Si no se encuentra solución
        return Solution(self.problem, roots)
