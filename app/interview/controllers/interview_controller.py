from fastapi import APIRouter, Header, Query
from typing import List, TYPE_CHECKING

from app.client.dto.schemas import InterviewsDetailsResponse

if TYPE_CHECKING:
    from app.interview.services.interview_service import InterviewService

router = APIRouter(
    prefix="/interviews",
    tags=["interview"],
    responses={404: {"description": "Not found"}},
)


def initialize(interview_service: "InterviewService"):
    @router.get("")
    async def get_interviews_details(
        role: str = Header(...),
        user_id: str = Query(...),
        page: str = Query(1),
        limit: str = Query(10),
    ) -> List[InterviewsDetailsResponse]:
        return await interview_service.get_interviews_details(
            role, user_id, page, limit
        )

    return {
        "get_interviews_details": get_interviews_details,
    }
