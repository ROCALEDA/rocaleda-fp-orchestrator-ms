import pytest
from unittest.mock import Mock, AsyncMock

from app.interview.controllers import interview_controller


class TestInterviewController:
    @pytest.mark.asyncio
    async def test_get_interview_details(self):
        mocked_service = Mock()
        mocked_service.get_interviews_details = AsyncMock()

        interviews_response = {
            "data": [
                {
                    "subject": "Entrevista X",
                    "client_name": "Pepito Perez",
                    "realization_date": "2021-02-03T09:30:00",
                    "score": 90,
                },
                {
                    "subject": "Entrevista X",
                    "client_name": "Juanito Juarez",
                    "realization_date": "2021-04-01T09:30:00",
                    "score": None,
                },
            ],
            "total_pages": 1,
        }
        mocked_service.get_interviews_details.return_value = interviews_response

        user_id = 21
        page = 1
        limit = 2
        role = 2

        get_interviews_details_func = interview_controller.initialize(mocked_service)[
            "get_interviews_details"
        ]

        func_response = await get_interviews_details_func(role, user_id, page, limit)

        mocked_service.get_interviews_details.assert_called_once_with(
            role, user_id, page, limit
        )
        assert func_response == interviews_response
