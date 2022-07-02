# Custom handlers
from datetime import datetime
from typing import Optional

from employee_cpf_record import EmploymentStatus


def parse_dt(input_dt: datetime) -> str:
    if input_dt.year < 1980:
        modified_dt = datetime(year=input_dt.year + 100, month=input_dt.month, day=input_dt.day)
        return modified_dt.strftime('%d.%b.%Y')
    else:
        return input_dt.strftime('%d.%b.%Y')


def parse_birth_dt(birth_dt_str, birth_yr) -> str:
    birth_dt = datetime.strptime(birth_dt_str, '%d/%m')
    return f'{birth_dt.strftime("%d.%b")}.{birth_yr}'

