from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import *
from datetime import datetime
from typing import List, Optional
import csv
from typing import Optional


async def crear_boleto(ticket: boleto, session:AsyncSession) -> boleto:
    session.add(ticket)
    await session.commit()
    await session.refresh(ticket)
    return ticket




async def get_all_fly (session: AsyncSession) -> List[boleto]:
    result = await session.execute(select(boleto))
    return result.all()


async def modificar()