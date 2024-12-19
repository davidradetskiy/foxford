import asyncio

from fastapi import FastAPI

from app.dao import create_appreal
from app.mock import create_mock_users
from app.routers import router
from app.utils import get_data_from_email

app = FastAPI(title="ServiceDesk")


async def periodic_get_data():
    while True:
        result = await get_data_from_email()
        await create_appreal(result)
        await asyncio.sleep(30)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_get_data())
    await create_mock_users()


app.include_router(router, prefix="/api")
