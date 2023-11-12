from fastapi import APIRouter
from typing import List, TYPE_CHECKING

from app.client.dto.schemas import PositionCandidateDetail

if TYPE_CHECKING:
    from app.position.services.position_service import PositionService

router = APIRouter(
    prefix="/positions",
    tags=["positions"],
    responses={404: {"description": "Not found"}},
)


def initialize(position_service: "PositionService"):
    @router.get("/{project_id}")
    async def get_closed_positions_with_candidate(project_id: int):
        return await position_service.get_closed_positions_with_candidate(project_id)

    @router.get("/{position_id}/candidates")
    async def get_position_candidates_details(
        position_id: int,
    ) -> List[PositionCandidateDetail]:
        return await position_service.get_position_candidates_details(position_id)

    return {
        "get_position_candidates_details": get_position_candidates_details,
        "get_closed_positions_with_candidate": get_closed_positions_with_candidate,
    }
