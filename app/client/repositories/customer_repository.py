import httpx
from fastapi import HTTPException
from pydantic import TypeAdapter
from typing import List

from app.client.dto.schemas import PositionCandidate
from app.commons.helpers import build_request_uri
from app.commons.settings import settings


class CustomerRepository:
    async def get_position_candidates(
        self, position_id: int
    ) -> List[PositionCandidate]:
        async with httpx.AsyncClient() as client:
            uri = build_request_uri(
                settings.customers_ms, f"positions/{position_id}/candidates"
            )
            print(f"Calling {uri}")
            response = await client.get(uri, timeout=60)

            if 400 <= response.status_code < 600:
                error_detail = response.json().get("detail", response.text)
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )
            payload = response.json()
            print("Response payload: " + str(payload))
            list_adapter = TypeAdapter(List[PositionCandidate])
            return list_adapter.validate_python(payload)

    async def get_closed_positions(self, project_id: int):
        async with httpx.AsyncClient() as client:
            uri = build_request_uri(
                settings.customers_ms, f"positions/closed/{project_id}"
            )
            print(f"Calling {uri}")
            response = await client.get(uri, timeout=60)

            if 400 <= response.status_code < 600:
                error_detail = response.json().get("detail", response.text)
                raise HTTPException(
                    status_code=response.status_code, detail=error_detail
                )
            payload = response.json()
            print("Response payload: " + str(payload))
            return payload
