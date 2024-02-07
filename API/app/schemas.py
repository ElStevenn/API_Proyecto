from pydantic import BaseModel, Field
from typing import Optional, List

"""
    Sechemas Definition

"""

class UserBase(BaseModel):
    username: str
 

class UserCreate(UserBase):
    constrasena: str
    email: str
    edad: Optional[str] = None

class UserLogin(UserBase):
    password: str
