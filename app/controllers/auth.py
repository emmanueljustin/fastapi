from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.user_model import UserModel
from app.database.postgre import get_db
from app.config.settings import settings
from app.core.security import verify_password

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(db: Session, username: str, password: str):
  user = db.query(UserModel).filter(UserModel.username == username). first()

  if not user:
    return False
  
  if not verify_password(password, user.hashed_password):
    return False
  
  return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
  )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")

    if username is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  
  user = db.query(UserModel).filter(UserModel.username == username).first()

  if user is None:
    raise credentials_exception
  
  return user
