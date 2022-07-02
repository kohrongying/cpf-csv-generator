from typing import List, Tuple

from openpyxl import load_workbook
from datetime import datetime

from employee_cpf_record import EmployeeCPFRecord


class InputFileConfig:
    def __init__(self, sheet_name=None, column_index_mapping=None, desired_rows_config=None) -> None:
        self.sheet_name = sheet_name or datetime.now().strftime('%b')
        self.column_index_mapping = column_index_mapping
        self.desired_rows_config = desired_rows_config or (1, 'NAME', 'TOTAL')


class InvalidSheetError(Exception):
    pass


class SheetParserSM:
    Pending, Begin, End = range(3)


class InputFile:
    def __init__(self, filename, config: InputFileConfig) -> None:
        self.filename = filename
        self.config = config

    def load_work_sheet(self):
        wb = load_workbook(self.filename, data_only=True)
        try:
            ws = wb[self.config.sheet_name]
            wb.close()
            return ws
        except KeyError as e:
            raise InvalidSheetError from e

    def get_employees_from_sheet(self):
        ws = self.load_work_sheet()
        employees: List[Tuple] = []
        state = SheetParserSM.Pending
        target_col_index, desired_rows_start_identifier, desired_rows_end_identifier = self.config.desired_rows_config
        for row in ws.iter_rows(min_row=1, max_col=30):
            target_col = row[target_col_index].value.upper() if row[target_col_index].value else ''

            if state == SheetParserSM.Pending:
                if desired_rows_start_identifier in target_col:
                    state = SheetParserSM.Begin
            elif state == SheetParserSM.Begin:
                if desired_rows_end_identifier in target_col:
                    state = SheetParserSM.End
                elif target_col:
                    employees.append(row)
            else:
                break
        return employees

    def create_record(self, row) -> EmployeeCPFRecord:
        e = EmployeeCPFRecord(
            name=self.extract_row_value(row, 'name')
        )
        return e

    def extract_row_value(self, row, column_name):
        try:
            if column_name in self.config.column_index_mapping:
                index = self.config.column_index_mapping.get(column_name)
                return row[index].value
        except Exception as e:
            raise e
        else:
            return None

    def process(self) -> List[EmployeeCPFRecord]:
        employees = self.get_employees_from_sheet()
        records = [self.create_record(employee) for employee in employees]
        return records
