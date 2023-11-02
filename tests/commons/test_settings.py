import os
import pytest


class TestSettings:
    @pytest.mark.asyncio
    async def test_settings(self):
        os.environ["customers_ms"] = "customers_url"
        os.environ["candidates_ms"] = "candidates_url"

        from app.commons.settings import settings

        assert settings.candidates_ms == "customers_url"
        assert settings.customers_ms == "candidates_url"
