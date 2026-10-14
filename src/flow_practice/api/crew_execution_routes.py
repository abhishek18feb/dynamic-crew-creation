
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from flow_practice.crews.crew.crew_builder import CrewBuilder


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/crews",
    tags=["Crew Execution"],
)

builder = CrewBuilder()


class CrewRunInput(BaseModel):
    inputs: dict = Field(default_factory=dict)


@router.post("/{crew_id}/run")
def run_crew(crew_id: str, request: CrewRunInput):
    try:
        crew = builder.build_crew(crew_id)
        result = crew.kickoff(inputs=request.inputs)

        return {
            "success": True,
            "crew_id": crew_id,
            "result": str(result),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception(
            "Crew execution failed for crew_id=%s",
            crew_id,
        )
        raise HTTPException(
            status_code=500,
            detail="Crew execution failed. Check application logs.",
        ) from exc
