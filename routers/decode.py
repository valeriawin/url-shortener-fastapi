from fastapi import APIRouter, Request, HTTPException

from models.urlpair import URLPair
from services.url_generator import url_cache
from services.validator import validate_user_request

router = APIRouter()


@router.post("/decode", response_model=URLPair)
async def decode_url(request: Request) -> URLPair:
    """ Args:
            request: body should contain a key-value pair
                    (key - "url", value - URL to decode)

        Returns:
            URLPair as JSON with "short url" and "long url"

        Raises:
            HTTPException 400: If no URL passed
            HTTPException 404: If URL is not found in memory
            HTTPException 422: If invalid URL passed

    """
    user_url = await validate_user_request(request)

    url_key_index = user_url.rfind('/') + 1
    user_url_key = user_url[url_key_index:]

    try:
        return url_cache[user_url_key]
    except KeyError as exception:
        raise HTTPException(status_code=404, detail="URL Not Found") \
                from exception
