# Custom handlers
import copy
from datetime import datetime
from typing import List

from employee_cpf_record import EmployeeCPFRecord


def parse_dt(input_dt: datetime) -> str:
    if input_dt.year < 1980:
        modified_dt = datetime(year=input_dt.year + 100, month=input_dt.month, day=input_dt.day)
        return modified_dt.strftime('%d.%b.%Y')
    else:
        return input_dt.strftime('%d.%b.%Y')


def parse_birth_dt(birth_dt_str, birth_yr) -> str:
    birth_dt = datetime.strptime(birth_dt_str, '%d/%m')
    return f'{birth_dt.strftime("%d.%b")}.{birth_yr}'


def build_lookup(emp_list, lookup_key):
    d = {}
    for r in emp_list:
        d[r.__getattribute__(lookup_key)] = r
    return d


def merge_employee(r1: EmployeeCPFRecord, r2: EmployeeCPFRecord) -> EmployeeCPFRecord:
    r1_copy = copy.deepcopy(r1)
    for attr in list(r1.__dict__.keys()):
        if r2.__getattribute__(attr):
            r1_copy.__setattr__(attr, r2.__getattribute__(attr))
    return r1_copy


def merge_employees(merge_criteria, emp_lists: List[List[EmployeeCPFRecord]]) -> List[EmployeeCPFRecord]:
    if len(emp_lists) == 1:
        return emp_lists[0]

    d = build_lookup(emp_lists[0], merge_criteria)
    for emp_list in emp_lists[1:]:
        for r2 in emp_list:
            lookup_key: str = r2.__getattribute__(merge_criteria)
            if lookup_key in d:
                r1: EmployeeCPFRecord = d.get(lookup_key)
                d[lookup_key] = merge_employee(r1, r2)
            else:
                d[lookup_key] = r2
    return list(d.values())


def merge_files(*file_args, on="name") -> List[EmployeeCPFRecord]:
    employee_record_groups = [file.process() for file in file_args]
    return merge_employees(on, employee_record_groups)
