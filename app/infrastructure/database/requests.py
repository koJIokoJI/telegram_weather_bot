from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models import Users


async def insert_user(
    session: AsyncSession,
    telegram_id: int,
    default_city: str = "",
    cities: list[str] = [],
    mailing_agreement: bool = False,
):
    # if default_city == "":
    #     default_city = await session.execute(
    #         select(Users.default_city).where(Users.telegram_id == telegram_id)
    #     )
    # if cities == []:
    #     cities = await session.execute(
    #         select(Users.cities).where(Users.telegram_id == telegram_id)
    #     )
    statement = insert(Users).values(
        {
            "telegram_id": telegram_id,
            "default_city": default_city,
            "cities": cities,
            "mailing_agreement": mailing_agreement,
        }
    )
    statement = statement.on_conflict_do_update(
        index_elements=["telegram_id"],
        set_={
            "default_city": default_city,
            "cities": cities,
            "mailing_agreement": mailing_agreement,
        },
    )
    await session.execute(statement=statement)
    await session.commit()


async def get_user(session: AsyncSession, telegram_id: int):
    statement = select(Users).where(Users.telegram_id == telegram_id)
    user = await session.execute(statement=statement)
    return user.scalar()


async def get_users(session: AsyncSession):
    statement = select(Users.telegram_id, Users.default_city)
    users = await session.execute(statement=statement)
    return users


async def get_default_city(session: AsyncSession, telegram_id: int):
    statement = select(Users.default_city).where(Users.telegram_id == telegram_id)
    default_city = await session.execute(statement=statement)
    return default_city.scalar()
