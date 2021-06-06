from pydantic import BaseModel
from typing import Optional

class Kinkster(BaseModel):
    firstName: str
    lastName: str
    phoneNumber: str
    locationRegion: str
    locationName: str

class RegisterRequest(BaseModel):
    emailAddress: str
    password: str
    firstName: str
    lastName: bool