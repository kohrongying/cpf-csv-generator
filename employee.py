from enum import Enum


class Citizenship(Enum):
    PR_1 = '1'
    PR_2 = '2'
    SG = '3'


class CPFContributionType(Enum):
    FULL_GRAD = 'F/G'
    GRAD_GRAD = 'G/G'


class Agency(Enum):
    CDAC = 'CDAC'
    MBMF = 'MBMF'
    SINDA = 'SINDA'
    ECF = 'ECF'


class EmploymentStatus(Enum):
    Existing = 'Existing'
    Left = 'Left'
    New = 'New'
    New_Leaving = 'New & Leaving'


class CPFEntry:
    def __init__(self, ordinary_wage: float, addtional_wage: float, agency_fund: float, agency=Agency.CDAC) -> None:
        self.ordinary_wage = ordinary_wage
        self.additional_wage = addtional_wage
        self.agency_fund = agency_fund
        self.agency = agency


class Employee:
    def __init__(self, id_number: str, name: str, citizenship: str, start_date: str,
                 employment_status: EmploymentStatus,
                 date_left: str, date_of_birth: str, cpf_contribution_type: str, sdl_payable=True) -> None:
        self.id_number = id_number
        self.name = name
        self.citizenship = citizenship
        self.start_date = start_date
        self.employment_status = employment_status
        self.date_left = date_left
        self.date_of_birth = date_of_birth
        self.cpf_contribution_type = cpf_contribution_type
        self.sdl_payable = sdl_payable
        self.cpf_entry = None

    def set_cpf_entry(self, record: CPFEntry) -> None:
        self.cpf_entry = record
