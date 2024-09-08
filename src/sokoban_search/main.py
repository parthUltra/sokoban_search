from argparse import ArgumentParser
from time import sleep
from pathlib import Path

from sokoban_search.sokoban import Sokoban


def get_parser() -> ArgumentParser:
    main_parser = ArgumentParser(
        prog="sokoban_search",
        description="State Space search for Sokoban",
    )
    main_parser.add_argument(
        "file", type=Path, help="path to the level file", metavar="FILE"
    )
    main_parser.add_argument(
        "--alt",
        help="assume FILE uses alternate representation",
        action="store_true",
    )
    subparsers = main_parser.add_subparsers(dest="action")

    _play_parser = subparsers.add_parser("play", help="play a game of sokoban")

    sim_parser = subparsers.add_parser("sim", help="simulate/state space search")
    sim_parser.add_argument(
        "--algo",
        "-a",
        required=True,
        help="use ALGO for state space search",
        metavar="ALGO",
        choices=["dfs", "bfs"],
    )
    sim_parser.add_argument(
        "--frametime",
        "-f",
        type=float,
        help="take TIME between frames",
        metavar="TIME",
        default=0.25,
    )

    return main_parser


def main():
    args = get_parser().parse_args()
    sokoban = Sokoban.from_file(args.file, is_alt=args.alt)

    if args.action == "play":
        sokoban.play()
        return

    # sim
    if args.algo == "dfs":
        states = sokoban.dfs()
    else:
        states = sokoban.bfs()
    for state in states:
        print("\033c", end="")
        sokoban.print(with_state=state)
        sleep(args.frametime)
    print("steps taken:", len(states))


if __name__ == "__main__":
    main()
