import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


load_dotenv()

CLEVER_DB = (
    f"postgresql+asyncpg://{os.getenv('CLEVER_USER')}:" 
    f"{os.getenv('CLEVER_PASSWORD')}@{os.getenv('CLEVER_HOST')}:" 
    f"{os.getenv('CLEVER_PORT')}/{os.getenv('CLEVER_DATABASE')}"
)

engine: AsyncEngine = create_async_engine(CLEVER_DB, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session
