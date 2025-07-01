from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI
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
    return session.exec(select(Todo)).all()

def save_data(session: Session, todo: Todo):
    session.add(todo)
    session.commit()
    # return todo
    return session.exec(select(Todo)).all()

@app.post("/", response_model=list[Todo], status_code=201)
async def create_todo(todo: Todo, session: Session = Depends(get_session)):
    # todo.completed = True if todo.completed == 'on' else False
    print("todo", todo.dict())
    return save_data(session, todo)

@app.delete('/{id}', response_model=list[Todo], status_code=201)
async def delete_todo(id: int, session: Session = Depends(get_session)):
    todo = session.exec(select(Todo).where(Todo.id == id)).one()
    # todo = session.get(Todo, id)
    session.delete(todo)
    session.commit()
    return session.exec(select(Todo)).all()

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
    todo = session.exec(select(Todo).where(Todo.id == id)).one()
    todo = Todo(**todo.dict())
    session.commit()
    return session.exec(select(Todo)).all()