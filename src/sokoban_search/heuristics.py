"""
Heuristics for Sokoban State Space Search
"""

from typing import List

from sokoban import Occupant, Position, SokobanState


def _manhattan(a: Position, b: Position) -> int:
    """
    Computes the manhattan distance two positions.

    ### Parameters
    a (Position): Position 1
    b (Position): Position 2

    ### Returns
    int: the manhattan distance between a and b
    """
    x1, y1 = a
    x2, y2 = b

    return abs(x1 - x2) + abs(y1 - y2)


def min_manhattan(goals: List[Position], state: SokobanState) -> int:
    """
    Computes the sum of the distance between each box and its closest goal tile.

    ### Parameters
    goals (List[Position]): the list of goals
    state (SokobanState): the current state

    ### Returns
    int: the heuristic
    """
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += min((_manhattan(box, goal) for goal in goals), default=0)

    return h


def sum_manhattan(goals: List[Position], state: SokobanState) -> int:
    """
    Computes the sum of the distance between each box and each goal tile.

    ### Parameters
    goals (List[Position]): the list of goals
    state (SokobanState): the current state

    ### Returns
    int: the heuristic
    """
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += sum((_manhattan(box, goal) for goal in goals), 0)

    return h


def sum_manhattan_hero(goals: List[Position], state: SokobanState) -> int:
    """
    Computes the sum of the distance between each box and each goal tile and
    also adds the distance between the current player position and each box to the
    heuristic.

    ### Parameters
    goals (List[Position]): the list of goals
    state (SokobanState): the current state

    ### Returns
    int: the heuristic
    """
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += sum((_manhattan(box, goal) for goal in goals), 0)
        h += _manhattan(state.hero, box)

    return h


def min_manhattan_hero(goals: List[Position], state: SokobanState) -> int:
    """
    Computes the sum of the distance between each box and its closest goal tile and
    also adds the distance between the current player position and each box to the
    heuristic.

    ### Parameters
    goals (List[Position]): the list of goals
    state (SokobanState): the current state

    ### Returns
    int: the heuristic
    """
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += min((_manhattan(box, goal) for goal in goals), default=0)
        h += _manhattan(state.hero, box)

    return h


def sum_manhattan_hero_penalty(
    goals: List[Position], state: SokobanState, penalty: int = 5
) -> int:
    """
    Computes the sum of the distance between each box and each goal tile and
    also adds the distance between the current player position and each box to the
    heuristic.
    We also add a penalty for each box that is not on a goal tile.

    ### Parameters
    goals (List[Position]): the list of goals
    state (SokobanState): the current state
    penalty (int): penalty for each box that is not on a goal tile

    ### Returns
    int: the heuristic
    """
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += sum((_manhattan(box, goal) for goal in goals), 0)
        h += _manhattan(state.hero, box)
    h += sum(penalty for (j, i) in goals if state.grid[i][j] != Occupant.BLOCK)

    return h


def min_manhattan_hero_penalty(
    goals: List[Position], state: SokobanState, penalty: int = 5
) -> int:
    """
    Computes the sum of the distance between each box and its closest goal tile and
    also adds the distance between the current player position and each box to the
    heuristic.
    We also add a penalty for each box that is not on a goal tile.

    ### Parameters
    goals (List[Position]): the list of goals
    state (SokobanState): the current state
    penalty (int): penalty for each box that is not on a goal tile

    ### Returns
    int: the heuristic
    """
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += min((_manhattan(box, goal) for goal in goals), default=0)
        h += _manhattan(state.hero, box)

    h += sum(penalty for (j, i) in goals if state.grid[i][j] != Occupant.BLOCK)

    return h
