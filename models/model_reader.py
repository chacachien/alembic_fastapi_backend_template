from pydantic import validator
from sqlmodel import Field, SQLModel, Relationship
from models.model_base import TimestampModel

from models.model_reader_blog import ReaderBlog

class ReaderBase(SQLModel):
    username: str
    email: str|None= Field(unique = True, index = True)
    full_name: str | None = None
    is_active: bool| None = Field(default=True)
    is_superuser: bool| None = Field(default=False)

        
class ReaderCreate(ReaderBase):
    password: str = Field(max_length=256, min_length=5)
    password2: str
    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v
    

class ReaderLogin(SQLModel):
    username: str
    password: str

class Reader(ReaderBase, TimestampModel, table = True):
    __tablename__ = "reader"
    id: int|None = Field(default=None, primary_key=True)
    hashed_password: str| None = None

    blogs: list["Blog"] = Relationship(back_populates="readers", link_model=ReaderBlog)

    def __repr__(self):
        return f"User: {self.email}"
    

class Token(SQLModel):
    access_token: str
    token_type: str
