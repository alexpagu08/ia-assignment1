import pygame
import random

from typing import Any

from hlogedu.search.common import ClassParameter
from hlogedu.search.problem import Problem, action, DDRange, Heuristic
from hlogedu.search.visualizer import SolutionVisualizer

# Visualization (you do not have to modify this!)
##############################################################################


class NQueensVisualizer(SolutionVisualizer):
    """Pygame-based visualizer for the N-Queens problem."""

    def draw_state(self, state: Any) -> None:
        """Draw a board with queens placed according to the given state."""
        n = self.problem.n_queens
        cell_size = self.get_cell_size()

        # Clear screen
        self.screen.fill((255, 255, 255))

        # Draw chessboard
        for row in range(n):
            for col in range(n):
                rect = pygame.Rect(
                    col * cell_size, row * cell_size, cell_size, cell_size
                )
                color = (240, 217, 181) if (row + col) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(self.screen, color, rect)

        # Draw queens
        for col, row in enumerate(state):
            center = (
                col * cell_size + cell_size // 2,
                row * cell_size + cell_size // 2,
            )
            radius = cell_size // 3
            pygame.draw.circle(self.screen, (200, 0, 0), center, radius)

        pygame.display.flip()

    def animate_transition(self, state: Any, action: Any, new_state: Any) -> None:
        """Smoothly animate the transition from one state to another."""
        n = self.problem.n_queens
        cell_size = self.get_cell_size()
        delay = self.get_delay()

        # figure out which queens moved
        moved = [
            (col, state[col], new_state[col])
            for col in range(n)
            if state[col] != new_state[col]
        ]

        if not moved:
            return  # nothing changed

        # number of steps in animation
        steps = 10

        for step in range(steps + 1):
            # interpolate state
            intermediate = list(state)
            for col, old_row, new_row in moved:
                interp_row = old_row + (new_row - old_row) * (step / steps)
                intermediate[col] = interp_row

            # draw interpolated state
            self.draw_interpolated_state(intermediate)
            pygame.time.delay(delay // max(1, steps))

        # final draw (ensure exact new state)
        self.draw_state(new_state)

    def draw_interpolated_state(self, state) -> None:
        """Draw state where row positions can be floats (for animation)."""
        n = self.problem.n_queens
        cell_size = self.get_cell_size()

        # Draw board
        self.screen.fill((255, 255, 255))
        for row in range(n):
            for col in range(n):
                rect = pygame.Rect(
                    col * cell_size, row * cell_size, cell_size, cell_size
                )
                color = (240, 217, 181) if (row + col) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(self.screen, color, rect)

        # Draw queens (supports float rows)
        for col, row in enumerate(state):
            center = (
                col * cell_size + cell_size // 2,
                int(row * cell_size + cell_size // 2),
            )
            radius = cell_size // 3
            pygame.draw.circle(self.screen, (200, 0, 0), center, radius)

        pygame.display.flip()


# Problem
##############################################################################


class NQueensIterativeRepair(Problem):
    """N-Queens problem

    This problem consists in placing n non-attacking queens on an
    nxn chessboard.

    This implementations starts with an nxn chessboard that already
    contains N queens on it, and tries to solve the problem by iteratively
    moving the queens to different possitions
    """

    NAME = "NQueensIR"
    VISUALIZER = NQueensVisualizer
    PARAMS = [
        ClassParameter(
            name="n_queens", type=int, default="8", help="Number of queens."
        ),
        ClassParameter(name="seed", type=int, default="123456", help="Random seed."),
    ]

    def __init__(self, n_queens: int = 8, seed: int = 123456):
        super().__init__()
        self.n_queens = n_queens
        self.seed = seed
        random.seed(self.seed)

    def get_start_states(self):
        return [tuple(random.randint(0, self.n_queens - 1) for _ in range(self.n_queens))]


    def is_goal_state(self, state):
        n = self.n_queens
        # Comprova si dues reines comparteixen fila o diagonal
        for c1 in range(n):
            for c2 in range(c1 + 1, n):
                r1, r2 = state[c1], state[c2]
                if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                    return False
        return True


    def is_valid_state(self, state):
        return len(state) == self.n_queens and all(0 <= r < self.n_queens for r in state)



    # Actions go here...

    @action(DDRange(0, 'n_queens'), DDRange(0, 'n_queens'))
    def move_queen(self, state, column, new_row):
        old_row = state[column]
        if old_row == new_row:
            return None  # no hay movimiento
        cost = abs(old_row - new_row)
        new_state = list(state)
        new_state[column] = new_row
        return cost, tuple(new_state)


# Heuristic
##############################################################################

@NQueensIterativeRepair.heuristic
class RepairHeuristic(Heuristic):
    """
    h(n) = tamaño de un apareamiento (matching) greedy en el grafo de conflictos.
    - Nodos: columnas (reinas).
    - Arista (i,j) si las reinas en columnas i y j se atacan (misma fila o diagonal).
    - Cada arista del matching exige >= 1 unidad de movimiento de alguna de las dos reinas.
    => h(n) es cota inferior del coste real: **admisible** (y consistente).
    """

    def compute(self, state):
        n = len(state)
        # 1) aristas de conflicto
        edges = []
        for c1 in range(n):
            r1 = state[c1]
            for c2 in range(c1 + 1, n):
                r2 = state[c2]
                if r1 == r2 or abs(r1 - r2) == abs(c1 - c2):
                    edges.append((c1, c2))

        if not edges:
            return 0

        # 2) matching greedy (parejas disjuntas)
        matched = set()
        msize = 0
        for u, v in edges:
            if u not in matched and v not in matched:
                matched.add(u); matched.add(v)
                msize += 1
        return msize

