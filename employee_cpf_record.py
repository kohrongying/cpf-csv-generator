from dataclasses import dataclass
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


@dataclass
class EmployeeCPFRecord:
    id_number: str = None
    name: str = None
    ordinary_wage: float = None
    additional_wage: float = None
    agency_fund: float = None
    agency: Agency = Agency.CDAC
    citizenship: Citizenship = None
    pr_start_date: str = None
    cpf_contribution_type: CPFContributionType = None
    employment_status: EmploymentStatus = None
    date_left: str = None
    date_of_birth: str = None
    sdl_payable: bool = True
