from models.model_base import TimestampModel
from sqlmodel import Field, Relationship, SQLModel

class ReaderBlogBase(SQLModel):
    reader_id: int| None = Field(foreign_key="reader.id", primary_key=True)
    blog_id: int| None = Field(foreign_key="blog.id", primary_key=True)

class ReaderBlog(ReaderBlogBase,TimestampModel, table = True):
    __tablename__ = "reader_blog"
    def __repr__(self):
        return f"UserBlog: {self.reader_id} - {self.blog_id}, read at {self.created_at}"


