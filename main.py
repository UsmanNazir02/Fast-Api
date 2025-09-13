from fastapi import FastAPI, HTTPException

# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from selector import list_students, get_student_by_id
# from services import (
#     create_student,
#     update_student,
#     delete_student,
# )
from type import (
    StudentCreate,
    StudentUpdate,
    StudentOut,
)
from services import (
    get_all_students,
    get_student_by_id_memory,
    create_student,
    update_student,
    delete_student,
)
from agent_routes import router as agent_router

# DATABASE_URL = "postgresql+asyncpg://postgres:admin123@localhost:5432/bootcamp-db"
# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = async_sessionmaker(engine, expire_on_commit=False)

# --- Dependency (Commented out database dependency) ---
# async def get_db():
#     async with async_session() as session:
#         yield session

# --- FastAPI App ---
app = FastAPI(title="Student API with Agent", version="2.0")

app.include_router(agent_router, prefix="/agent", tags=["agent"])


@app.get("/students/", response_model=list[StudentOut])
async def read_students():
    # students = await list_students(db)
    students = get_all_students()
    return students


@app.get("/students/{student_id}", response_model=StudentOut)
async def read_student(student_id: int):
    # student = await get_student_by_id(db, student_id)
    student = get_student_by_id_memory(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/students/", response_model=StudentOut, status_code=201)
async def create_student_endpoint(student: StudentCreate):
    # student_obj = await create_student(db, student)
    student_obj = create_student(student)
    return student_obj


@app.put("/students/{student_id}", response_model=StudentOut)
async def update_student_endpoint(student_id: int, student: StudentUpdate):
    # updated = await update_student(db, student_id, student)
    updated = update_student(student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@app.delete("/students/{student_id}", response_model=StudentOut)
async def delete_student_endpoint(student_id: int):
    # deleted = await delete_student(db, student_id)
    deleted = delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return deleted


@app.get("/")
async def root():
    return {"message": "Student API with Agent is running!", "version": "2.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
