from pydantic import BaseModel

class ClientCreate(BaseModel):
    email: str
    mobile: str | None = None
    password: str