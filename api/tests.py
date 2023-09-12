import unittest
from scripts import *


class TestGetIcaoList(unittest.TestCase):
    def test_first(self):
        actual = get_icao_list()[0]
        expected = '00V'
        self.assertEqual(actual, expected)

    def test_last(self):
        actual = get_icao_list()[-1]
        expected = 'Z71'
        self.assertEqual(actual, expected)


class TestGetCoords(unittest.TestCase):
    def test_g3v(self):
        self.assertEqual(get_coords('3gv'), (39.0156, -94.2133))
        self.assertEqual(get_coords('KMIA'), (25.7932, -80.2906))


if __name__ == '__main__':
    unittest.main()
