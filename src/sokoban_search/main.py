"""
Sokoban State Space Search CLI
"""
from argparse import ArgumentParser
from pathlib import Path
from typing import List
from time import sleep, time_ns

from sokoban_search.heuristics import (
    min_manhattan_hero_reward,
    min_manhattan,
    min_manhattan_hero,
    sum_manhattan_hero_reward,
    sum_manhattan,
    sum_manhattan_hero,
)
from sokoban_search.sokoban import Sokoban

HEURISTICS = {
    "min": min_manhattan,
    "sum": sum_manhattan,
    "sumhero": sum_manhattan_hero,
    "minhero": min_manhattan_hero,
    "sumhero-": sum_manhattan_hero_reward,
    "minhero-": min_manhattan_hero_reward,
}


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
        action="store_false",
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
        choices=["dfs", "bfs", "bestfs"],
    )
    sim_parser.add_argument(
        "--frametime",
        "-f",
        type=float,
        help="take TIME between frames",
        metavar="TIME",
        default=0.25,
    )
    sim_parser.add_argument(
        "--heuristic",
        "-u",
        choices=HEURISTICS.keys(),
        default="sum",
        help="(for bestfs) use HEURISTIC",
        metavar="HEURISTIC",
    )

    bench_parser = subparsers.add_parser("bench", help="benchmark")
    bench_parser.add_argument(
        "--exclude",
        "-x",
        nargs="*",
        choices=["dfs", "bfs", *HEURISTICS.keys()],
        help="exclude EXLC from benchmarking",
        metavar="EXCL",
        default=[],
    )

    return main_parser


def benchmark(sokoban: Sokoban, excl: List[str]):
    sokoban.print()

    print()
    for algo, fn in (("BFS", sokoban.bfs), ("DFS", sokoban.dfs)):
        if algo.lower() in excl:
            print("Skipping", algo)
            continue

        start_time = time_ns()
        states = fn()
        time_taken = time_ns() - start_time

        print(f"{algo:<8}\tSteps: {len(states) - 1}\tTime: {time_taken / 10**9:.4f}s")

    print("\nBestFS")
    for heuristic, h_fn in HEURISTICS.items():
        if heuristic.lower() in excl:
            print("Skipping", heuristic)
            continue
        start_time = time_ns()
        states = sokoban.best_fs(h_fn)
        time_taken = time_ns() - start_time
        print(
            f"{heuristic:<8}\tSteps: {len(states) - 1}\tTime: {time_taken / 10**9:.4f}s"
        )


def main():
    args = get_parser().parse_args()
    sokoban = Sokoban.from_file(args.file, is_alt=args.alt)

    if args.action == "play":
        sokoban.play()
        return

    if args.action == "bench":
        benchmark(sokoban, args.exclude)
        return

    # sim
    heuristic = HEURISTICS[args.heuristic]

    start = time_ns()
    states = {
        "dfs": sokoban.dfs,
        "bfs": lambda: sokoban.bfs(print_depth_info=True),
        "bestfs": lambda: sokoban.best_fs(heuristic),
    }[args.algo]()
    time_taken = time_ns() - start

    for state in states:
        print("\033c", end="")
        sokoban.print(with_state=state)
        sleep(args.frametime)
    print("steps taken:", len(states) - 1)
    print("time taken:", time_taken / 10**9)


if __name__ == "__main__":
    main()
