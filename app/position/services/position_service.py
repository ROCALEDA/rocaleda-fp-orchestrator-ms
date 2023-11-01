from fastapi import HTTPException
from pydantic import TypeAdapter
from typing import List

from app.client.dto.schemas import PositionCandidate
from app.client.repositories.candidate_repository import CandidateRepository
from app.client.repositories.customer_repository import CustomerRepository


class PositionService:
    def __init__(
        self,
        candidate_repository: CandidateRepository,
        customer_repository: CustomerRepository,
    ):
        self.customer_repository = customer_repository
        self.candidate_repository = candidate_repository

    async def get_position_candidates_details(self, position_id: int):
        try:
            candidates_list = await self.customer_repository.get_position_candidates(
                position_id
            )
            # TypeAdapter(List[PositionCandidate]).validate_json(candidates_list)
            query_ids = ""
            for candidate in candidates_list:
                query_ids = query_ids + str(candidate.user_id) + ","
            query_params = {"ids": query_ids}
            return self.candidate_repository.get_candidates_paginated(query_params)
            # candidates_list = PositionCandidatesResponse(**candidates_list.__dict__)

        except HTTPException as e:
            print("Http exception: ", e.detail)
            raise e
        except Exception as e:
            print("Internal server error: ", e)
            raise HTTPException(500, "Internal server error")
