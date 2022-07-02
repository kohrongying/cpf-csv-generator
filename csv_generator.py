from enum import Enum


class Output(Enum):
    id_number, name, ordinary_wage, additional_wage, agency_fund, agency, citizenship, pr_start_date, cpf_contribution_type, employment_status, date_left, date_of_birth, sdl_payable = range(13)