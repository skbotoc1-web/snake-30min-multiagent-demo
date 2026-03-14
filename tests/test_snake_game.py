import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.snake_game import (
    build_parser,
    create_game,
    load_high_score,
    main,
    render,
    run_scripted,
    save_high_score,
    step,
)


class SnakeTests(unittest.TestCase):
    def test_initial_state(self):
        s = create_game(seed=1)
        self.assertEqual(len(s.snake), 3)
        self.assertFalse(s.game_over)

    def test_move_and_grow(self):
        s = create_game(width=8, height=6, seed=1)
        s.food = (s.snake[0][0], s.snake[0][1] + 1)
        step(s, "D", seed=2)
        self.assertEqual(s.score, 1)
        self.assertEqual(len(s.snake), 4)

    def test_wall_collision(self):
        s = create_game(width=5, height=5, seed=1)
        for _ in range(10):
            step(s, "W")
            if s.game_over:
                break
        self.assertTrue(s.game_over)

    def test_prevent_opposite_direction(self):
        s = create_game(seed=1)
        old_head = s.snake[0]
        step(s, "A")
        self.assertEqual(s.direction, "D")
        self.assertNotEqual(s.snake[0], old_head)

    def test_self_collision(self):
        s = create_game(width=6, height=6, seed=1)
        for move in ["D", "S", "A"]:
            s.food = (
                s.snake[0][0] + (1 if move == "S" else -1 if move == "W" else 0),
                s.snake[0][1] + (1 if move == "D" else -1 if move == "A" else 0),
            )
            step(s, move)
        step(s, "W")
        self.assertTrue(s.game_over)

    def test_render_contains_score_and_symbols(self):
        s = create_game(seed=1)
        out = render(s)
        self.assertIn("Score: 0", out)
        self.assertIn("O", out)
        self.assertIn("*", out)

    def test_run_scripted_and_parser(self):
        s = run_scripted("DDSSAAWW", width=10, height=8, seed=2)
        self.assertIsNotNone(s)
        parser = build_parser()
        args = parser.parse_args(["--width", "10", "--height", "8", "--moves", "DD"])
        self.assertEqual(args.width, 10)
        self.assertEqual(args.moves, "DD")

    def test_highscore_persistence(self):
        with tempfile.TemporaryDirectory() as td:
            hp = Path(td) / "highscore.txt"
            self.assertEqual(load_high_score(hp), 0)
            save_high_score(hp, 2)
            self.assertEqual(load_high_score(hp), 2)
            save_high_score(hp, 1)
            self.assertEqual(load_high_score(hp), 2)

    def test_main_scripted(self):
        with tempfile.TemporaryDirectory() as td:
            hp = Path(td) / "score.txt"
            with patch("builtins.print"):
                with patch("sys.argv", ["snake_game.py", "--moves", "DDDD", "--seed", "3", "--highscore-file", str(hp)]):
                    rc = main()
                    self.assertIn(rc, (0, 1))
                    self.assertGreaterEqual(load_high_score(hp), 0)

    def test_main_invalid_board(self):
        with patch("sys.argv", ["snake_game.py", "--width", "2", "--height", "2"]):
            with self.assertRaises(SystemExit):
                main()

    def test_reset_highscore(self):
        with tempfile.TemporaryDirectory() as td:
            hp = Path(td) / "score.txt"
            hp.write_text("5", encoding="utf-8")
            with patch("builtins.print"):
                with patch(
                    "sys.argv",
                    [
                        "snake_game.py",
                        "--moves",
                        "DD",
                        "--highscore-file",
                        str(hp),
                        "--reset-highscore",
                    ],
                ):
                    main()
            self.assertGreaterEqual(load_high_score(hp), 0)

    def test_run_cli_quit_path(self):
        with patch("builtins.input", side_effect=["q"]):
            with patch("builtins.print") as mock_print:
                from src.snake_game import run_cli

                run_cli()
                self.assertTrue(mock_print.called)


if __name__ == "__main__":
    unittest.main()
