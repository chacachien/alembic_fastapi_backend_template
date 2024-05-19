from fastapi import Depends
from db.db import get_session
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.model_reader import *
from fastapi import HTTPException
from core.security import AuthHandler
from starlette import status


auth_handler = AuthHandler()
class UserService(object):
    __instance = None
    def __init__(self) -> None:
        pass

    @staticmethod
    async def authenticate_user(reader: ReaderLogin, session: AsyncSession):
        query = select(Reader).where(Reader.username == reader.username)
        result = await session.execute(query)
        reader_found = result.scalar()
        print(reader_found)
        if not reader_found:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
        elif not auth_handler.verify_password(reader.password, reader_found.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
        else:
            token = auth_handler.encode_token(reader_found.id, reader_found.username)
            return token
        
    @staticmethod
    async def register(reader: ReaderCreate, session: AsyncSession):
        try:
            reader_new = Reader(
                username = reader.username,
                hashed_password=auth_handler.get_password_hash(reader.password),
                email = reader.email,
                full_name = reader.full_name,
                is_active = reader.is_active,
                is_superuser = reader.is_superuser
            )
            session.add(reader_new)
            await session.commit()

            await session.refresh(reader_new)
            return reader_new
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=str(e))
    
    @staticmethod
    async def get_me(reader_id: int, session: AsyncSession):
        try:
            query = select(Reader).where(Reader.id == reader_id)
            result = await session.execute(query)
            reader = result.scalar()
            return reader
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = str(e))
        