import csv
import os
from datetime import datetime

import custom_module


# Task 2
def read_employees():
    employees_data = {
        "fields": [],
        "rows": [],
    }

    try:
        with open("../csv/employees.csv", "r", newline="") as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    employees_data["fields"] = row
                else:
                    employees_data["rows"].append(row)

        return employees_data

    except Exception as error:
        print(f"An exception occurred: {error}")
        return employees_data



employees = read_employees()


# Task 3
def column_index(column_name):
    return employees["fields"].index(column_name)



employee_id_column = column_index("employee_id")


# Task 4
def first_name(row_number):
    first_name_column = column_index("first_name")
    return employees["rows"][row_number][first_name_column]


# Task 5
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    return list(filter(employee_match, employees["rows"]))


# Task 6
def employee_find_2(employee_id):
    return list(
        filter(
            lambda row: int(row[employee_id_column]) == employee_id,
            employees["rows"],
        )
    )


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


# Task 11
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)


# Task 12
def read_minutes():
    def read_minutes_file(file_path):
        result = {
            "fields": [],
            "rows": [],
        }

        with open(file_path, "r", newline="") as file:
            reader = csv.reader(file)

            for index, row in enumerate(reader):
                if index == 0:
                    result["fields"] = row
                else:
                    result["rows"].append(tuple(row))

        return result

    try:
        first_minutes = read_minutes_file("../csv/minutes1.csv")
        second_minutes = read_minutes_file("../csv/minutes2.csv")
        return first_minutes, second_minutes

    except Exception as error:
        print(f"An exception occurred: {error}")
        return (
            {"fields": [], "rows": []},
            {"fields": [], "rows": []},
        )



minutes1, minutes2 = read_minutes()


# Task 13
def create_minutes_set():
    minutes1_set = set(minutes1["rows"])
    minutes2_set = set(minutes2["rows"])

    return minutes1_set.union(minutes2_set)



minutes_set = create_minutes_set()


# Task 14
def create_minutes_list():
    return list(
        map(
            lambda row: (
                row[0],
                datetime.strptime(row[1], "%B %d, %Y"),
            ),
            minutes_set,
        )
    )


minutes_list = create_minutes_list()


# Task 15
def write_sorted_list():
    
    minutes_list.sort(key=lambda row: row[1])

    sorted_list = list(
        map(
            lambda row: (
                row[0],
                datetime.strftime(row[1], "%B %d, %Y"),
            ),
            minutes_list,
        )
    )

    with open("./minutes.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(minutes1["fields"])
        writer.writerows(sorted_list)

    return sorted_list



if __name__ == "__main__":
    print(sort_by_last_name())
    print("----------------")

    print(employee_dict(employees["rows"][0]))
    print("----------------")

    print(all_employees_dict())
    print("----------------")

    set_that_secret("Python is fun!")
    print(custom_module.secret)
    print("----------------")

    print(minutes1)
    print(minutes2)
    print("----------------")

    print(minutes_set)
    print("----------------")

    print(minutes_list)
    print("----------------")

    print(write_sorted_list())