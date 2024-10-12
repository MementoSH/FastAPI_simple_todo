from pydantic import BaseModel

class Task(BaseModel):
    id: int
    description: str
    status: str
    created_at: str
    updated_at: str

class TaskCreate(BaseModel):
    description: str

class TaskUpdate(BaseModel):
    description: str

class TaskStatusUpdate(BaseModel):
    status: str