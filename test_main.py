import datetime
from unittest import TestCase

from main import load_current_month_sheet, get_employees_from_sheet


class Test(TestCase):
    filename = './Test-Salary-2022.xlsx'

    def test_load_current_month_sheet(self):
        ws = load_work_sheet(self.filename)
        expected = datetime.datetime.now().strftime('%b')
        self.assertEqual(expected, ws.title)

    def test_load_work_sheet_override_month(self):
        ws = load_work_sheet(self.filename, month='Jun')
        self.assertEqual('Jun', ws.title)

    def test_load_work_sheet_override_invalid_month(self):
        with self.assertRaises(InvalidSheetError):
            load_work_sheet(self.filename, month='abc')

    def test_get_employees_from_sheet(self):
        ws = load_work_sheet(self.filename, month='Jul')
        employees = get_employees_from_sheet(ws)
        self.assertEqual(12, len(employees))
        start_row_index = employees[0][0].row
        self.assertEqual(7, start_row_index)
