import pytest

from app.commons.helpers import build_request_uri


class TestHelpers:
    @pytest.mark.asyncio
    async def test_build_request_uri(self):
        host = "fakehost.net"
        endpoint = "this/endpoint"
        test_uri = build_request_uri(host, endpoint)
        assert test_uri == "https://fakehost.net/this/endpoint"
