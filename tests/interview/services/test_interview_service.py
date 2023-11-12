import pytest
from fastapi import HTTPException
from unittest.mock import Mock, AsyncMock

from app.interview.services.interview_service import InterviewService


class TestCustomerService:
    @pytest.mark.asyncio
    async def test_get_interviews_details(self):
        mocked_candidate_repository = Mock()
        mocked_customer_repository = Mock()

        mocked_candidate_repository.get_interviews_paginated = AsyncMock()
        mocked_candidate_repository.get_interviews_paginated.return_value = Mock(
            data=[
                Mock(
                    id=1,
                    customer_id=21,
                    candidate_id=31,
                    subject="Entrevista X",
                    realization_date="2021-02-03T09:30:00",
                    score=90,
                    open_position_id=22,
                ),
                Mock(
                    id=2,
                    customer_id=21,
                    candidate_id=32,
                    subject="Entrevista X",
                    realization_date="2021-04-01T09:30:00",
                    score=None,
                    open_position_id=None,
                ),
            ],
            total_pages=1,
        )

        mock_customer_1 = Mock(user_id=21)
        mock_customer_1.name = "Customer A"
        mocked_customer_repository.get_customers = AsyncMock()
        mocked_customer_repository.get_customers.return_value = Mock(
            data=[mock_customer_1], total_pages=1
        )

        service = InterviewService(
            mocked_candidate_repository,
            mocked_customer_repository,
        )

        role = 2
        user_id = 21
        page = 1
        limit = 2
        mock_candidate_ids = {"ids": "21,21"}

        response = await service.get_interviews_details(role, user_id, page, limit)

        mocked_candidate_repository.get_interviews_paginated.assert_called_once_with(
            {"user_id": user_id, "page": page, "limit": limit}, {"role": role}
        )
        mocked_customer_repository.get_customers.assert_called_once_with(
            mock_candidate_ids
        )
        assert len(response["data"]) == 2
        assert response["data"][1]["subject"] == "Entrevista X"
        assert response["data"][1]["client_name"] == "Customer A"
        assert response["data"][1]["realization_date"] == "2021-04-01T09:30:00"
        assert response["data"][1]["score"] is None
        assert response["total_pages"] == 1

    @pytest.mark.asyncio
    async def test_get_interviews_details_no_interviews(self):
        mocked_candidate_repository = Mock()
        mocked_customer_repository = Mock()

        mocked_candidate_repository.get_interviews_paginated = AsyncMock()
        mocked_candidate_repository.get_interviews_paginated.return_value = Mock(
            data=[],
            total_pages=1,
        )

        service = InterviewService(
            mocked_candidate_repository,
            mocked_customer_repository,
        )

        role = 2
        user_id = 99
        page = 1
        limit = 2

        response = await service.get_interviews_details(role, user_id, page, limit)

        mocked_candidate_repository.get_interviews_paginated.assert_called_once_with(
            {"user_id": user_id, "page": page, "limit": limit}, {"role": role}
        )
        assert len(response) == 0

    @pytest.mark.asyncio
    async def test_get_interviews_details_http_exception(self):
        mocked_candidate_repository = Mock()
        mocked_customer_repository = Mock()
        mocked_candidate_repository.get_interviews_paginated = AsyncMock()
        mocked_candidate_repository.get_interviews_paginated.side_effect = (
            HTTPException(500, "Some Error")
        )

        role = 2
        user_id = 99
        page = 1
        limit = 2

        service = InterviewService(
            mocked_candidate_repository,
            mocked_customer_repository,
        )

        with pytest.raises(HTTPException):
            await service.get_interviews_details(role, user_id, page, limit)

    @pytest.mark.asyncio
    async def test_get_position_candidates_details_general_exception(self):
        mocked_candidate_repository = Mock()
        mocked_customer_repository = Mock()
        mocked_candidate_repository.get_interviews_paginated = AsyncMock()
        mocked_candidate_repository.get_interviews_paginated.side_effect = Exception(
            "Some error"
        )

        role = 0
        user_id = 0
        page = 0
        limit = 0

        service = InterviewService(
            mocked_candidate_repository,
            mocked_customer_repository,
        )

        with pytest.raises(HTTPException):
            await service.get_interviews_details(role, user_id, page, limit)
