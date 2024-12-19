from sqlalchemy import delete, insert, select, update

from app.models import Appeal, User
from database import async_session_maker


async def create_appreal(apprels: list[dict]):
    async with async_session_maker() as session:
        for apprel in apprels:
            stmt = insert(Appeal).values(
                {"message": apprel["body"], "email": apprel["sender"], "status": "add"}
            )
            await session.execute(stmt)
            await session.commit()


async def get_user_by_code(user_code: str):
    async with async_session_maker() as session:
        stmt = select(User).where(User.code == user_code)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def get_appeal_by_id(id_appeal: int):
    async with async_session_maker() as session:
        stmt = select(Appeal).where(Appeal.id == id_appeal)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def done_appeal_(id_appeal: int):
    async with async_session_maker() as session:
        stmt = update(Appeal).where(Appeal.id == id_appeal).values(status="done")
        await session.execute(stmt)
        await session.commit()


async def get_appreals(status=None, date_sort="desc"):
    async with async_session_maker() as session:
        query = select(Appeal)

        if status:
            query = query.where(Appeal.status == status)

        if date_sort == "asc":
            query = query.order_by(Appeal.datetime.asc())
        else:
            query = query.order_by(Appeal.datetime.desc())

        result = await session.execute(query)
        appeals = result.scalars().all()

    return appeals


async def create_user(user: dict):
    async with async_session_maker() as session:
        stmt = select(User).where(User.code == user["code"])
        result = await session.execute(stmt)
        user_in_db = result.scalar_one_or_none()

        if user_in_db is None:
            stmt = insert(User).values(user)
            await session.execute(stmt)
            await session.commit()
