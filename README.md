# Sokoban Search
State Space search for Sokoban

We used [`uv`](https://github.com/astral-sh/uv) to run the project during the development and would recommend you use `uv` to run the project.

To check the usage run `uv run src/sokoban_search/main.py --help` or `python3 src/sokoban_search/main.py --help`.

We have also provided some example levels in the `levels/` folder.

### Dependencies
[`pynput`](https://pypi.org/project/pynput/) is the only dependency and is used for taking the keyboard input when playing a game of sokoban.

### Example Usage
- `uv run src/sokoban_search/main.py levels/trivial.txt play`
  - play the `trivial.txt` level.
- `uv run src/sokoban_search/main.py levels/level_01.txt sim --algo bestfs --heuristic sum`
  - uses the best first search algorithm on `level_01.txt` to find a path to the goal and then shows it on the terminal.
  - you can use the `--frametime <time>` option to change the amount of time spent on showing one frame.
- `uv run src/sokoban_search/main.py levels/level_03.txt bench`
  - will benchmark all the algorithms and heuristics on `level_03.txt` and print the results.
  - you can exclude certain heuristics or algorithms by using the `-x <excl_1> <excl_2>...` flag

If you do not use `uv`, replace `uv run` with `python3` and everything should work the same.
