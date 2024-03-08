from pydantic import BaseModel

class RegisterTenant(BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    is_bussines: bool