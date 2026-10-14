import ast
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from flow_practice.employee_flow import EmployeeFlow
from flow_practice.models.employee import Employee
from typing import Any

router = APIRouter()


class EmployeeSearchRequest(BaseModel):
    query: str = Field(
        ...,
        examples=[
            "Find Python or React developers with "
            "workload less than or equal to 20 hours"
        ],
    )


class EmployeeSearchResponse(BaseModel):
    query: str
    employees: list[Employee]


import ast
import json
import re

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from flow_practice.employee_flow import EmployeeFlow
from flow_practice.employee_flow_dynamic import EmployeeFlowDynamic
from flow_practice.models.employee import Employee

router = APIRouter()


def parse_crew_result(raw_result: str):
    """Parse JSON or a Python-like Crew result."""

    # First, try valid JSON.
    try:
        return json.loads(raw_result)
    except (json.JSONDecodeError, TypeError):
        pass

    # Convert MongoDB ObjectId('...') into a quoted string.
    normalized = re.sub(
        r"ObjectId\(['\"]([0-9a-fA-F]{24})['\"]\)",
        r"'\1'",
        raw_result,
    )

    # Then parse the Python representation.
    try:
        return ast.literal_eval(normalized)
    except (ValueError, SyntaxError):
        return None

    
@router.post(
    "/employees/search",
    response_model=None,
)
def search_employees(request: EmployeeSearchRequest):
    flow = EmployeeFlow()

    result = flow.kickoff(
        inputs={"query": request.query}
    )

    raw_result = result.raw

    print("RESULT TYPE:", type(result))
    print("RAW RESULT:", raw_result)

    response_data = parse_crew_result(raw_result)

    if not isinstance(response_data, (dict, list)):
        raise HTTPException(
            status_code=502,
            detail={
                "message": "The employee agent returned an unexpected response.",
                "raw_result": raw_result,
            },
        )

    # Handle an operation error.
    if isinstance(response_data, dict) and response_data.get("error"):
        raise HTTPException(
            status_code=409,
            detail=response_data["error"],
        )

    # Handle successful creation.
    if (
        isinstance(response_data, dict)
        and response_data.get("success") is True
    ):
        return response_data

    # Handle a successful employee lookup.
    if (
        isinstance(response_data, dict)
        and "employee_id" in response_data
    ):
        return {
            "query": request.query,
            "employee": response_data,
        }

    # Handle employee search.
    if isinstance(response_data, list):
        return {
            "query": request.query,
            "employees": response_data,
        }

    raise HTTPException(
        status_code=502,
        detail={
            "message": "Unable to identify the employee operation result.",
            "raw_result": raw_result,
        },
    )


def parse_crew_result_dynamic(raw_result: Any) -> Any:
    """Convert CrewAI output into a Python dict or list."""

    if isinstance(raw_result, (dict, list)):
        return raw_result

    if not isinstance(raw_result, str):
        return None

    text = raw_result.strip()

    # Remove Markdown code fences such as ```json ... ```
    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\s*```$",
                  "",
                  text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
    
@router.post(
    "/employees/search-dynamic",
    response_model=None,
)
def search_employees(request: EmployeeSearchRequest):
    flow = EmployeeFlowDynamic()

    result = flow.kickoff(
        inputs={"query": request.query}
    )

    raw_result = result.raw

    print("RESULT TYPE:", type(result))
    print("RAW RESULT:", raw_result)

    response_data = parse_crew_result_dynamic(raw_result)

    if not isinstance(response_data, (dict, list)):
        raise HTTPException(
            status_code=502,
            detail={
                "message": "The employee agent returned an unexpected response.",
                "raw_result": raw_result,
            },
        )

    # Handle an operation error.
    if isinstance(response_data, dict) and response_data.get("error"):
        raise HTTPException(
            status_code=409,
            detail=response_data["error"],
        )

    # Handle successful creation.
    if (
        isinstance(response_data, dict)
        and response_data.get("success") is True
    ):
        return response_data

    # Handle a successful employee lookup.
    if (
        isinstance(response_data, dict)
        and "employee_id" in response_data
    ):
        return {
            "query": request.query,
            "employee": response_data,
        }

    # Handle employee search.
    if isinstance(response_data, list):
        return {
            "query": request.query,
            "employees": response_data,
        }

    raise HTTPException(
        status_code=502,
        detail={
            "message": "Unable to identify the employee operation result.",
            "raw_result": raw_result,
        },
    )