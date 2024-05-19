from sqlmodel import SQLModel, Field, Relationship
from models.model_base import TimestampModel
from models.model_reader import Reader
from typing import Optional
from enum import Enum
from models.model_reader_blog import ReaderBlog
from pydantic import validator
class TypeCatoChoices(Enum):
    BOOK = 'Đọc sách'
    CONFIDE = 'Tâm sự'
    BLOG = 'Đọc Blog'
    NEWS = 'Tin tức'
    LEARN = 'Bài học'
    MODIVATION = 'Khích lệ'
    STORY = 'Kể chuyện'
    PRODUCTIVITY = 'Năng suất'
    RELAX = 'Giải trí'
    EXPERIENCE = 'Trãi nghiệm'

class BlogBase(SQLModel):
    title: str
    category: TypeCatoChoices
    read_time: int
    content: str
    summary: Optional[str] 
    img: str

class BlogCreate(BlogBase):
    pass

class BlogUpdate(TimestampModel):
    title: str | None = None
    category: TypeCatoChoices | None = None
    read_time: int | None = None
    content: str | None = None
    summary: str | None = None
    img: str | None = None
    


class BlogRead(BlogBase):
    id: int

# class BlogUpdate():
#     title: Optional[str]
#     category: Optional[TypeChoices]
#     read_time: Optional[int]
#     content: Optional[str]
#     summary: Optional[str]
#     img: Optional[str]


class Blog(BlogBase, TimestampModel, table = True):
    __tablename__ = "blog"
    id: Optional[int] = Field(default=None, primary_key=True)
    readers: list[Reader] = Relationship(back_populates="blogs", link_model=ReaderBlog)

    def __repr__(self):
        return f"Blog: {self.title}"