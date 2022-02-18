from json.decoder import JSONDecodeError

from validators import url
from fastapi import HTTPException, Request


async def validate_user_request(request: Request) -> str:
    """ Args:
            request: JSON in request body with a key-value pair
                (key - "url", value - URL to encode)

        Returns:
            URL from value

        Raises:
            HTTPException 400: If no URL passed
            HTTPException 422: If invalid URL passed

    """
    try:
        request_data = await request.json()
    except JSONDecodeError as exception:
        raise HTTPException(status_code=400, detail="No URL Passed") \
                from exception

    user_url = request_data['url']

    if not url(user_url):
        raise HTTPException(status_code=422, detail="Invalid URL")

    return user_url
