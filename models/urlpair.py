from pydantic import BaseModel, AnyUrl


class URLPair(BaseModel):
    short_url: AnyUrl
    long_url: AnyUrl
