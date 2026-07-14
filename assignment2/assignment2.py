import csv
import os

def read_employees():
    emdic = {}
    rows = []

    try:
        with open("../csv/employees.csv", "r") as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    emdic["fields"] = row
                else:
                    rows.append(row)

        emdic["rows"] = rows
        return emdic

    except Exception as e:
        print(f"An exception occurred: {e}")


# Task 3
def column_index(column_name):
    return employees["fields"].index(column_name)


# Task 4: 
def first_name(row_number):
    first_name_column = column_index("first_name")
    return employees["rows"][row_number][first_name_column]


# Task 5: 
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))
    return matches


# Task 6: 
def employee_find_2(employee_id):
    matches = list(
        filter(
            lambda row: int(row[employee_id_column]) == employee_id,
            employees["rows"]
        )
    )

    return matches

# Task 7
def sort_by_last_name():
    last_name_column = column_index("last_name")

    employees["rows"].sort(
        key=lambda row: row[last_name_column]
    )

    return employees["rows"]


# Task 8
def employee_dict(row):
    result = {}

    for index, field in enumerate(employees["fields"]):
        if field != "employee_id":
            result[field] = row[index]

    return result

# Task 9
def all_employees_dict():
    result = {}

    for row in employees["rows"]:
        employee_id = row[employee_id_column]
        result[employee_id] = employee_dict(row)

    return result

# Task 10
def get_this_value():
    return os.getenv("THISVALUE")

import custom_module
# Task 11
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)



# Task 12
def read_minutes():
    def read_minutes_file(file_path):
        result = {}
        rows = []

        with open(file_path, "r") as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    result["fields"] = row
                else:
                    rows.append(tuple(row))

        result["rows"] = rows
        return result

    try:
        minutes1 = read_minutes_file("../csv/minutes1.csv")
        minutes2 = read_minutes_file("../csv/minutes2.csv")

        return minutes1, minutes2

    except Exception as e:
        print(f"An exception occurred: {e}")


# Task 13
def create_minutes_set():
    minutes1_set = set(minutes1["rows"])
    minutes2_set = set(minutes2["rows"])

    combined_set = minutes1_set.union(minutes2_set)

    return combined_set

from datetime import datetime
# Task 14
def create_minutes_list():
    minutes_list = list(minutes_set)

    converted_list = list(
        map(
            lambda row: (
                row[0],
                datetime.strptime(row[1], "%B %d, %Y")
            ),
            minutes_list
        )
    )

    return converted_list


# Task 15
def write_sorted_list():
    minutes_list.sort(key=lambda row: row[1])

    converted_list = list(
        map(
            lambda row: (
                row[0],
                datetime.strftime(row[1], "%B %d, %Y")
            ),
            minutes_list
        )
    )

    with open("./minutes.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(minutes1["fields"])
        writer.writerows(converted_list)

    return converted_list

#main

employees = read_employees()
print(employees)

print("-------------")

employee_id_column = column_index("employee_id")

print(employees["rows"])
print("-------------")
print(sort_by_last_name())
print("-------------")

print(employee_dict("rows"))

print("-------------")

print(all_employees_dict())

print("-------------")


set_that_secret("Python is fun!")
print(custom_module.secret)

print("-------------")

minutes1, minutes2 = read_minutes()

print(minutes1)
print(minutes2)

print("-------------")

minutes_set = create_minutes_set()
print(minutes_set)



minutes_list = create_minutes_list()
print(minutes_list)
print("-------------")
