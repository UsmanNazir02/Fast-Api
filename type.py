
from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    name: str
    age: int | None = None
    gender: Optional[str] = None 
    email: Optional[str] = None  

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):  
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None

class StudentOut(StudentBase):
    id: int

# New model for agent commands
class AgentCommand(BaseModel):
    prompt: str