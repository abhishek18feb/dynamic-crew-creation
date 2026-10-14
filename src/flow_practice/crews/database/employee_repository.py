from flow_practice.crews.database.mongodb import (
    employees_collection,
)


def search_employees(
    skills: list[str],
    max_workload: int,
) -> list[dict]:

    employees = employees_collection.find(
        {
             "skills": {
                "$in": skills
            },
            "workload_hours": {
                "$lte": max_workload
            },
        },
        {
            "_id": 0
        },
    )

    return list(employees)

def get_employee_by_id(employee_id: str) -> dict | None:
    return employees_collection.find_one(
        {"employee_id": employee_id},
        {"_id": 0},
    )

# from flow_practice.crews.database.mongodb import employees_collection


def create_employee(employee_data: dict) -> dict:
    existing = employees_collection.find_one(
        {"employee_id": employee_data["employee_id"]}
    )

    if existing:
        raise ValueError(
            f"Employee {employee_data['employee_id']} already exists"
        )

    employees_collection.insert_one(employee_data)

    return employee_data

def update_employee(
    employee_id: str,
    update_data: dict,
) -> dict | None:
    # Prevent updates that contain no actual changes.
    if not update_data:
        raise ValueError("No employee fields were provided to update")

    # Only allow updates to these fields.
    allowed_fields = {
        "name",
        "role",
        "email",
        "skills",
        "resume_path",
        "experience_years",
        "workload_hours",
    }

    invalid_fields = set(update_data.keys()) - allowed_fields

    if invalid_fields:
        raise ValueError(
            f"Fields cannot be updated: {sorted(invalid_fields)}"
        )

    result = employees_collection.update_one(
        {"employee_id": employee_id},
        {"$set": update_data},
    )

    if result.matched_count == 0:
        return None

    return employees_collection.find_one(
        {"employee_id": employee_id},
        {"_id": 0},
    )

def delete_employee(employee_id: str) -> dict | None:
    # Find the employee before deleting.
    employee = employees_collection.find_one(
        {"employee_id": employee_id},
        {"_id": 0},
    )

    if employee is None:
        return None

    result = employees_collection.delete_one(
        {"employee_id": employee_id}
    )

    if result.deleted_count == 0:
        return None

    return employee