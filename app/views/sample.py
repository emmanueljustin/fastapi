from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
async def sample():
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
      "message": "This is a sample response from the sample endpoint.",
    }
  )