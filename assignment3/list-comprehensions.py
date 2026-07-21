# Task 3: List Comprehensions Practice

import csv


with open("../csv/employees.csv", newline="", encoding="utf-8") as csv_file:
    employees = list(csv.reader(csv_file))


# Create a list of full employee names and skip the heading row.
employee_names = [
    employee[1] + " " + employee[2]
    for employee in employees[1:]
]

print(employee_names)


# Create a list containing only names with the letter "e".
names_with_e = [
    name
    for name in employee_names
    if "e" in name.lower()
]

print(names_with_e)