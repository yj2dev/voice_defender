from pydantic import BaseModel


class UserRegister(BaseModel):
    phone_no: str
