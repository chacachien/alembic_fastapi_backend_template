from fastapi import FastAPI
from fastapi.security import OAuth2
from core.config import settings
from api.api_v1.api import router as api_router
from starlette.middleware.authentication import AuthenticationMiddleware
import logging


logging.config.fileConfig(settings.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
app = FastAPI(title="Blogs API", openapi_url=f"{settings.API_V1_STR}/openapi.json")
app.include_router(api_router, prefix=settings.API_V1_STR) 


#app.add_middleware(AuthenticationMiddleware, backend = JWTAuth())