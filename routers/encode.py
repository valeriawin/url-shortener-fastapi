from fastapi import APIRouter, Request

from models.urlpair import URLPair
from services.validator import validate_user_request
from services.url_generator import generate_url_key, url_cache

router = APIRouter()


@router.post("/encode", response_model=URLPair)
async def encode_url(request: Request) -> URLPair:
    """ Args:
            request: body should contain a key-value pair
                    (key - "url", value - URL to encode)

        Returns:
            URLPair as JSON with "short url" and "long url"

        Raises:
            HTTPException 400: If no URL passed
            HTTPException 422: If invalid URL passed

    """
    user_url = await validate_user_request(request)

    for url_pair in url_cache.values():
        if url_pair.long_url == user_url:
            return url_pair

    url_key = generate_url_key()
    user_short_url = 'http://short.est/' + url_key
    url_cache[url_key] = URLPair(short_url=user_short_url, long_url=user_url)

    return url_cache[url_key]
