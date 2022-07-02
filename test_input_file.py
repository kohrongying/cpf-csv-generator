from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from csv_generator import Output
from input_file import InputFileConfig, InvalidSheetError, InputFile


class TestInputFileConfig(TestCase):
    def test_input_file_config_without_sheet_name_should_return_current_month(self):
        config = InputFileConfig()
        expected = datetime.now().strftime('%b')
        self.assertEqual(expected, config.sheet_name)

    def test_input_file_config_with_sheet_name_should_return_it(self):
        config = InputFileConfig(sheet_name='Jun')
        self.assertEqual('Jun', config.sheet_name)


class TestInputFile(TestCase):
    filename = './Test-Salary-2022.xlsx'
    desired_rows_config = (1, 'NAME', 'GRAND TOTAL')
    config = InputFileConfig(sheet_name='Jun', desired_rows_config=desired_rows_config)

    def test_load_work_sheet_override_invalid_month(self):
        invalid_config = InputFileConfig(sheet_name='abc')
        with self.assertRaises(InvalidSheetError):
            InputFile(self.filename, invalid_config).load_work_sheet()

    def test_get_employees_from_sheet(self):
        sheet_rows = InputFile(self.filename, self.config).get_employees_from_sheet()
        self.assertEqual(13, len(sheet_rows))
        start_row_index = sheet_rows[0][0].row
        self.assertEqual(7, start_row_index)

    def test_extract_row_value_with_title_should_return_value(self):
        config = InputFileConfig(column_index_mapping={
            Output.name: 1
        })
        row = (0, MagicMock(value='Sharon Mendez'))
        actual = InputFile(self.filename, config).extract_row_value(row, Output.name)
        self.assertEqual('Sharon Mendez', actual)

    def test_input_file_config_without_title_should_return_None(self):
        config = InputFileConfig(column_index_mapping={
            Output.name: 1
        })
        row = (0, MagicMock(value='Sharon Mendez'))
        actual = InputFile(self.filename, config).extract_row_value(row, Output.id_number)
        self.assertEqual(None, actual)
