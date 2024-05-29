from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from database.models import Engineer, Object, Block, CheckList


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


async def orm_get_object(session: AsyncSession, object_id: int):
    query = select(Object).where(Object.id == object_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_add_object(session: AsyncSession, data: dict):
    obj = Object(address=data['address'],
                 engineer_id=data['engineer_id'])
    session.add(obj)
    await session.commit()


async def orm_get_objects_checked(session: AsyncSession, checked: bool):
    if checked:
        query = select(Object).filter(Object.checked == checked).options(subqueryload(Object.engineer),
                                                                         subqueryload(Object.blocks).subqueryload(
                                                                             Block.engineer))
    else:
        query = select(Object).filter(Object.checked == checked).options(subqueryload(Object.engineer))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_blocks_object(ids: int, session: AsyncSession):
    query = select(Block).filter(Block.object_id == ids).options(subqueryload(Block.engineer))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_add_block(data: dict, session: AsyncSession):
    obj = Block(name=data['name'],
                object_id=data['object_id'],
                engineer_id=data['engineer_id'])
    session.add(obj)
    await session.commit()


async def orm_add_check_list(data: dict, session: AsyncSession):
    obj = CheckList(block_id=data['block_id'],
                    scheme=data['scheme'],
                    one_c=data['one_c'],
                    equipment=data['equipment'],
                    location=data['location'],
                    optimal=data['optimal'])
    session.add(obj)
    await session.commit()
    query_block = select(Block).where(Block.id == data['block_id'])
    result_block = await session.execute(query_block)
    block = result_block.scalars().one()
    block.checked = True

    query_object = select(Object).where(Object.id == block.object_id).options(subqueryload(Object.blocks))
    result_object = await session.execute(query_object)
    object_bl = result_object.scalars().one()
    for block in object_bl.blocks:
        if not block.checked:
            break
    else:
        object_bl.checked = True
    await session.commit()
