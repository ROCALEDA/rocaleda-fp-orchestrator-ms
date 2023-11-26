from fastapi import HTTPException
from typing import TYPE_CHECKING

from app.client.dto.schemas import InterviewsDetailsResponse

if TYPE_CHECKING:
    from app.client.repositories.candidate_repository import CandidateRepository
    from app.client.repositories.customer_repository import CustomerRepository


class InterviewService:
    def __init__(
        self,
        candidate_repository: "CandidateRepository",
        customer_repository: "CustomerRepository",
    ):
        self.customer_repository = customer_repository
        self.candidate_repository = candidate_repository

    async def get_interviews_details(
        self, role: str, user_id: str, page: str, limit: str
    ) -> InterviewsDetailsResponse:
        try:
            reroute_headers = {"role": role}
            reroute_params = {
                "user_id": user_id,
            }
            if page is not None:
                reroute_params["page"] = page
            if limit is not None:
                reroute_params["limit"] = limit
            interviews_list = await self.candidate_repository.get_interviews_paginated(
                reroute_params, reroute_headers
            )
            
            if not interviews_list.data:
                return {
                    "data": [],
                    "total_pages": 0
                }
            detailed_interviews = []
            query_ids = []
            for interview in interviews_list.data:
                query_ids.append(str(interview.customer_id))
            ids = ",".join(query_ids)
            customers_query_params = {"ids": ids}
            customers_details = await self.customer_repository.get_customers(
                customers_query_params
            )
            for interview in interviews_list.data:
                customer_name = ""
                for customer in customers_details.data:
                    if interview.customer_id == customer.user_id:
                        customer_name = customer.name
                        break
                detailed_interviews.append(
                    {
                        "subject": interview.subject,
                        "client_name": customer_name,
                        "realization_date": interview.realization_date,
                        "score": interview.score,
                    }
                )
            return {
                "data": detailed_interviews,
                "total_pages": interviews_list.total_pages,
            }
        except HTTPException as e:
            print("Http exception: ", e.detail)
            raise e
        except Exception as e:
            print("Internal server error: ", e)
            raise HTTPException(500, "Internal server error")
