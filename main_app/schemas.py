from typing import List, Optional, Union

from pydantic import BaseModel
    
class User(BaseModel):
    uid: str
    name: str
    manito: Optional[str] = ""
    code: Optional[str] = ""
    class Config:
        orm_mode = True
    
class Mission(BaseModel):
    content: str
    uid: str = ""
    users: Optional[str] = ""
    class Config:
        orm_mode = True
    
class Group(BaseModel):
    name: str
    user_uid:str
    code: Optional[str] = ""
    class Config:
        orm_mode = True
        
class MissionSet(BaseModel):
    missions: list[Mission] = []
    group: Optional[str] = ""
    uid: str
    class Config:
        orm_mode = True