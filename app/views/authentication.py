from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.dto.user_dto import Loginrequest, RegisterRequest
from sqlalchemy.orm import Session
from app.database.postgre import get_db
from app.controllers.auth import authenticate_user, get_current_user
from app.core.security import create_access_token, get_password_hash
from app.models.user_model import UserModel

router = APIRouter()

@router.get("/check")
async def check(current_user: UserModel = Depends(get_current_user)):
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
      "message": "User is authenticated",
      "user_id": current_user.id,
      "username": current_user.username,
      "email": current_user.email
    }
  )

@router.post("/login")
async def login(request: Loginrequest, db: Session = Depends(get_db)):
  user = authenticate_user(db, request.username, request.password)

  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  
  access_token = create_access_token(data={"sub": user.username})
  return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={
      "access_token": access_token,
      "token_type": "Bearer"
    }
  )


@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
  user = db.query(UserModel).filter((UserModel.username == request.username) | (UserModel.email == request.email)).first()

  if user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
  
  hashed_password = get_password_hash(request.password)

  new_user = UserModel(
    username=request.username,
    email=request.email,
    hashed_password=hashed_password
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  user = authenticate_user(db, request.username, request.password)
  access_token = create_access_token(data={"sub": user.username})

  return JSONResponse(
    status_code=status.HTTP_201_CREATED,
    content={
      "message": "User registered successfully",
      "user_id": new_user.id,
      "username": new_user.username,
      "email": new_user.email,
      "access_token": access_token,
      "token_type": "Bearer"
    }
  )
