import unittest
import datetime

from simulator import constant_weight_func, fails_weight_func, frequency_weight_func


class TestSimulator(unittest.TestCase):
    def test_constant_weight_func(self):
        self.assertEqual(constant_weight_func({}), 1.0)
        self.assertEqual(constant_weight_func({'tries': [0, 0], 'times': [datetime.datetime.now()] * 2}), 1.0)

    def test_fails_weight_func(self):
        self.assertEqual(fails_weight_func({}, 10), 0) # TODO: flip order of args
        self.assertEqual(fails_weight_func({'tries': []}, 3), 0)
        self.assertEqual(fails_weight_func({'tries': [0]}, 3), 1)
        self.assertEqual(fails_weight_func({'tries': [0, 0]}, 3), 4)
        self.assertEqual(fails_weight_func({'tries': [0, 0, 0]}, 3), 9)
        self.assertEqual(fails_weight_func({'tries': [1]}, 3), 0)
        self.assertEqual(fails_weight_func({'tries': [1, 0]}, 3), 1)
        self.assertEqual(fails_weight_func({'tries': [1, 0, 0]}, 3), 4)
        self.assertEqual(fails_weight_func({'tries': [1, 1]}, 3), 0)
        self.assertEqual(fails_weight_func({'tries': [1, 1, 0]}, 3), 1)
        self.assertEqual(fails_weight_func({'tries': [1, 1, 1]}, 3), 0)
        self.assertEqual(fails_weight_func({'tries': [0, 1, 1, 1]}, 3), 0)
        self.assertEqual(fails_weight_func({'tries': [0, 0, 1, 1]}, 3), 1)
        self.assertEqual(fails_weight_func({'tries': [0, 1, 0, 1]}, 3), 1)
        self.assertEqual(fails_weight_func({'tries': [0, 1, 1, 0]}, 3), 1)
        self.assertEqual(fails_weight_func({'tries': [1, 1, 1, 1]}, 3), 0)
        self.assertEqual(fails_weight_func({'tries': [1, 0, 1, 1]}, 3), 1)
        self.assertEqual(fails_weight_func({'tries': [1, 1, 0, 1]}, 3), 1)
        self.assertEqual(fails_weight_func({'tries': [1, 1, 1, 0]}, 3), 1)

    def test_frequency_weight_func(self):
        def now_func():
            return datetime.datetime(2023, 12, 16, 15, 30)
        now_ts = now_func()
        day0 = now_ts - datetime.timedelta(minutes=30)
        day1 = now_ts - datetime.timedelta(days=1)
        day2 = now_ts - datetime.timedelta(days=2)
        day6 = now_ts - datetime.timedelta(days=6)
        day7 = now_ts - datetime.timedelta(days=7)
        day10 = now_ts - datetime.timedelta(days=10)
        day14 = now_ts - datetime.timedelta(days=14)
        day21 = now_ts - datetime.timedelta(days=21)

        self.assertEqual(frequency_weight_func({}, 10, 1), 10)
        self.assertEqual(frequency_weight_func({'times': [day0]}, 3, 7, now_func), 2)
        self.assertEqual(frequency_weight_func({'times': [day7]}, 3, 7, now_func), 2)
        self.assertEqual(frequency_weight_func({'times': [day0, day0]}, 3, 7, now_func), 2)
        self.assertEqual(frequency_weight_func({'times': [day1, day0]}, 3, 7, now_func), 2)
        self.assertEqual(frequency_weight_func({'times': [day6, day0]}, 3, 7, now_func), 2)
        self.assertEqual(frequency_weight_func({'times': [day7, day0]}, 3, 7, now_func), 1)
        self.assertEqual(frequency_weight_func({'times': [day10, day7]}, 3, 7, now_func), 2)
        self.assertEqual(frequency_weight_func({'times': [day2, day1, day0]}, 3, 7, now_func), 2)
        self.assertEqual(frequency_weight_func({'times': [day7, day1, day0]}, 3, 7, now_func), 1)
        self.assertEqual(frequency_weight_func({'times': [day10, day7, day1, day0]}, 3, 7, now_func), 1)
        self.assertEqual(frequency_weight_func({'times': [day14, day0]}, 3, 7, now_func), 1)
        self.assertEqual(frequency_weight_func({'times': [day14, day7, day0]}, 3, 7, now_func), 0)
        self.assertEqual(frequency_weight_func({'times': [day21, day14, day7, day0]}, 3, 7, now_func), 0)
        self.assertEqual(frequency_weight_func({'times': [day21, day10, day7, day0]}, 3, 7, now_func), 1)


if __name__ == '__main__':
    unittest.main()
