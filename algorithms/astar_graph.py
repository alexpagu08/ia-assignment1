from hlogedu.search.algorithm import Algorithm, Node, Solution
from hlogedu.search.containers import PriorityQueue


class GraphAstar(Algorithm):
    NAME = "my-graph-astar"

    def __init__(self, problem):
        super().__init__(problem)
        self.fringe = PriorityQueue()  

    def run(self):
        expand_counter = 0
        roots = [Node(s) for s in self.problem.get_start_states()]

        cost_so_far = {}
        for n in roots:
            f_n = n.cost + self.problem.heuristic(n.state)
            self.fringe.push(n, f_n)
            cost_so_far[n.state] = n.cost

        while not self.fringe.is_empty():
            n = self.fringe.pop()

            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)

            expand_counter += 1
            n.expand_order = expand_counter
            n.location = Node.Location.EXPANDED

            # Expandir sucesores ordenados lexicográficamente
            for s, a, c in sorted(self.problem.get_successors(n.state), key=lambda x: x[0]):
                new_cost = n.cost + c

                # Solo expandir si no se conoce o se mejora el coste
                if s not in cost_so_far or new_cost < cost_so_far[s]:
                    ns = Node(s, a, cost=new_cost, parent=n)
                    n.add_successor(ns)
                    cost_so_far[s] = new_cost

                    f_ns = new_cost + self.problem.heuristic(s)
                    self.fringe.push(ns, f_ns)

        # No se ha encontrado solución
        return Solution(self.problem, roots)
