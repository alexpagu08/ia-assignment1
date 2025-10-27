from dataclasses import dataclass

from hlogedu.search.problem import Problem, action, DDRange, Heuristic, DynamicCategorical as DCategorical

@action(DDRange(0, 'num_kiwis'), DCategorical('vertices'))
def move_kiwi(self, state, kiwi_index, dst):
    ...


@dataclass(frozen=True, order=True)
class State:
    kiwis: tuple[str]
    dogs: tuple[str]


# Problem
##############################################################################


class KiwisAndDogsProblem(Problem):
    NAME = "kiwis-and-dogs"

    def __init__(self):
        super().__init__()
        # Assume we only have `nobody(X)` and `somebody(X)` conditions.
        # In case of having more than one condition, these will always be
        # a conjunction and will be separated by a comma.
        self.graph = {
            # A
            ("A", "B"): (3, "nobody(E)"),
            ("A", "C"): (4, ""),
            # B
            ("B", "A"): (3, "nobody(E)"),
            ("B", "C"): (1, ""),
            ("B", "G"): (5, ""),
            # C
            ("C", "B"): (1, ""),
            ("C", "D"): (2, "somebody(E),somebody(G)"),
            # D
            ("D", "C"): (2, "somebody(E),somebody(G)"),
            ("D", "E"): (8, "somebody(A)"),
            ("D", "F"): (3, "somebody(C)"),
            # E
            ("E", "D"): (8, "somebody(A)"),
            ("E", "F"): (5, ""),
            # F
            ("F", "D"): (3, "somebody(C)"),
            # G
            ("G", "F"): (7, ""),
            ("G", "B"): (5, ""),
        }
        self.num_kiwis = 2
        self.num_dogs = 1
        self.vertices = sorted({v for edge in self.graph for v in edge})

    def get_start_states(self):
        return [State(kiwis=("D", "F"), dogs=("C",))]

    def is_goal_state(self, state):
        return all(k == "A" for k in state.kiwis) and all(d == "E" for d in state.dogs)

    def is_valid_state(self, state):
        valid_vertices = {v for edge in self.graph for v in edge}
        return all(k in valid_vertices for k in state.kiwis) and all(d in valid_vertices for d in state.dogs)

    # ACTIONS

    @action(DDRange(0, 'num_kiwis'), DCategorical('vertices'))
    def move_kiwi(self, state, kiwi_idx, dst):
        src = state.kiwis[kiwi_idx]
        edge = (src, dst)
        if edge not in self.graph:
            return None

        cost, cond = self.graph[edge]
        if not self.check_conditions(cond, state):
            return None

        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = dst
        new_state = State(kiwis=tuple(new_kiwis), dogs=state.dogs)
        return (cost, new_state)

    @action(DDRange(0, 'num_dogs'), DCategorical('vertices'))
    def move_dog(self, state, dog_idx, dst):
        src = state.dogs[dog_idx]
        edge = (src, dst)
        if edge not in self.graph:
            return None

        cost, cond = self.graph[edge]
        if not self.check_conditions(cond, state):
            return None

        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = dst
        new_state = State(kiwis=state.kiwis, dogs=tuple(new_dogs))
        return (cost, new_state)

    # AUXILIARY METHODS

    def check_conditions(self, cond_str, state):
        """Return True if all conditions (somebody/nobody) hold in this state."""
        if not cond_str:
            return True

        conds = cond_str.split(",")
        all_positions = set(state.kiwis) | set(state.dogs)

        for cond in conds:
            cond = cond.strip()
            if cond.startswith("somebody("):
                v = cond[len("somebody("):-1]
                if v not in all_positions:
                    return False
            elif cond.startswith("nobody("):
                v = cond[len("nobody("):-1]
                if v in all_positions:
                    return False
        return True
    

@KiwisAndDogsProblem.heuristic
class DistanceToGoalHeuristic(Heuristic):
    NAME = "DistanceToGoalHeuristic"

    def compute(self, state):
        """Suma de distàncies dels kiwis fins a A i del gos fins a E."""
        # Distàncies simples basades en lletres (per aproximar)
        # Només una heurística admissible simple
        target_kiwi = "A"
        target_dog = "E"

        # Si vols millorar-la, pots basar-te en el cost del graf real
        h_kiwis = sum(abs(ord(k) - ord(target_kiwi)) for k in state.kiwis)
        h_dogs = sum(abs(ord(d) - ord(target_dog)) for d in state.dogs)
        return h_kiwis + h_dogs
