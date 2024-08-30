from argparse import ArgumentParser
from pathlib import Path

from sokoban_search.sokoban import Sokoban


def get_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="sokoban_search",
        description="State Space search for Sokoban",
    )
    parser.add_argument(
        "action",
        type=lambda x: x.lower(),
        choices=["play", "sim"],
        help="play or simulate?",
        metavar="ACTION",
    )
    parser.add_argument(
        "file", type=Path, help="path to the level file", metavar="FILE"
    )

    return parser


def main():
    args = get_parser().parse_args()
    sokoban = Sokoban.from_file(args.file)
    match args.action:
        case "play":
            sokoban.play()
        case "sim":
            sokoban.sim()
        case eh:
            raise ValueError(f"{eh} eh?")


if __name__ == "__main__":
    main()
