from typing import List

from sqlalchemy import String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class Engineer(Base):
    __tablename__ = 'engineer'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(unique=True)
    firstname: Mapped[str] = mapped_column(String(100), nullable=True)
    surname: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)


class Object(Base):
    __tablename__ = 'object'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(150), nullable=False)
    engineer_id: Mapped[int] = mapped_column(ForeignKey('engineer.id', ondelete='CASCADE'), nullable=False)
    checked: Mapped[bool] = mapped_column(Boolean, default=False)

    blocks: Mapped[List['Block']] = relationship('Block', back_populates='object')
    engineer: Mapped['Engineer'] = relationship(backref='object')


class Block(Base):
    __tablename__ = 'block'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[int] = mapped_column(String(100), nullable=False)
    checked: Mapped[bool] = mapped_column(Boolean, default=False)
    object_id: Mapped[int] = mapped_column(ForeignKey('object.id', ondelete='CASCADE'), nullable=False)
    engineer_id: Mapped[int] = mapped_column(ForeignKey('engineer.id', ondelete='CASCADE'), nullable=False)

    object: Mapped['Object'] = relationship('Object', back_populates='blocks')
    engineer: Mapped['Engineer'] = relationship(backref='block_engineer')


class CheckList(Base):
    __tablename__ = 'checklist'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    block_id: Mapped[int] = mapped_column(ForeignKey('block.id', ondelete='CASCADE'), nullable=False)
    scheme: Mapped[bool] = mapped_column(Boolean, default=False)
    one_c: Mapped[bool] = mapped_column(Boolean, default=False)
    equipment: Mapped[bool] = mapped_column(Boolean, default=False)
    location: Mapped[bool] = mapped_column(Boolean, default=False)
    optimal: Mapped[bool] = mapped_column(Boolean, default=False)

    address: Mapped['Block'] = relationship(backref='checklist')
