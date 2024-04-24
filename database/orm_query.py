from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Engineer


async def orm_add_engineer(session: AsyncSession, data: dict):
    obj = Engineer(user_id=int(data['user_id']),
                   firstname=data['firstname'],
                   surname=data['surname'],
                   phone=data['phone'])
    session.add(obj)
    await session.commit()


async def orm_get_engineers(session: AsyncSession):
    query = select(Engineer)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_engineer(session: AsyncSession, engineer_id: int):
    query = select(Engineer).where(Engineer.id == engineer_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_delete_engineer(session: AsyncSession, engineer_id: int):
    query = delete(Engineer).where(Engineer.id == engineer_id)
    await session.execute(query)
    await session.commit()
