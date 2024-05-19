from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import JsonValue
from starlette.responses import JSONResponse
from starlette import status
from db.db import get_session
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.model_reader import *
from typing import Annotated
from core.security import AuthHandler
import logging

from api.api_v1.services.user_services import UserService


router = APIRouter()
# dependencies=[Depends(oauth2_bearer), Depends(get_current_user)]
#user_dependency = Annotated[dict, Depends(get_current_user)]
auth_handler = AuthHandler()
logger = logging.getLogger()

@router.get("/")
async def get_readers(
                    session: AsyncSession = Depends(get_session), 
                    q: Annotated[str | None, Query(max_length=20)]=None,
                    user = Depends(auth_handler.auth_wrapper)
                    ):
    # if user is None:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    readers = await session.execute(select(Reader))

    if q is not None:
        readers = await session.execute(select(Reader).where(Reader.name == q))
        readers_result = readers.scalar()
        return {"readers": [reader for reader in readers_result]}
    else:
        readers = readers.scalars().all()
        return {"total": len(readers), "readers": [reader for reader in readers]}
    

# @router.get("/{reader_id}")
# async def get_reader(reader_id: Annotated[int, Path(title='The id')], session: AsyncSession = Depends(get_session)):
#     reader = await session.exec(select(Reader).where(Reader.id == reader_id)).first()
#     return reader

@router.get("/{reader_id}/blogs")
async def get_reader_blogs(reader_id: Annotated[int, Path(title='The reader id')], session: AsyncSession = Depends(get_session)):
    reader = await session.exec(select(Reader).where(Reader.id == reader_id)).first()
    return reader.blogs


# register
@router.post("/register")
async def create_reader(reader_data: ReaderCreate,user_service: UserService = Depends(), session: AsyncSession = Depends(get_session)):
    #reader = Reader(**reader_data.model_dump())
    reader_new = await user_service.register(reader_data, session)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=f"Successful!, User: {reader_new}")

@router.post('/login')
async def login(reader: ReaderLogin, user_service: UserService = Depends(), session: AsyncSession= Depends(get_session) ):
    token = await user_service.authenticate_user(reader, session=session)
    return {"access_token": token, "token_type": "bearer"}

@router.get('/me')
async def get_me(current_reader: JsonValue = Depends(auth_handler.auth_wrapper), user_service: UserService = Depends(), session:AsyncSession=Depends(get_session)):
    logger.debug(f"current reader: {current_reader} ")
    current_user = await user_service.get_me(current_reader['userid'], session)
    return current_user
