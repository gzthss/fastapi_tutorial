from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


database_url = "postgresql+asyncpg://postgres:admin123@192.168.1.11:5432/postgres"

engine = create_async_engine(database_url, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with async_session() as session:
        yield session

async def init_db():
    print("init_db start")
    print(f"Connecting to database as: {engine.url.username}")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("init_db end")









