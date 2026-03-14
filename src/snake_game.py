from __future__ import annotations

import argparse
import random
from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable, Tuple

Pos = Tuple[int, int]
DIRS = {
    "W": (-1, 0),
    "S": (1, 0),
    "A": (0, -1),
    "D": (0, 1),
}
OPPOSITE = {"W": "S", "S": "W", "A": "D", "D": "A"}


@dataclass
class GameState:
    width: int
    height: int
    snake: Deque[Pos]
    direction: str
    food: Pos
    score: int = 0
    game_over: bool = False


def _spawn_food(width: int, height: int, snake: Iterable[Pos], rng: random.Random) -> Pos:
    occupied = set(snake)
    free = [(r, c) for r in range(height) for c in range(width) if (r, c) not in occupied]
    if not free:
        return (-1, -1)
    return rng.choice(free)


def create_game(width: int = 12, height: int = 8, seed: int | None = None) -> GameState:
    rng = random.Random(seed)
    center = (height // 2, width // 2)
    snake = deque([center, (center[0], center[1] - 1), (center[0], center[1] - 2)])
    food = _spawn_food(width, height, snake, rng)
    return GameState(width=width, height=height, snake=snake, direction="D", food=food)


def step(state: GameState, direction: str | None = None, seed: int | None = None) -> GameState:
    if state.game_over:
        return state

    rng = random.Random(seed)
    d = state.direction
    if direction:
        direction = direction.upper()
        if direction in DIRS and direction != OPPOSITE[d]:
            d = direction

    dr, dc = DIRS[d]
    head_r, head_c = state.snake[0]
    new_head = (head_r + dr, head_c + dc)

    if not (0 <= new_head[0] < state.height and 0 <= new_head[1] < state.width):
        state.game_over = True
        return state

    body = set(state.snake)
    tail = state.snake[-1]
    will_grow = new_head == state.food
    if not will_grow:
        body.remove(tail)
    if new_head in body:
        state.game_over = True
        return state

    state.snake.appendleft(new_head)
    if will_grow:
        state.score += 1
        state.food = _spawn_food(state.width, state.height, state.snake, rng)
        if state.food == (-1, -1):
            state.game_over = True
    else:
        state.snake.pop()

    state.direction = d
    return state


def render(state: GameState) -> str:
    board = [["." for _ in range(state.width)] for _ in range(state.height)]
    if state.food != (-1, -1):
        fr, fc = state.food
        board[fr][fc] = "*"
    for i, (r, c) in enumerate(state.snake):
        board[r][c] = "O" if i == 0 else "o"
    lines = ["".join(row) for row in board]
    lines.append(f"Score: {state.score}")
    if state.game_over:
        lines.append("GAME OVER")
    return "\n".join(lines)


def run_scripted(moves: str, width: int = 12, height: int = 8, seed: int | None = None) -> GameState:
    state = create_game(width=width, height=height, seed=seed)
    for i, move in enumerate(moves.upper()):
        if state.game_over:
            break
        if move not in DIRS:
            continue
        step(state, move, seed=None if seed is None else seed + i + 1)
    return state


def run_cli(width: int = 12, height: int = 8, seed: int | None = None) -> None:
    print("Snake (WASD + Enter, q zum Beenden)")
    state = create_game(width=width, height=height, seed=seed)
    print(render(state))
    while not state.game_over:
        cmd = input("Move [W/A/S/D, Enter=weiter]: ").strip().upper()
        if cmd == "Q":
            print("Abbruch.")
            return
        step(state, cmd if cmd else None)
        print(render(state))
    print("Final Score:", state.score)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal Snake in Python")
    parser.add_argument("--width", type=int, default=12, help="Spielfeldbreite")
    parser.add_argument("--height", type=int, default=8, help="Spielfeldhöhe")
    parser.add_argument("--seed", type=int, default=None, help="RNG-Seed")
    parser.add_argument(
        "--moves",
        type=str,
        default=None,
        help="Scripted Moves, z.B. WWAASD (für non-interactive Runs)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.width < 5 or args.height < 5:
        parser.error("width/height müssen jeweils >= 5 sein")

    if args.moves is not None:
        state = run_scripted(args.moves, width=args.width, height=args.height, seed=args.seed)
        print(render(state))
        print("Final Score:", state.score)
        return 0 if not state.game_over else 1

    run_cli(width=args.width, height=args.height, seed=args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
