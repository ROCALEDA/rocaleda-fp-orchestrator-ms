import pytest
from unittest.mock import Mock, AsyncMock

from app.position.controllers import position_controller


class TestPositionController:
    @pytest.mark.asyncio
    async def test_get_position_candidates_details(self):
        mocked_service = Mock()
        mocked_service.get_position_candidates_details = AsyncMock()

        pos_candidates_data = [
            {"user_id": 1, "fullname": "Candidate A"},
            {"user_id": 2, "fullname": "Candidate B"},
        ]
        mocked_service.get_position_candidates_details.return_value = (
            pos_candidates_data
        )

        position_id = 1

        get_position_candidates_details_func = position_controller.initialize(
            mocked_service
        )["get_position_candidates_details"]

        func_response = await get_position_candidates_details_func(position_id)

        mocked_service.get_position_candidates_details.assert_called_once_with(
            position_id
        )
        assert func_response == pos_candidates_data
