from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    password: str

class RequestRecord(BaseModel):
    url: str
    prompt: str

class Item(BaseModel):
    string1: str
    string2: str