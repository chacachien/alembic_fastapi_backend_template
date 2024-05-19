
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWSError, JWTError
from db.db import get_session
from sqlmodel import select, delete
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.model_reader import *
from typing import Annotated
router = APIRouter()




# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def create_user(user_data: ReaderCreate, session: AsyncSession = Depends(get_session)):
#     try:
#         create_user_model = Reader(
#             username = user_data.username,
#             hashed_password=get_password_hash(user_data.password),
#             email = user_data.email,
#             full_name = user_data.full_name,
#             is_active = user_data.is_active,
#             is_superuser = user_data.is_superuser
#         )
#         session.add(create_user_model)
#         await session.commit()

#         return create_user_model
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# @router.post("/token", response_model=Token)
# async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], session: AsyncSession = Depends(get_session)):
#     user = await authenticate_user(form_data.username, form_data.password, session)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
#     token = create_access_token(user.id, user.username)

#     return {"access_token": token, "token_type": "bearer"}



# async def authenticate_user(username:str, password: str, session: AsyncSession):
#     query = select(Reader).where(Reader.username == username)
#     result = await session.execute(query)
#     user = result.scalar()
#     print(user)

#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# async def get_user(token):
#     try:
#         user = get_current_user(token)
#         if user.username is None or user.user_id is None:
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
#         return user
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user.")