import logging

from psycopg import AsyncConnection
from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


def build_pg_conninfo(
    db_name: str, host: str, port: int, user: str, password: str
) -> str:
    conninfo = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    return conninfo


async def log_db_version(connection: AsyncConnection) -> None:
    try:
        async with connection.cursor() as cursor:
            await cursor.execute("SELECT version();")
            db_version = await cursor.fetchone()
            logger.info(
                f"Connection to PostgreSQL established. PostgreSQL version: {db_version['version']}"
            )
    except Exception as e:
        logger.error("Failed to establish connection to PostgreSQL")


async def get_pg_pool(
    db_name: str,
    host: str,
    port: int,
    user: str,
    password: str,
    min_size: int = 1,
    max_size: int = 3,
    timeout: float | None = 30.0,
) -> AsyncConnectionPool:
    try:
        db_pool = AsyncConnectionPool(
            conninfo=build_pg_conninfo(
                db_name=db_name, host=host, port=port, user=user, password=password
            ),
            min_size=min_size,
            max_size=max_size,
            timeout=timeout,
            open=False,
        )
        await db_pool.open()
        async with db_pool.connectino() as connection:
            await log_db_version(connection=connection)
        return db_pool
    except Exception as e:
        logger.exception("Failed to initialize PostgreSQL pool: %s", e)
        raise
