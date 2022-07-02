from csv_generator import Output
from employee_cpf_record import EmploymentStatus
from input_file import InputFileConfig, InputFile
from utils import parse_birth_dt, parse_dt

if __name__ == '__main__':
    config = InputFileConfig(
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
    filename = './TnT-Salary-2022.xlsx'
    file = InputFile(filename, config)
    employees = file.process()
    print(employees)
