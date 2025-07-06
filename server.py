import json
import traceback
from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    priority: int = Field(default=0)
    completed: bool = Field(default=False)


engine = create_engine("sqlite:///todo2.db", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)  # Ensures no duplicate table definitions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/", response_model=list[Todo])
async def get_all_todo(session: Session = Depends(get_session)):
    # todos = session.exec(select(Todo)).all()
    todos = session.query(Todo).all()
    # print("todos", todos)
    return todos

# @app.post('/test')
# async def post_test(data: dict):
#     print(data)
#     return data

@app.post('/', status_code=201)
async def create_todo(todo: Todo, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()
    return session.exec(select(Todo)).all()

@app.delete('/{id}', response_model=list[Todo], status_code=200)
def delete_todo(id: int, session: Session = Depends(get_session)):
    # print("id", id)
    # todo = session.get(Todo, id)
    # todo = session.exec(select(Todo).where(Todo.id == id)).one()
    # todo = session.exec(select(Todo).filter(Todo.id == id)).one_or_none()
    # todo = session.query(Todo).filter(Todo.id == id).first()
    # todo = session.query(Todo).get(id)
    todo = session.query(Todo).where(Todo.id == id).one()
    session.delete(todo)
    session.commit()
    todos = [todo.dict() for todo in session.exec(select(Todo)).all()]
    return todos

app.get('/{id}', response_model=Todo)
async def get_single_todo(id: int, session: Session = Depends(get_session)):
    return session.exec(select(Todo).where(Todo.id == id)).one()

@app.patch('/{id}', response_model=list[Todo], status_code=201)
async def modify_todo(id: int, session: Session = Depends(get_session)):
    todo = session.exec(select(Todo).where(Todo.id == id)).one()
    todo.completed = not todo.completed
    session.commit()
    return session.exec(select(Todo)).all()

@app.put('/{id}', response_model=list[Todo], status_code=201)
async def update_todo(id: int, todo: Todo, session: Session = Depends(get_session)):
    db_todo = session.exec(select(Todo).where(Todo.id == id)).one()
    # print("db_todo", db_todo)
    # db_todo.title = todo.title
    # db_todo.priority = todo.priority
    # db_todo.completed = todo.completed
    todo_data = todo.model_dump(exclude={'id'}, exclude_unset=True)
    db_todo.sqlmodel_update(todo_data)
    # session.add(db_todo)
    session.commit()
    return session.exec(select(Todo)).all()


