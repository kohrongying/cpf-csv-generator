from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock

from csv_generator import Output
from employee_cpf_record import Agency, EmploymentStatus
from input_file import InputFileConfig, InvalidSheetError, InputFile
from utils import parse_dt, parse_birth_dt


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

    def test_extract_row_value_without_title_should_return_None(self):
        config = InputFileConfig(column_index_mapping={
            Output.name: 1
        })
        row = (0, MagicMock(value='Sharon Mendez'))
        actual = InputFile(self.filename, config).extract_row_value(row, Output.id_number)
        self.assertEqual(None, actual)

    def test_extract_row_value_support_array_indexes(self):
        config = InputFileConfig(column_index_mapping={
            Output.date_of_birth: [0, 1]
        })
        row = (MagicMock(value='haha'), MagicMock(value='Sharon Mendez'))
        actual = InputFile(self.filename, config).extract_row_value(row, Output.date_of_birth)
        self.assertEqual(['haha', 'Sharon Mendez'], actual)

    def test_extract_row_value_support_array_indexes(self):
        config = InputFileConfig(column_index_mapping={
            Output.date_of_birth: [0, 1]
        })
        row = (MagicMock(value='haha'), MagicMock(value='Sharon Mendez'))
        actual = InputFile(self.filename, config).extract_row_value(row, Output.date_of_birth)
        self.assertEqual(['haha', 'Sharon Mendez'], actual)

    def test_additional_handlers_should_take_custom_fn_return_processed_value(self):
        handlers = {
            Output.agency_fund: lambda x: abs(x),
        }
        config = InputFileConfig(sheet_name='Jun', column_index_mapping={
            Output.agency_fund: 1,
        }, additional_handlers=handlers)
        row = (0, MagicMock(value=-1.5))
        actual = InputFile(self.filename, config).process_row_value(row, Output.agency_fund)
        self.assertEqual(1.5, actual)

    def test_additional_handlers_support_multiple_arguments(self):
        handlers = {
            Output.date_of_birth: lambda x, y: parse_birth_dt(x, y),
        }
        config = InputFileConfig(sheet_name='Jun', column_index_mapping={
            Output.date_of_birth: [0, 1],
        }, additional_handlers=handlers)
        row = (MagicMock(value='30/7'), MagicMock(value=1979))
        actual = InputFile(self.filename, config).process_row_value(row, Output.date_of_birth)
        self.assertEqual('30.Jul.1979', actual)

    def test_create_record_should_return_correct_values(self):
        config = InputFileConfig(
            sheet_name='Jun',
            column_index_mapping={
                Output.name: 1,
                Output.ordinary_wage: 7,
                Output.additional_wage: 10,
                Output.agency_fund: 17,
                Output.date_of_birth: [23, 24],
                Output.date_left: 21,
                Output.employment_status: 21
            },
            additional_handlers={
                Output.agency_fund: lambda x: abs(x),
                Output.date_of_birth: lambda x, y: parse_birth_dt(x, y),
                Output.date_left: lambda x: parse_dt(x) if x else None,
                Output.employment_status: lambda x: EmploymentStatus.Left if x else EmploymentStatus.Existing,
            }
        )
        file = InputFile(self.filename, config)
        sheet_rows = file.get_employees_from_sheet()
        record = file.create_record(sheet_rows[0])
        self.assertEqual(2000, record.ordinary_wage)
        self.assertEqual(1230.25, record.additional_wage)
        self.assertEqual(1.5, record.agency_fund)
        self.assertEqual(Agency.CDAC, record.agency)
        self.assertEqual('Sharon Mendez', record.name)
        self.assertEqual('30.Jul.1979', record.date_of_birth)
        self.assertEqual(None, record.date_left)
        self.assertEqual(EmploymentStatus.Existing, record.employment_status)
        self.assertTrue(record.sdl_payable)
