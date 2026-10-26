
def test_addition():
    result = 10 + 20

    assert result == 30


def test_employee_name():
    employee_name = "Vikram Patel"

    assert employee_name == "Vikram Patel"


def test_workload_limit():
    workload_hours = 20
    maximum_hours = 25

    assert workload_hours <= maximum_hours