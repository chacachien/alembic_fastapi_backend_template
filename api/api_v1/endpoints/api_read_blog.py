# api when reader read a blog, add it into the table

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from db.db import get_session
from sqlmodel import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.model_blog import Blog, BlogCreate
from models.model_reader import Reader
from models.model_reader_blog import ReaderBlog


router = APIRouter(prefix="/readblog", tags=["Readers"])

# @router.get("/")
# async def get_reader_blog(session: AsyncSession = Depends(get_session), 
#                     reader_id: int = Query(None, title='The id of the reader'),
#                     blog_id: int = Query(None, title='The id of the blog'),
#                     ):
#     try:
#         if reader_id is not None and blog_id is not None:
#             reader_blog = session.exec(select(ReaderBlog).where(ReaderBlog.reader_id == reader_id and ReaderBlog.blog_id == blog_id)).first()
#             return reader_blog
#         elif reader_id is None and blog_id is not None:
#             reader_blog = session.exec(select(ReaderBlog)).all()
#             return reader_blog
#         elif reader_id is not None:
#             reader_blog = session.exec(select(ReaderBlog).where(ReaderBlog.reader_id == reader_id)).all()
#             return reader_blog
#         else:
#             reader_blog = session.exec(select(ReaderBlog).where(ReaderBlog.blog_id == blog_id)).all()
#             return reader_blog
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

    
@router.get("/")
async def update_reader_blog(reader_id: int = Query(None, title='The id of the reader'), 
                            blog_id: int = Query(None, title='The id of the blog'), 
                            session: AsyncSession = Depends(get_session)):
    try:
        reader = await session.exec(select(Reader).where(Reader.id == reader_id)).first()
        blog = await session.exec(select(Blog).where(Blog.id == blog_id)).first()
        blog.readers.append(reader)
        await session.add(blog)
        await session.commit()

        print("update reader blog", blog.readers)
        print("update reader blog", reader.blogs)

        return blog
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
