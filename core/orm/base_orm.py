from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError

from core.database import async_session_maker
from core.logs.logs import logger_error


class BaseOrm:
    model = None

    @classmethod
    async def insert_data(cls, **kwargs):
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**kwargs)
                await session.execute(query)
                await session.commit()

        except (Exception, SQLAlchemyError) as e:
            if isinstance(e, SQLAlchemyError):
                logger_error.error(f"SQLAlchemy exception in insert_data: {str(e)}")
            else:
                logger_error.error(f"Unknown exception in insert_data: {str(e)}")

    @classmethod
    async def found_one_or_none(cls, **kwargs):
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__.columns).filter_by(**kwargs)
                result = await session.execute(query)
                return result.mappings().one_or_none()

        except (Exception, SQLAlchemyError) as e:
            if isinstance(e, SQLAlchemyError):
                logger_error.error(
                    f"SQLAlchemy exception in found_one_or_none: {str(e)}"
                )
            else:
                logger_error.error(f"Unknown exception in found_one_or_none: {str(e)}")
