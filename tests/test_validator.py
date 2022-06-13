import pytest
from fastapi import HTTPException

from services.validator import validate_user_request

CORRECT_URL = "https://google.com"
INVALID_URL = "htps://google.com"


class MockRequest:
    """
    Original:
        class Request from Fastapi

    """
    def __init__(self, json_data):
        self.json_data = json_data

    async def json(self):
        return self.json_data


@pytest.mark.asyncio
async def test_no_url_validation():
    with pytest.raises(HTTPException) as error_info:
        no_url_request = MockRequest(json_data={"url": ''})
        await validate_user_request(no_url_request)

        assert error_info == HTTPException(status_code=400, detail="No URL Passed")


@pytest.mark.asyncio
async def test_invalid_url_validation():
    with pytest.raises(HTTPException) as error_info:
        invalid_url_request = MockRequest(json_data={"url": INVALID_URL})
        await validate_user_request(invalid_url_request)

        assert error_info == HTTPException(status_code=422, detail="Invalid URL")


@pytest.mark.asyncio
async def test_correct_url_validation():
    correct_url_request = MockRequest(json_data={"url": CORRECT_URL})
    result = await validate_user_request(correct_url_request)

    assert result == CORRECT_URL
