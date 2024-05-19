from fastapi import APIRouter
from api.api_v1.endpoints.api_blog import router as blog_router
from api.api_v1.endpoints.api_reader import router as reader_router
from api.api_v1.endpoints.api_read_blog import router as reader_blog_router
from api.api_v1.endpoints.api_auth import router as auth_router
router = APIRouter()

router.include_router(blog_router, prefix="/blogs" , tags=["Blogs"])
router.include_router(reader_router, prefix="/readers", tags=["Readers"])
router.include_router(reader_blog_router, prefix="/readblog", tags=["ReadBlog"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
