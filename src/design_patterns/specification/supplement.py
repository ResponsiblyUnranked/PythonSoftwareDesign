from enum import Enum


class InvalidEmployeeError(ValueError):
    pass


class Department(Enum):
    SALES = "sales"
    HR = "hr"
    MARKETING = "marketing"
    FINANCE = "finance"
    DEVELOPMENT = "development"
