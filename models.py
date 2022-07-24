from sqlalchemy import Column, Integer, String
from database import Base


# Define To Do class inheriting from Base
class ToDo(Base):
    __tablename__ = 'todo_table'
    id = Column(Integer, primary_key=True)
    task = Column(String(256))
