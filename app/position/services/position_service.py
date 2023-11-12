from fastapi import HTTPException
from typing import List, TYPE_CHECKING

from app.client.dto.schemas import PositionCandidateDetail

if TYPE_CHECKING:
    from app.client.repositories.candidate_repository import CandidateRepository
    from app.client.repositories.customer_repository import CustomerRepository


class PositionService:
    def __init__(
        self,
        candidate_repository: "CandidateRepository",
        customer_repository: "CustomerRepository",
    ):
        self.customer_repository = customer_repository
        self.candidate_repository = candidate_repository

    async def get_closed_positions_with_candidate(self, project_id: int):
        try:
            positions = await self.customer_repository.get_closed_positions(project_id)

            positions = [
                {
                    "position_id": position["id"],
                    "position_name": position["position_name"],
                    "candidate_id": position["candidate_id"],
                    "candidate_name": (
                        await self.candidate_repository.get_candidates_paginated(
                            {"ids": f"{position['candidate_id']}"}
                        )
                    )
                    .data[0]
                    .fullname,
                }
                for position in positions
            ]
            print("ACA AL FINAL")
            return positions
        except HTTPException as e:
            print("Http exception: ", e.detail)
            raise e
        except Exception as e:
            print("Internal server error: ", e)
            raise HTTPException(500, "Internal server error")

    async def get_position_candidates_details(
        self, position_id: int
    ) -> List[PositionCandidateDetail]:
        try:
            candidates_list = await self.customer_repository.get_position_candidates(
                position_id
            )
            if not candidates_list:
                return []
            query_ids = []
            for candidate in candidates_list:
                query_ids.append(str(candidate.candidate_id))
            ids = ",".join(query_ids)
            query_params = {"ids": ids}
            candidates_details = (
                await self.candidate_repository.get_candidates_paginated(query_params)
            )
            position_candidates = []
            for candidate_data in candidates_details.data:
                position_candidates.append(
                    {
                        "user_id": candidate_data.user_id,
                        "fullname": candidate_data.fullname,
                        "tech_skills": candidate_data.tech_skills,
                        "soft_skills": candidate_data.soft_skills,
                    }
                )
            return position_candidates

        except HTTPException as e:
            print("Http exception: ", e.detail)
            raise e
        except Exception as e:
            print("Internal server error: ", e)
            raise HTTPException(500, "Internal server error")
