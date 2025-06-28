from typing import Optional

from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine


# Define the Todo model
class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    priority: int = Field(default=0)
    completed: bool = Field(default=False)

# Create the SQLite database engine
engine = create_engine("sqlite:///todo.db", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)  # Ensures no duplicate table definitions

# Initialize FastAPI app
app = FastAPI()

# Dependency: Provide a database session
def get_session():
    with Session(engine) as session:
        yield session

# Event to create tables only once during application startup
# @app.on_event("startup")
# def on_startup():
#     SQLModel.metadata.create_all(engine)  # Ensures no duplicate table definitions

@app.get("/")
async def get_all_todo(session: Session = Depends(get_session)):
    return session.exec(Todo.select()).all()

@app.post("/")
async def create_todo(todo: Todo, session: Session = Depends(get_session)):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True, workers=1)