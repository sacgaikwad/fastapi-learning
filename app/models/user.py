from pydantic import BaseModel, EmailStr, field_validator

class UserRequest(BaseModel):
    name: str
    age: int
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        domain = value.split("@")[1]

        if domain != "gmail.com":
            raise ValueError(
                "Email must be a gmail.com address"
            )
        return value

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value <= 18:
            raise ValueError(
                "Age must be greater than 18"
            )
        return value


class UserResponse(BaseModel):
    user_id: int


class UserDetailResponse(BaseModel):
    user_id: int
    name: str
    age: int
    email: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    user_id: int
    name: str
    email: str  