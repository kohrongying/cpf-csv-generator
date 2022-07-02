from datetime import datetime
from unittest import TestCase

from utils import parse_dt, parse_birth_dt


class UtilsTest(TestCase):
    def test_parse_dt(self):
        dt = datetime.strptime('1915-04-20 00:00:00', '%Y-%m-%d %H:%M:%S')
        actual = parse_dt(dt)
        self.assertEqual('20.Apr.2015', actual)

    def test_parse_birth_dt(self):
        actual = parse_birth_dt('30/07', 1979)
        self.assertEqual('30.Jul.1979', actual)
