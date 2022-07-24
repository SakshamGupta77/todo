from pydantic import BaseModel


# Create ToDoRequest Base Model
class ToDo(BaseModel):
    task: str
