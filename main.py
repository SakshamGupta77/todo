from fastapi import FastAPI, status, HTTPException
from database import Base, engine
from sqlalchemy.orm import Session
import models
import schemas


# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()


# fast api loads configs of web server in app


@app.get("/todo")
def retrieve_all_items():
    session = Session(bind=engine, expire_on_commit=False)

    todo_list = session.query(models.ToDo).all()

    session.close()
    return todo_list


@app.get("/todo/{id}")
def retrieve_item(id: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    todo = session.query(models.ToDo).get(id)

    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo


# page refresh is always a get call
@app.post("/todo", status_code=status.HTTP_201_CREATED)
def insert_item(todo: schemas.ToDo):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the ToDo database model
    todo_db = models.ToDo(task=todo.task)

    session.add(todo_db)
    session.commit()

    todo_id = todo_db.id

    session.close()

    return {"message": f"creating a new item: {todo_id}"}


@app.put("/todo/{id}")
def update_item(id: int, todo_request: schemas.ToDo):
    session = Session(bind=engine, expire_on_commit=False)
    # exception handling
    try:
        todo = session.query(models.ToDo).get(id)

        if todo:
            todo.task = todo_request.task
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

        return todo
    finally:
        session.close()


@app.delete("/todo/{id}")
def delete_in_list(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    try:
        todo = session.query(models.ToDo).get(id)

        if todo:
            session.delete(todo)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

        return None
    finally:
        session.close()
