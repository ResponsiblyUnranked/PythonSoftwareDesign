from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.design_patterns.specification.supplement import Employee, Department


# Generic specification framework
class BaseSpecification(ABC):
    @abstractmethod
    def is_satisfied_by(self, employee: Employee) -> bool:
        raise NotImplementedError()

    def __and__(self, other: BaseSpecification) -> AndSpecification:
        return AndSpecification(self, other)

    def __or__(self, other: BaseSpecification) -> OrSpecification:
        return OrSpecification(self, other)

    def __neg__(self) -> NotSpecification:
        return NotSpecification(self)


@dataclass
class AndSpecification(BaseSpecification):
    first: BaseSpecification
    second: BaseSpecification

    def is_satisfied_by(self, employee: Employee) -> bool:
        return self.first.is_satisfied_by(employee) and self.second.is_satisfied_by(
            employee
        )


@dataclass
class OrSpecification(BaseSpecification):
    first: BaseSpecification
    second: BaseSpecification

    def is_satisfied_by(self, employee: Employee) -> bool:
        return self.first.is_satisfied_by(employee) or self.second.is_satisfied_by(
            employee
        )


@dataclass
class NotSpecification(BaseSpecification):
    subject: BaseSpecification

    def is_satisfied_by(self, employee: Employee) -> bool:
        return not self.subject.is_satisfied_by(employee)


# Application specifications
class IsValidWorkingAge(BaseSpecification):
    def is_satisfied_by(self, employee: Employee) -> bool:
        return 18 < employee.age < 99


class HadValidName(BaseSpecification):
    def is_satisfied_by(self, employee: Employee) -> bool:
        return employee.name != ""


class BelongsToDepartment(BaseSpecification):
    def __init__(self, department: Department) -> None:
        self.department = department

    def is_satisfied_by(self, employee: Employee) -> bool:
        return employee.department == self.department


class MatchesHiringCriteria(BaseSpecification):
    def is_satisfied_by(self, employee: Employee) -> bool:
        if (
            employee.age < 18
            or employee.age > 99
            or employee.department == Department.SALES
            or employee.name == ""
        ):
            return False

        return True


class SalesRaiseEligibility(BaseSpecification):
    def is_satisfied_by(self, employee: Employee) -> bool:
        if employee.department == Department.SALES:
            if employee.salary < 10_000:
                return False

            if employee.salary >= 10_000:
                if employee.age >= 75:
                    return False
                else:
                    return True

        return False


class FinanceRaiseEligibility(BaseSpecification):
    def is_satisfied_by(self, employee: Employee) -> bool:
        if employee.department == Department.FINANCE:
            if employee.salary > 85_000:
                return False
            return True

        return False


class DevelopmentRaiseEligibility(BaseSpecification):
    def is_satisfied_by(self, employee: Employee) -> bool:
        if employee.department == Department.DEVELOPMENT:
            return True

        return False


class HrRaiseEligibility(BaseSpecification):
    def is_satisfied_by(self, employee: Employee) -> bool:
        if employee.department == Department.HR:
            for year in employee.previous_bonus_years:
                if year == 2022:
                    return False
            return True

        return False
