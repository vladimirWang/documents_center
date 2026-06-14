from pydantic import BaseModel, Field


class user_login(BaseModel):
    username: str = Field(description="用户名")
    password: str = Field(description="密码", min_length=6, max_length=8)


class user_register(BaseModel):
    name: str
    age: int = Field(description="年龄", gt=0)
    email: str | None = None
