from fastapi import FastAPI

from .routers import encode, decode

app = FastAPI()

app.include_router(encode.router)
app.include_router(decode.router)


@app.get("/")
async def root():
    return {
        "message": "Available Endpoints: /encode, /decode"
    }
