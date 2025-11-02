from hlogedu.search.algorithm import Algorithm, Node, Solution
from hlogedu.search.containers import Stack


class TreeIds(Algorithm):
    NAME = "my-tree-ids"

    def __init__(self, problem):
        super().__init__(problem)
        self.fringe = Stack()  

    def run(self):
        """Iterative Deepening Search (IDS)."""
        roots = [Node(s) for s in self.problem.get_start_states()]

        # Caso trivial: estado inicial ya es objetivo
        for n in roots:
            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)

        limit = 0
        while True:
            result = self._dls(roots, limit)
            if result != "cutoff":
                return result
            limit += 1

    def _dls(self, roots, limit):
        """Depth-Limited Search (DLS)."""
        
        self.fringe = Stack()
        expanded = set()
        expand_counter = 0
        cutoff = False

        # Inicializar pila con raíces
        for n in roots:
            self.fringe.push(n)

        while not self.fringe.is_empty():
            n = self.fringe.pop()

            # Si hemos alcanzado el límite → marcar corte
            if n.depth == limit:
                cutoff = True
                continue

            # Marcar nodo expandido
            expand_counter += 1
            n.expand_order = expand_counter
            n.location = Node.Location.EXPANDED
            expanded.add(n.state)

            # Generar sucesores ordenados lexicográficamente
            for s, a, c in sorted(self.problem.get_successors(n.state), key=lambda x: x[0]):
                ns = Node(s, a, cost=n.cost + c, parent=n)
                n.add_successor(ns)

                if self.problem.is_goal_state(ns.state):
                    return Solution(self.problem, roots, solution_node=ns)

                if ns.state not in expanded:
                    self.fringe.push(ns)

        # Resultado según haya corte o fallo
        if cutoff:
            return "cutoff"
        else:
            return Solution(self.problem, roots)
