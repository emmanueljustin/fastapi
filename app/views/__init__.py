from fastapi import FastAPI

from app.views.intro import router as intro_router
from app.views.sample import router as sample_router
from app.views.authentication import router as auth_router

def include_routers(app: FastAPI):
  app.include_router(intro_router, prefix="/intro", tags=["Developer Introduction"])
  app.include_router(sample_router, prefix="/sample", tags=["Sample Endpoint"])
  app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
