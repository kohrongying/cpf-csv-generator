from datetime import datetime
from enum import Enum
import csv
from typing import List

from employee_cpf_record import EmployeeCPFRecord


class Output(Enum):
    id_number, name, ordinary_wage, additional_wage, agency_fund, agency, citizenship, pr_start_date, cpf_contribution_type, employment_status, date_left, date_of_birth, sdl_payable = range(
        13)


class CSVGenerator:
    template_file = './CPF-ESS_Employee_Template.csv'

    def save(self, records: List[EmployeeCPFRecord]):
        with open(self.template_file, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            field_names = next(reader)

        with open(f'CPF-ESS_Employee_{datetime.today().strftime("%Y-%m-%d")}.csv', mode='w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(field_names)

            for record in records:
                writer.writerow([
                    record.id_number,
                    record.name,
                    record.ordinary_wage,
                    record.additional_wage,
                    record.agency_fund,
                    record.agency.value,
                    record.citizenship.value,
                    record.pr_start_date,
                    record.cpf_contribution_type.value,
                    record.employment_status.value,
                    record.date_left,
                    record.date_of_birth,
                    "Yes" if record.sdl_payable else "No",
                ])
