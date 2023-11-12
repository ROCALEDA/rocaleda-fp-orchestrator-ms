import httpx
from fastapi import HTTPException
from app.client.dto.schemas import CandidatesResponse, InterviewsResponse
from app.commons.helpers import build_request_uri
from app.commons.settings import settings


class CandidateRepository:
    async def get_candidates_paginated(self, query_params) -> CandidatesResponse:
        async with httpx.AsyncClient() as client:
            uri = build_request_uri(settings.candidates_ms, "candidates")
            print(f"Sending {query_params} to {uri}")
            response = await client.get(uri, params=query_params, timeout=60)

            if 400 <= response.status_code < 600:
                error_detail = response.json().get("detail", response.text)
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )
            payload = response.json()
            print("Response payload: " + str(payload))
            return payload

    async def get_interviews_paginated(self, query_params, headers) -> InterviewsResponse:
        async with httpx.AsyncClient() as client:
            uri = build_request_uri(settings.candidates_ms, "interviews")
            print(
                f"Sending params {query_params} and headers {headers} to GET {uri}"
            )
            response = await client.get(
                uri, params=query_params, headers=headers, timeout=60
            )
            if 400 <= response.status_code < 600:
                error_detail = response.json().get("detail", response.text)
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )
            print("Response payload: " + str(payload))
            return response.json()