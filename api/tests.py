import unittest
from scripts import *
import pandas as pd
from dotenv import load_dotenv

load_dotenv('../api/.env')
FSE_KEY = os.getenv('FSE_KEY')


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
        self.assertEqual(get_coords('3GV'), (39.0156, -94.2133))
        self.assertEqual(get_coords('KMIA'), (25.7932, -80.2906))


class TestGetDistance(unittest.TestCase):
    def test_mkc_to_mci(self):
        self.assertEqual(get_distance('KMKC', 'kmci'), 12)

    def test_atl_to_lax(self):
        self.assertEqual(get_distance('kAtl', 'KLax'), 1691)


class TestGetAssignments(unittest.TestCase):
    def test_function(self):
        icao = 'KLXT'
        df = get_assignments(FSE_KEY, icao)
        self.assertEqual(df.iloc[0, 0], icao)


class TestStringifyIcaoList(unittest.TestCase):
    def test_n(self):
        test_list = ['3GV', 'KMKC', 'KMCI', 'KATL', 'KCLT']
        self.assertEqual(stringify_icao_list(test_list), ['3GV', 'KMKC', 'KMCI', 'KATL', 'KCLT'])
        self.assertEqual(stringify_icao_list(test_list, n=2), ['3GV-KMCI-KCLT', 'KMKC-KATL'])

    def test_icao_list(self):
        icao_list = get_icao_list()
        stringified_list = stringify_icao_list(icao_list)
        self.assertEqual(len(icao_list), 1092)
        self.assertEqual(len(stringified_list), 30)


if __name__ == '__main__':
    unittest.main()
