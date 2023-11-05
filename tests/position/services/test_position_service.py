import pytest
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock

from app.position.services.position_service import PositionService


class TestCustomerService:
    @pytest.mark.asyncio
    async def test_get_position_candidates_details(self):
        mocked_candidate_repository = Mock()
        mocked_customer_repository = Mock()

        mocked_customer_repository.get_position_candidates = AsyncMock()
        mocked_customer_repository.get_position_candidates.return_value = [
            Mock(
                candidate_id=1,
                technical_score=10,
                softskill_score=20,
                general_score=30,
            ),
            Mock(
                candidate_id=2,
                technical_score=None,
                softskill_score=None,
                general_score=None,
            ),
        ]

        mock_softskill = Mock(id=1, description="Not a reeeal description")
        mock_softskill.name = "Leadership"
        mock_techskill = Mock(id=1)
        mock_techskill.name = "Frontend"
        mocked_candidate_repository.get_candidates_paginated = AsyncMock()
        mock_data = [
            Mock(
                fullname="Candidate A",
                user_id=1,
                soft_skills=[mock_softskill],
                tech_skills=[mock_techskill],
            ),
            Mock(
                fullname="CandidateB",
                user_id=2,
                soft_skills=[mock_softskill],
                tech_skills=[mock_techskill],
            ),
        ]
        mocked_candidate_repository.get_candidates_paginated.return_value = Mock(
            data=mock_data, total_pages=1
        )

        service = PositionService(
            mocked_candidate_repository,
            mocked_customer_repository,
        )

        position_id = 1
        mock_candidate_ids = {"ids": "1,2"}

        response = await service.get_position_candidates_details(position_id)

        mocked_customer_repository.get_position_candidates.assert_called_once_with(
            position_id
        )
        mocked_candidate_repository.get_candidates_paginated.assert_called_once_with(
            mock_candidate_ids
        )
        assert len(response) == 2
        assert response[0]["id"] == 1
        assert response[0]["fullname"] == "Candidate A"

    @pytest.mark.asyncio
    async def test_get_position_candidates_details_http_exception(self):
        mocked_candidate_repository = Mock()
        mocked_customer_repository = Mock()
        mocked_customer_repository.get_position_candidates = AsyncMock()
        mocked_customer_repository.get_position_candidates.side_effect = HTTPException(
            500, "Some Error"
        )

        position_id = 0

        service = PositionService(
            mocked_candidate_repository,
            mocked_customer_repository,
        )

        with pytest.raises(HTTPException):
            await service.get_position_candidates_details(position_id)

    @pytest.mark.asyncio
    async def test_get_position_candidates_details_general_exception(self):
        mocked_candidate_repository = Mock()
        mocked_customer_repository = Mock()
        mocked_customer_repository.get_position_candidates = AsyncMock()
        mocked_customer_repository.get_position_candidates.side_effect = Exception(
            "Some error"
        )

        position_id = -1

        service = PositionService(
            mocked_candidate_repository,
            mocked_customer_repository,
        )

        with pytest.raises(HTTPException):
            await service.get_position_candidates_details(position_id)
