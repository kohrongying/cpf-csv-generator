import datetime
from unittest import TestCase

from employee import Agency
from main import load_work_sheet, get_employees_from_sheet, create_cpf_entry, InvalidSheetError


class TestMain(TestCase):
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

    def test_create_cpf_entry(self):
        ws = load_work_sheet(self.filename, month='Jun')
        rows = get_employees_from_sheet(ws)
        row = rows[0]
        cpf_entry = create_cpf_entry(row)
        self.assertEqual(2000, cpf_entry.ordinary_wage)
        self.assertEqual(1230.25, cpf_entry.additional_wage)
        self.assertEqual(1.50, cpf_entry.agency_fund)
        self.assertEqual(Agency.CDAC, cpf_entry.agency)
