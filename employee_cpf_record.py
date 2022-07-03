from enum import Enum


class Citizenship(Enum):
    PR_1 = '1'
    PR_2 = '2'
    SG = '3'


class CPFContributionType(Enum):
    FULL_GRAD = 'F/G'
    GRAD_GRAD = 'G/G'
    NA = ''


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


class EmployeeCPFRecord:
    def __init__(self, id_number=None, name=None, ordinary_wage=None, additional_wage=None, agency_fund=None,
                 agency=None, citizenship=None, pr_start_date=None,
                 employment_status=None,
                 date_left=None, date_of_birth=None, cpf_contribution_type=None, sdl_payable=None, ) -> None:
        self.id_number = id_number
        self.name = name
        self.ordinary_wage = ordinary_wage
        self.additional_wage = additional_wage
        self.agency_fund = agency_fund
        self.agency = agency
        self.citizenship = citizenship
        self.pr_start_date = pr_start_date
        self.cpf_contribution_type = cpf_contribution_type
        self.employment_status = employment_status
        self.date_left = date_left
        self.date_of_birth = date_of_birth
        self.sdl_payable = sdl_payable
