import os
import pytest


class TestSettings:
    @pytest.mark.asyncio
    async def test_settings(self):
        os.environ["candidates_ms"] = "candidates_url"
        os.environ["customers_ms"] = "customers_url"

        from app.commons.settings import settings

        assert settings.candidates_ms == "candidates_url"
        assert settings.customers_ms == "customers_url"
