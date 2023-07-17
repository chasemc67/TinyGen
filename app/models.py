from pydantic import BaseModel

class RequestRecord(BaseModel):
    url: str
    prompt: str