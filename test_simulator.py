import unittest
import datetime

from simulator import constant_weight_func, last_fails_weight_func


class TestSimulator(unittest.TestCase):
    def test_constant_weight_func(self):
        self.assertEqual(constant_weight_func({}), 1.0)
        self.assertEqual(constant_weight_func({'tries': [0, 0], 'times': [datetime.datetime.now()] * 2}), 1.0)

    def test_last_fails_weight_func(self):
        self.assertEqual(last_fails_weight_func({}, 10), 11)
        self.assertEqual(last_fails_weight_func({'tries': []}, 3), 4)
        self.assertEqual(last_fails_weight_func({'tries': [0]}, 3), 4)
        self.assertEqual(last_fails_weight_func({'tries': [0, 0]}, 3), 4)
        self.assertEqual(last_fails_weight_func({'tries': [0, 0, 0]}, 3), 4)
        self.assertEqual(last_fails_weight_func({'tries': [1]}, 3), 3)
        self.assertEqual(last_fails_weight_func({'tries': [1, 0]}, 3), 3)
        self.assertEqual(last_fails_weight_func({'tries': [1, 0, 0]}, 3), 3)
        self.assertEqual(last_fails_weight_func({'tries': [1, 1]}, 3), 2)
        self.assertEqual(last_fails_weight_func({'tries': [1, 1, 0]}, 3), 2)
        self.assertEqual(last_fails_weight_func({'tries': [1, 1, 1]}, 3), 1)
        self.assertEqual(last_fails_weight_func({'tries': [0, 1, 1, 1]}, 3), 1)
        self.assertEqual(last_fails_weight_func({'tries': [0, 0, 1, 1]}, 3), 2)
        self.assertEqual(last_fails_weight_func({'tries': [0, 1, 0, 1]}, 3), 2)
        self.assertEqual(last_fails_weight_func({'tries': [0, 1, 1, 0]}, 3), 2)
        self.assertEqual(last_fails_weight_func({'tries': [1, 1, 1, 1]}, 3), 1)
        self.assertEqual(last_fails_weight_func({'tries': [1, 0, 1, 1]}, 3), 2)
        self.assertEqual(last_fails_weight_func({'tries': [1, 1, 0, 1]}, 3), 2)
        self.assertEqual(last_fails_weight_func({'tries': [1, 1, 1, 0]}, 3), 2)


if __name__ == '__main__':
    unittest.main()
