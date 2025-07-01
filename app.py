# import json
# import traceback
# from typing import Any, Dict, Optional

# from fastapi import Depends, FastAPI, Request

# # from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from sqlmodel import Field, Session, SQLModel, create_engine, select
# from starlette.middleware.cors import CORSMiddleware

# app = FastAPI()
# # Allow CORS for testing purposes
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Replace '*' with your frontend URL for production
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# class Todo(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str
#     priority: int = Field(default=0)
#     completed: bool = Field(default=False)


# engine = create_engine("sqlite:///todo2.db", connect_args={"check_same_thread": False})
# SQLModel.metadata.create_all(engine)  # Ensures no duplicate table definitions

# app = FastAPI()

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# def get_session():
#     with Session(engine) as session:
#         yield session

# @app.get("/", response_model=list[Todo])
# async def get_all_todo(session: Session = Depends(get_session)):
#     return session.exec(select(Todo)).all()

# def save_data(session: Session, todo: Todo):
#     session.add(todo)
#     session.commit()
#     # return todo
#     return session.exec(select(Todo)).all()

# # @app.post("/", status_code=201)
# # async def test(request: Request):
# #     # Extract JSON directly from request
# #     json_data = await request.json()
# #     print(json_data)  # Debug the raw JSON
# #     return {"status": "ok"}

# @app.post("/", status_code=201)
# async def test(request: Request):
#     try:
#         # Log raw request body
#         raw_body = await request.body()
#         print(f"Raw Body: {raw_body.decode('utf-8')}")  # Decode bytes to string
#         # Parse JSON data
#         json_data = await request.json()
#         print(f"JSON Parsed: {json_data}")  # Log parsed JSON
#         # Respond back with 'success'
#         return {"status": "ok", "data_received": json_data}
#     except Exception as e:
#         # Log and send error response
#         error_message = traceback.format_exc()
#         print(f"Error Occurred: {error_message}")
#         return {"error": "Invalid JSON received", "detail": str(e)}

# # @app.post("/", response_model=list[Todo], status_code=201)
# # async def create_todo(todo: Todo, session: Session = Depends(get_session)):
# #     # todo.completed = True if todo.completed == 'on' else False
# #     print("todo", todo.dict())
# #     return save_data(session, todo)

# @app.delete('/{id}', response_model=list[Todo], status_code=201)
# async def delete_todo(id: int, session: Session = Depends(get_session)):
#     todo = session.exec(select(Todo).where(Todo.id == id)).one()
#     # todo = session.get(Todo, id)
#     session.delete(todo)
#     session.commit()
#     return session.exec(select(Todo)).all()

# app.get('/{id}', response_model=Todo)
# async def get_single_todo(id: int, session: Session = Depends(get_session)):
#     return session.exec(select(Todo).where(Todo.id == id)).one()

# @app.patch('/{id}', response_model=list[Todo], status_code=201)
# async def modify_todo(id: int, session: Session = Depends(get_session)):
#     todo = session.exec(select(Todo).where(Todo.id == id)).one()
#     todo.completed = not todo.completed
#     session.commit()
#     return session.exec(select(Todo)).all()

# @app.put('/{id}', response_model=list[Todo], status_code=201)
# async def update_todo(id: int, todo: Todo, session: Session = Depends(get_session)):
#     db_todo = session.exec(select(Todo).where(Todo.id == id)).one()
#     todo = Todo(**todo.dict())
#     session.commit()
#     return session.exec(select(Todo)).all()

import json  # For debugging raw JSON
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine

# --- Database Configuration ---

DATABASE_FILE = "products.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True logs SQL queries

# --- SQLModel Database Model ---
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    price: float

# --- FastAPI Application Setup ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Specify your frontend origin for security
    allow_credentials=True,  # Allow cookies/credentials
    allow_methods=["*"],  # Allow POST, OPTIONS, GET, etc.
    allow_headers=["*"],  # Allow all headers
)

# --- Database Initialization ---
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)  # Creates tables based on SQLModel schema
    print("Database initialized and tables created.")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()  # Ensure tables are created on server startup

# --- Dependency to get a database session ---
def get_session():
    with Session(engine) as session:
        yield session

# --- Endpoint: Add Product ---
# @app.post("/")
# async def add_product(product: Product):
#     print(f"Received data: {product.model_dump_json(indent=2)}")  # Debug incoming JSON

#     with Session(engine) as session:
#         session.add(product)  # Add product to the session
#         session.commit()  # Save product in the database
#         session.refresh(product)  # Refresh instance (fetch auto-generated ID)

#         response_message = {
#             "message": "Product added successfully!",
#             "id": product.id,
#             "received_data": product.model_dump(),
#         }
#         print(f"Product saved to DB with ID {product.id}")
#         return response_message

@app.post("/")
async def add_product(request: Request):
    headers = request.headers
    body = await request.body()
    print("Headers:", headers)
    print("Body:", body)
    # with Session(engine) as session:
    #     session.add(product)
    #     session.commit()
    #     session.refresh(product)
    return {"message": "Product added successfully!"}

# --- Endpoint: Get All Products ---
@app.get("/products")
async def get_all_products():
    with Session(engine) as session:
        products = session.query(Product).all()  # Fetch all rows from Product table
        return {"products": [p.dict() for p in products]}