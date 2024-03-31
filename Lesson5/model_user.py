from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: int
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
