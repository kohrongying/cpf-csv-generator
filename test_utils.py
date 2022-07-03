from datetime import datetime
from unittest import TestCase

from employee_cpf_record import EmployeeCPFRecord
from utils import parse_dt, parse_birth_dt, build_lookup, merge_employee, merge_employees


class UtilsTest(TestCase):
    def test_parse_dt(self):
        dt = datetime.strptime('1915-04-20 00:00:00', '%Y-%m-%d %H:%M:%S')
        actual = parse_dt(dt)
        self.assertEqual('20.Apr.2015', actual)

    def test_parse_birth_dt(self):
        actual = parse_birth_dt('30/07', 1979)
        self.assertEqual('30.Jul.1979', actual)

    def test_build_lookup(self):
        r1 = EmployeeCPFRecord(name='Candy')
        r2 = EmployeeCPFRecord(name='Choco')
        actual = build_lookup([r1, r2], "name")
        self.assertEqual({"Candy": r1, "Choco": r2}, actual)

    def test_merge_employee(self):
        r1 = EmployeeCPFRecord(name='Candy', ordinary_wage=1000.0)
        r2 = EmployeeCPFRecord(name='Candy', id_number='S9123456A')
        actual = merge_employee(r1, r2)
        self.assertEqual(EmployeeCPFRecord(
            name='Candy',
            ordinary_wage=1000.0,
            id_number='S9123456A'
        ), actual)

        self.assertEqual(EmployeeCPFRecord(
            name='Candy',
            ordinary_wage=1000.0,
        ), r1)
        self.assertEqual(EmployeeCPFRecord(
            name='Candy',
            id_number='S9123456A'
        ), r2)

    def test_merge_employees(self):
        g1_r1 = EmployeeCPFRecord(name='Candy', ordinary_wage=1000.0)
        g1_r2 = EmployeeCPFRecord(name='Choco')

        g2_r1 = EmployeeCPFRecord(name='Candy', id_number='S9123456A')
        g2_r2 = EmployeeCPFRecord(name='Pasta')
        actual = merge_employees('name', [[g1_r1, g1_r2], [g2_r1, g2_r2]])
        self.assertListEqual([
            EmployeeCPFRecord(name='Candy', ordinary_wage=1000.0, id_number='S9123456A'),
            EmployeeCPFRecord(name='Choco'),
            EmployeeCPFRecord(name='Pasta')
        ], actual)
