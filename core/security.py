from datetime import timedelta, datetime
from typing import Annotated, Union, Any
from fastapi import APIRouter, Depends, HTTPException, Security

from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.model_reader import Reader
from passlib.context import CryptContext
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer
from jose import JWTError, jwt
from core.config import settings
from starlette.authentication import (
    AuthenticationBackend,
    AuthenticationError,
    AuthCredentials,
    UnauthenticatedUser
)

class AuthHandler:
    def __init__(self):
        self.SECRET_KEY = settings.SECRET_KEY
        self.ALGORITHM = settings.ALGORITHM
        self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_bearer = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

    def encode_token(self, user_id: int, username: str) -> str:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": username,
            "id": user_id,
            "exp": expire,
        }
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms = self.ALGORITHM)
            username: str= payload.get('sub')
            userid: int = payload.get('id')
            return {'username': username, "userid": userid}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        return self.decode_token(auth.credentials)
        
    
    def verify_password(self, plain_password, hashed_password):
        return self.bcrypt_context.verify(plain_password, hashed_password)
    def get_password_hash(self,password):
        return self.bcrypt_context.hash(password)
    
    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(HTTPBearer())):
        user_info = self.decode_token(auth.credentials)
        print(user_info)
        if user_info is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_info


