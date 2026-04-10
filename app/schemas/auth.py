from pydantic import Field, EmailStr

from app.schemas.base import RequestSchema, ResponseSchema


class RegisterRequest(RequestSchema):
	username: str = Field(min_length=3, max_length=50)
	email: EmailStr
	password: str = Field(min_length=8, max_length=128)

class LoginRequest(RequestSchema):
	email: EmailStr
	password: str = Field(min_length=8, max_length=128)

class UserResponse(ResponseSchema):
	id: int