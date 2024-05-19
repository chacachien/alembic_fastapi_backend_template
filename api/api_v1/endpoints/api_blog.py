from email import message
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from db.db import get_session
from sqlmodel import select, delete
from sqlalchemy.ext.asyncio.session import AsyncSession
from models.model_blog import *
from typing import Annotated
from core.security import AuthHandler
from api.api_v1.services.user_services import UserService
import logging
logger = logging.getLogger()
auth_handler = AuthHandler()

router = APIRouter()

@router.get("/", status_code=200)
async def get_blogs(
                    session: AsyncSession = Depends(get_session), 
                    q: Annotated[str | None, Query(max_length=20)]=None,
                    ):
    try:

        if q:
            if q.upper() not in [choice.name for choice in TypeCatoChoices]:
                raise HTTPException(status_code=400, detail=f"Invalid category: {q}")
        query = select(Blog)
        result = await session.execute(query)
        blogs = result.scalars().all()
        
        if not blogs:
            raise HTTPException(status_code=404, detail=f"No blogs with the category {q} found")

        return {"total": len(blogs), "blogs": blogs}
    
    except HTTPException as he:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)})")

@router.get("/{blog_id}")
async def get_blog(blog_id: Annotated[int, Path(title='The id')], session: AsyncSession = Depends(get_session)):
    try:
        # Execute the query to retrieve the blog with the specified ID
        query = select(Blog).where(Blog.id == blog_id)
        result = await session.execute(query)
        blog = result.scalar()

        if not blog:
            raise HTTPException(status_code=404, detail=f"Blog with id {blog_id} not found")
            
        return blog

    except HTTPException as he:
        raise
    
    except Exception as e:
        # Handle unexpected errors gracefully
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/")
async def create_blog(blog_data: BlogCreate, session: AsyncSession = Depends(get_session), user = Depends(auth_handler.get_current_user)):
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        logger.info(f"User {user['userid']} is trying to get blogs")
        user_info = await UserService.get_me(user['userid'], session)

        if not user_info.is_superuser:
            raise HTTPException(status_code=403, detail="Forbidden")

        # Create a new Blog instance using the provided data
        blog = Blog(**blog_data.model_dump())
        # Add the blog to the session, commit the transaction, and refresh the blog to populate auto-generated values
        print(blog)
        session.add(blog)
        await session.commit()
        await session.refresh(blog)
        
        return blog
    except Exception as e:
        # Handle unexpected errors gracefully
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@router.patch("/{blog_id}")
async def update_blog(
    blog_id: int,
    blog_data: BlogUpdate,
    session: AsyncSession = Depends(get_session),
   
):
    try:
        # Retrieve the blog to update
        query = select(Blog).where(Blog.id == blog_id)
        result = await session.execute(query)
        blog = result.scalar()
        print("BLOG: ", blog)
        if not blog:
            raise HTTPException(status_code=404, detail=f"Blog with id {blog_id} not found")

        # Update the blog data
        for field, value in blog_data.model_dump(exclude_unset=True).items():
            setattr(blog, field, value)

        # Commit the transaction
        session.add(blog)
        await session.commit()

        # Refresh the blog to reflect the changes
        await session.refresh(blog)

        return blog
    except HTTPException as he:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.delete("/{blog_id}")
async def delete_blog(blog_id: int, session: AsyncSession = Depends(get_session)):
    try:
        # Retrieve the blog to delete
        query = select(Blog).where(Blog.id == blog_id)
        result = await session.execute(query)
        blog = result.scalar()

        if not blog:
            raise HTTPException(status_code=404, detail=f"Blog with id {blog_id} not found")

        # Delete the blog
        delete_query = delete(Blog).where(Blog.id == blog_id)
        await session.execute(delete_query)
        await session.commit()

        return {"message": f"Blog with id {blog_id} deleted successfully"}
    except HTTPException as he:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")