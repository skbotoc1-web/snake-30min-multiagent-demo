import unittest
from unittest.mock import patch

from src.snake_game import create_game, step, render, GameState


class SnakeTests(unittest.TestCase):
    def test_initial_state(self):
        s = create_game(seed=1)
        self.assertEqual(len(s.snake), 3)
        self.assertFalse(s.game_over)

    def test_move_and_grow(self):
        s = create_game(width=8, height=6, seed=1)
        s.food = (s.snake[0][0], s.snake[0][1] + 1)
        step(s, 'D', seed=2)
        self.assertEqual(s.score, 1)
        self.assertEqual(len(s.snake), 4)

    def test_wall_collision(self):
        s = create_game(width=5, height=5, seed=1)
        for _ in range(10):
            step(s, 'W')
            if s.game_over:
                break
        self.assertTrue(s.game_over)

    def test_prevent_opposite_direction(self):
        s = create_game(seed=1)
        # initial direction is D, opposite A should be ignored
        old_head = s.snake[0]
        step(s, 'A')
        self.assertEqual(s.direction, 'D')
        self.assertNotEqual(s.snake[0], old_head)

    def test_self_collision(self):
        s = create_game(width=6, height=6, seed=1)
        # Grow snake to allow self-collision shape
        for move in ['D', 'S', 'A']:
            s.food = (
                s.snake[0][0] + (1 if move == 'S' else -1 if move == 'W' else 0),
                s.snake[0][1] + (1 if move == 'D' else -1 if move == 'A' else 0),
            )
            step(s, move)
        # Now move up into body
        step(s, 'W')
        self.assertTrue(s.game_over)

    def test_render_contains_score_and_symbols(self):
        s = create_game(seed=1)
        out = render(s)
        self.assertIn('Score: 0', out)
        self.assertIn('O', out)
        self.assertIn('*', out)

    def test_run_cli_quit_path(self):
        # Cover run_cli path minimally
        with patch('builtins.input', side_effect=['q']):
            with patch('builtins.print') as mock_print:
                from src.snake_game import run_cli
                run_cli()
                self.assertTrue(mock_print.called)


if __name__ == '__main__':
    unittest.main()
