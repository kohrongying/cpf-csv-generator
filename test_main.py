import datetime
from unittest import TestCase

from main import load_current_month_sheet, get_employees_from_sheet


class Test(TestCase):
    filename = './TnT-Salary-2022-tes.xlsx'

    def test_load_current_month_sheet(self):
        ws = load_current_month_sheet(self.filename)
        expected = datetime.datetime.now().strftime('%b')
        self.assertEqual(expected, ws.title)

    def test_get_employees_from_sheet(self):
        employees = get_employees_from_sheet('./TnT-Salary-2022-tes.xlsx')
        self.assertEqual(12, len(employees))
        start_row_index = employees[0][0].row
        self.assertEqual(7, start_row_index)
