from pydantic import BaseModel


class AsyncResponse(BaseModel):
    message: str
