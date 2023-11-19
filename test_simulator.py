import unittest
import datetime

from simulator import constant_weight_func


class TestSimulator(unittest.TestCase):
    def test_constant_weight_func(self):
        self.assertEqual(constant_weight_func({}), 1.0)
        self.assertEqual(constant_weight_func({'tries': [0] * 2, 'times': [datetime.datetime.now()] * 2}), 1.0)


if __name__ == '__main__':
    unittest.main()
