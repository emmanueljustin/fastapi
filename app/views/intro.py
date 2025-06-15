from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from app.controllers.auth import get_current_user


router = APIRouter(
	dependencies=[Depends(get_current_user)],
)

@router.get("/")
async def get_intro():
	"""
	About me.
	"""
	try:
		return JSONResponse(
			status_code=status.HTTP_200_OK,
			content={
				"name": "Emmanuel Justin Atienza",
				"role": "Software Engineer",
				"description": "A passionate software engineer with a focus on building efficient and scalable applications.",
				"interests": [
					"Mobile Development",
					"Fullstack Development",
					"Cloud Computing"
				],
			}
		)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=str(e)
		)