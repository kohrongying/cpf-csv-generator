from csv_generator import Output, CSVGenerator
from employee_cpf_record import EmploymentStatus
from input_file import InputFileConfig, InputFile
from utils import parse_birth_dt, parse_dt, merge_files

if __name__ == '__main__':
    config = InputFileConfig(
        desired_rows_config=(1, 'NAME', 'GRAND TOTAL'),
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
    file = InputFile(filename='./Test-Salary-2022.xlsx', config=config)

    pii_config = InputFileConfig(
        desired_rows_config=(1, 'NAME', 'GRAND TOTAL'),
        column_index_mapping={
            Output.id_number: 3,
            Output.name: 1,
        },
    )
    id_numbers_file = InputFile(filename='./Test-Identity-2022.xlsx', config=pii_config)
    employees = merge_files(file, id_numbers_file)

    CSVGenerator().save(records=employees)
