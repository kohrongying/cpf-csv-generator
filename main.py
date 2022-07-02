import datetime
from typing import List, Tuple

from openpyxl import load_workbook


def run():
    filename: str = './TnT-Salary-2022.xlsx'
    employees = get_employees_from_sheet(filename)


class InvalidSheetError(Exception):
    pass


def load_current_month_sheet(filename):
    wb = load_workbook(filename)
    current_month = datetime.datetime.now().strftime('%b')
    try:
        ws = wb[current_month]
        return ws
    except KeyError as e:
        raise InvalidSheetError from e


class SheetParserSM:
    Pending, Begin, End = range(3)


def get_employees_from_sheet(filename):
    ws = load_current_month_sheet(filename)
    employees: List[Tuple] = []
    state = SheetParserSM.Pending
    for row in ws.iter_rows(min_row=1, max_col=30):
        second_col = row[1].value.upper() if row[1].value else ''

        if state == SheetParserSM.Pending:
            if 'NAME' in second_col:
                state = SheetParserSM.Begin
        elif state == SheetParserSM.Begin:
            if 'GRAND TOTAL' in second_col:
                state = SheetParserSM.End
            elif second_col:
                employees.append(row)
        else:
            break
    return employees


if __name__ == '__main__':
    load_current_month_sheet('./TnT-Salary-2022.xlsx')
