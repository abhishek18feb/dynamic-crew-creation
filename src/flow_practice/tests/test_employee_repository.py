
import pytest

from flow_practice.crews.database import employee_repository as repo


class FakeEmployeesCollection:
    def __init__(self):
        self.employee = None
        self.find_results = []
        self.matched_count = 1
        self.deleted_count = 1
        self.inserted_documents = []
        self.update_calls = []
        self.delete_calls = []
        self.find_calls = []
        self.find_one_calls = []

    def find(self, query, projection=None):
        self.find_calls.append((query, projection))
        return self.find_results

    def find_one(self, query, projection=None):
        self.find_one_calls.append((query, projection))
        return self.employee

    def insert_one(self, employee_data):
        self.inserted_documents.append(employee_data)
        return {"inserted_id": "fake-id"}

    def update_one(self, query, update):
        self.update_calls.append((query, update))
        return type(
            "UpdateResult",
            (),
            {"matched_count": self.matched_count},
        )()

    def delete_one(self, query):
        self.delete_calls.append(query)
        return type(
            "DeleteResult",
            (),
            {"deleted_count": self.deleted_count},
        )()


@pytest.fixture
def fake_collection(monkeypatch):
    collection = FakeEmployeesCollection()
    monkeypatch.setattr(repo, "employees_collection", collection)
    return collection


@pytest.fixture
def employee_data():
    return {
        "employee_id": "EMP-001",
        "name": "Test Employee",
        "role": "Python Developer",
        "email": "test@example.com",
        "skills": ["Python", "FastAPI"],
        "experience_years": 4,
        "workload_hours": 20,
    }


def test_search_employees_returns_matching_records(
    fake_collection,
    employee_data,
):
    fake_collection.find_results = [employee_data]

    result = repo.search_employees(
        skills=["Python"],
        max_workload=30,
    )

    assert result == [employee_data]
    query, projection = fake_collection.find_calls[0]
    assert query == {
        "skills": {"$in": ["Python"]},
        "workload_hours": {"$lte": 30},
    }
    assert projection == {"_id": 0}


def test_search_employees_returns_empty_list(fake_collection):
    fake_collection.find_results = []

    result = repo.search_employees(
        skills=["Java"],
        max_workload=10,
    )

    assert result == []


def test_get_employee_by_id_returns_employee(
    fake_collection,
    employee_data,
):
    fake_collection.employee = employee_data

    result = repo.get_employee_by_id("EMP-001")

    assert result == employee_data
    assert fake_collection.find_one_calls[0] == (
        {"employee_id": "EMP-001"},
        {"_id": 0},
    )


def test_get_employee_by_id_returns_none_when_missing(
    fake_collection,
):
    fake_collection.employee = None

    assert repo.get_employee_by_id("UNKNOWN") is None


def test_create_employee_inserts_new_record(
    fake_collection,
    employee_data,
):
    fake_collection.employee = None

    result = repo.create_employee(employee_data)

    assert result == employee_data
    assert fake_collection.inserted_documents == [employee_data]


def test_create_employee_rejects_duplicate_id(
    fake_collection,
    employee_data,
):
    fake_collection.employee = {
        "employee_id": "EMP-001",
    }

    with pytest.raises(
        ValueError,
        match="Employee EMP-001 already exists",
    ):
        repo.create_employee(employee_data)

    assert fake_collection.inserted_documents == []


def test_update_employee_rejects_empty_update(
    fake_collection,
):
    with pytest.raises(
        ValueError,
        match="No employee fields were provided",
    ):
        repo.update_employee("EMP-001", {})

    assert fake_collection.update_calls == []


def test_update_employee_rejects_disallowed_fields(
    fake_collection,
):
    with pytest.raises(
        ValueError,
        match="Fields cannot be updated",
    ):
        repo.update_employee(
            "EMP-001",
            {"employee_id": "EMP-999"},
        )

    assert fake_collection.update_calls == []


def test_update_employee_returns_none_when_not_found(
    fake_collection,
):
    fake_collection.matched_count = 0

    result = repo.update_employee(
        "UNKNOWN",
        {"role": "Developer"},
    )

    assert result is None


def test_update_employee_updates_and_returns_employee(
    fake_collection,
    employee_data,
):
    fake_collection.matched_count = 1
    fake_collection.employee = {
        **employee_data,
        "role": "Senior Python Developer",
    }

    result = repo.update_employee(
        "EMP-001",
        {"role": "Senior Python Developer"},
    )

    assert result["role"] == "Senior Python Developer"
    assert fake_collection.update_calls == [
        (
            {"employee_id": "EMP-001"},
            {"$set": {"role": "Senior Python Developer"}},
        )
    ]


def test_delete_employee_returns_none_when_missing(
    fake_collection,
):
    fake_collection.employee = None

    result = repo.delete_employee("UNKNOWN")

    assert result is None
    assert fake_collection.delete_calls == []


def test_delete_employee_returns_none_if_delete_count_is_zero(
    fake_collection,
    employee_data,
):
    fake_collection.employee = employee_data
    fake_collection.deleted_count = 0

    result = repo.delete_employee("EMP-001")

    assert result is None
    assert fake_collection.delete_calls == [
        {"employee_id": "EMP-001"}
    ]


def test_delete_employee_returns_deleted_employee(
    fake_collection,
    employee_data,
):
    fake_collection.employee = employee_data
    fake_collection.deleted_count = 1

    result = repo.delete_employee("EMP-001")

    assert result == employee_data
    assert fake_collection.delete_calls == [
        {"employee_id": "EMP-001"}
    ]
