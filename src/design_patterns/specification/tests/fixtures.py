from src.design_patterns.specification.supplement import Department

valid_new_employees = [
    ("Roy", 31, Department.DEVELOPMENT),
    ("Jen", 28, Department.HR),
    ("Moss", 30, Department.FINANCE),
]

invalid_new_employees = [
    ("Jaon", 10, Department.DEVELOPMENT),
    ("Clare", 28, Department.SALES),
    ("Sarah", 102, Department.MARKETING),
    ("", 45, Department.HR),
]
