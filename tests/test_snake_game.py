import unittest
from src.snake_game import create_game, step


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


if __name__ == '__main__':
    unittest.main()
