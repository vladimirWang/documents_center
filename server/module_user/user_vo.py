from typing import Annotated

from pydantic import BaseModel, Field

EmailStr = Annotated[str, Field(pattern=r"^.+@.+\..+$", description="邮箱")]

PasswordStr = Annotated[str, Field(description="密码", min_length=6, max_length=8)]


class UserLogin(BaseModel):
    email: EmailStr
    password: PasswordStr


class UserRegister(BaseModel):
    # username: str
    # age: int = Field(description="年龄", gt=0)
    # email: str | None = None
    email: EmailStr
    password: PasswordStr
