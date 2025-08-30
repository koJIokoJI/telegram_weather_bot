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
    return user.first()
