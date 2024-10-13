from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Config


engine = create_async_engine(Config.DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Асинхронный генератор для получения сеанса базы данных.

    Этот генератор используется для создания и управления жизненным циклом сеанса базы данных.
    Он создаёт сеанс при входе в контекст и автоматически закрывает его при выходе.

    Returns:
        AsyncGenerator[AsyncSession, None]: Генератор, который возвращает объект `AsyncSession`.
    """
    async with async_session() as session:
        yield session
