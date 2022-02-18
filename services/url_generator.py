from string import ascii_letters
from random import choice

url_cache = {}

URL_FILLING = ascii_letters + '0123456789'


def generate_url_key() -> str:
    """Returns:
            Unique 6-character key for a short url
            http://short.est/ (GeAi9K)<- this is an example of a key

    """
    new_url_key = [choice(URL_FILLING) for _ in range(6)]
    new_url_key = ''.join(new_url_key)

    if new_url_key not in url_cache:
        return new_url_key

    return generate_url_key()
