from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: int


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    user_id: int
    user_hash: str
