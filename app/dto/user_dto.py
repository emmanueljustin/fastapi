from pydantic import BaseModel

class Loginrequest(BaseModel):
  username: str
  password: str


class RegisterRequest(BaseModel):
  username: str
  email: str
  password: str
