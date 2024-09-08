"""
Heuristics for Sokoban State Space Search
"""

from typing import List

from sokoban_search.sokoban import Occupant, Position, SokobanState


def _manhattan(a: Position, b: Position) -> int:
    """
    Compute the manhattan distance two positions

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
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += min((_manhattan(box, goal) for goal in goals), default=0)

    return h


def sum_manhattan(goals: List[Position], state: SokobanState) -> int:
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += sum((_manhattan(box, goal) for goal in goals), 0)

    return h


def sum_manhattan_hero(goals: List[Position], state: SokobanState) -> int:
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += sum((_manhattan(box, goal) for goal in goals), 0)
        h += _manhattan(state.hero, box)

    return h


def min_manhattan_hero(goals: List[Position], state: SokobanState) -> int:
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += min((_manhattan(box, goal) for goal in goals), default=0)
        h += _manhattan(state.hero, box)

    return h


def sum_manhattan_hero_reward(
    goals: List[Position], state: SokobanState
) -> int:
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += sum((_manhattan(box, goal) for goal in goals), 0)
        h += _manhattan(state.hero, box)
    h -= sum(5 for (j, i) in goals if state.grid[i][j] == Occupant.BLOCK)

    return h


def min_manhattan_hero_reward(
    goals: List[Position], state: SokobanState
) -> int:
    boxes = state.box_positions()
    h = 0
    for box in boxes:
        h += min((_manhattan(box, goal) for goal in goals), default=0)
        h += _manhattan(state.hero, box)
    h -= sum(5 for (j, i) in goals if state.grid[i][j] == Occupant.BLOCK)

    return h
