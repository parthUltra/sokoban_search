from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Self, Tuple

import pynput.keyboard as kb

# x, y coordinates of a hero / goal
Position = Tuple[int, int]


"""
Display representations of different grid occupants and states.
"""
DISPLAY_CHARS: Dict[str, str] = {
    " ": "  ",
    "H": "🧍",
    "W": "🧱",
    "G": "⭐",
    "B": "📦",
    "GB": "❎",
    "GH": "🧔",
}


class Occupant(Enum):
    """
    Possible occupant's of the Sokoban grid.
    The Hero is not included as it is stored separately.
    """
    EMPTY = " "
    BLOCK = "B"
    WALL = "W"


class Direction(Enum):
    """
    Direction in which the hero can move.
    """
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


@dataclass
class SokobanState:
    """
    The state of the Sokoban grid at one instance.

    ### Fields:
    grid (List[List[Occupant]]): A matrix of Occupants (WALL, BLOCK, EMPTY)
    """
    grid: List[List[Occupant]]
    hero: Position

    def is_legal_pos(self, new_x: int, new_y: int) -> bool:
        """
        Check if (new_x, new_y) is a legal position on the grid.

        ### Parameters
        new_x (int): x-coordinate
        new_y (int): y-coordinate

        ### Returns
        bool: True if (new_x, new_y) is valid, False otherwise
        """
        return 0 <= new_x < len(self.grid[0]) and 0 <= new_y < len(self.grid)

    def can_push_to(self, push_x, push_y) -> bool:
        """
        Check if (push_x, push_y) is a legal position on the grid to which a box can be pushed.

        ### Parameters
        push_x (int): x-coordinate
        push_y (int): y-coordinate

        ### Returns
        bool: True if (push_x, push_y) is valid, False otherwise
        """
        return (
            self.is_legal_pos(push_x, push_y)
            and self.grid[push_y][push_x] == Occupant.EMPTY
        )

    def move(self, direction: Direction) -> Self:
        """
        Generate a new state which is the result of moving the hero in the `direction`

        ### Parameters
        direction (Direction): the direction to move in (UP, DOWN, LEFT, RIGHT)

        ### Returns
        SokobanState: SokobanState which is the result of moving in direction
        """
        new_state = deepcopy(self)
        hero_x, hero_y = new_state.hero
        dx, dy = direction.value
        new_x, new_y = hero_x + dx, hero_y + dy

        # check if the new position is within the grid
        if not new_state.is_legal_pos(new_x, new_y):
            return new_state

        match new_state.grid[new_y][new_x]:
            case Occupant.EMPTY:
                # move the hero
                new_state.hero = (new_x, new_y)
            case Occupant.BLOCK:
                # check if we can push the block
                push_x, push_y = new_x + dx, new_y + dy
                if new_state.can_push_to(push_x, push_y):
                    # push the block
                    new_state.grid[push_y][push_x] = Occupant.BLOCK
                    new_state.grid[new_y][new_x] = Occupant.EMPTY
                    new_state.hero = (new_x, new_y)
            case Occupant.WALL:
                # can't move into a wall, return the unchanged state
                pass

        return new_state


class Sokoban:
    """
    The main Sokoban class which handles most of the game logic and the state space search.
    """
    def __init__(self, state: SokobanState, goals: List[Position]):
        """
        ### Parameters
        state (SokobanState): starting state of the grid
        goals (List[Position]): list of goals (x,y coordinates)
        """
        self.state = state
        self.goals = goals

    def print(self, with_state: SokobanState | None = None):
        """
        Print the current game state. Is used when playing the game too.

        ### Parameters
        with_state (SokobanState | None): print `with_state` instead of `self.state` if provided
        """
        state = self.state
        if with_state is not None:
            state = with_state

        disp_mat = [[occupant.value for occupant in row] for row in state.grid]

        hero_x, hero_y = state.hero

        for goal_x, goal_y in self.goals:
            match state.grid[goal_y][goal_x]:
                case Occupant.EMPTY:
                    disp_mat[goal_y][goal_x] = "G"
                case Occupant.BLOCK:
                    disp_mat[goal_y][goal_x] = "GB"

        if state.grid[hero_y][hero_x] == Occupant.EMPTY:
            disp_mat[hero_y][hero_x] = "H"

        if state.hero in self.goals:
            disp_mat[hero_y][hero_x] = "GH"

        for row in disp_mat:
            for char in row:
                print(DISPLAY_CHARS[char], end="")
            print()

    def play(self):
        """
        Play the game of Sokoban.
        """
        print("Use arrow keys to move. Press 'q' to quit.")
        self.print()

        def on_press(key):
            try:
                if key == kb.Key.up:
                    self.state = self.state.move(Direction.UP)
                elif key == kb.Key.down:
                    self.state = self.state.move(Direction.DOWN)
                elif key == kb.Key.left:
                    self.state = self.state.move(Direction.LEFT)
                elif key == kb.Key.right:
                    self.state = self.state.move(Direction.RIGHT)
                elif key.char == "q":
                    return False

                print("\033c", end="")
                self.print()

                if self.goal_test(self.state):
                    print("Congratulations! You solved the puzzle!")
                    return False
            except AttributeError:
                pass

        with kb.Listener(on_press=on_press) as listener:
            listener.join()

    def sim(self):
        """
        Simulate a game of sokoban.
        The user has to enter the state to move to after each move gen.
        """
        while not self.goal_test(self.state):
            states = self.move_gen(self.state)
            for i, state in enumerate(states):
                print("STATE", i)
                self.print(with_state=state)

            next_state = int(input("Select next state: "))
            self.state = states[next_state]

    def goal_test(self, state: SokobanState) -> bool:
        """
        Check if the given `state` is a goal state.

        ### Parameters
        state (SokobanState): the state which we have to check

        ### Returns
        bool: True if `state` is a goal state, False otherwise
        """
        return all(state.grid[y][x] == Occupant.BLOCK for (x, y) in self.goals)

    def move_gen(self, state: SokobanState) -> List[SokobanState]:
        """
        Generate all possible states that are neighbors of `state`

        ### Parameters
        state (SokobanState): state to generate the neighbors for

        ### Returns
        List[SokobanState]: list of all possible neighbors of `state`
        """
        states = []
        for dir in Direction:
            new_state = state.move(dir)
            if new_state not in states and new_state != state:
                states.append(new_state)

        return states

    @staticmethod
    def _parse_position(pair: str) -> Position:
        [x, y] = pair.split(",")
        return (int(x), int(y))

    @staticmethod
    def _parse_goals(line: str) -> List[Position]:
        return [Sokoban._parse_position(pair) for pair in line.split()]

    @classmethod
    def from_file(cls, filepath: Path) -> Self:
        """
        Parse a Sokoban puzzle from a file.

        ### Parameters
        filepath (Path): The path to the puzzle file
        
        ### Returns
        Sokoban: The parsed sokoban puzzle
        """
        if not (filepath.exists() and filepath.is_file()):
            raise FileNotFoundError(f"{filepath} not found or is not a file")

        with open(filepath, "r") as f:
            raw_data = f.read().splitlines()

        hero = Sokoban._parse_position(raw_data.pop())
        goals = Sokoban._parse_goals(raw_data.pop())
        # assuming the grid only has the data for walls and blocks
        grid = [[Occupant(c.upper()) for c in line] for line in raw_data]

        return cls(SokobanState(grid, hero), goals)
