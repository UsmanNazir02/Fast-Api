from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from selector import list_students, get_student_by_id, list_teachers, get_teacher_by_id
from services import (
    create_student,
    update_student,
    delete_student,
    # create_teacher,
    # update_teacher,
    # delete_teacher,
)
from type import (
    StudentCreate,
    StudentUpdate,
    StudentOut,
    # TeacherCreate,
    # TeacherUpdate,
    # TeacherOut,
)

DATABASE_URL = "postgresql+asyncpg://postgres:admin123@localhost:5432/bootcamp-db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


# --- Dependency ---
async def get_db():
    async with async_session() as session:
        yield session


# --- FastAPI App ---
app = FastAPI()


# --- Student Endpoints ---
@app.get("/students/", response_model=list[StudentOut])
async def read_students(db: AsyncSession = Depends(get_db)):
    students = await list_students(db)
    return students


@app.get("/students/{student_id}", response_model=StudentOut)
async def read_student(student_id: int, db: AsyncSession = Depends(get_db)):
    student = await get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.post("/students/", response_model=StudentOut, status_code=201)
async def create_student_endpoint(
    student: StudentCreate, db: AsyncSession = Depends(get_db)
):
    student_obj = await create_student(db, student)
    return student_obj


@app.put("/students/{student_id}", response_model=StudentOut)
async def update_student_endpoint(
    student_id: int, student: StudentUpdate, db: AsyncSession = Depends(get_db)
):
    updated = await update_student(db, student_id, student)
    if not updated:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated


@app.delete("/students/{student_id}", response_model=StudentOut)
async def delete_student_endpoint(student_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return deleted


# # --- Teacher Endpoints ---
# @app.get("/teachers/", response_model=list[TeacherOut])
# async def read_teachers(db: AsyncSession = Depends(get_db)):
#     teachers = await list_teachers(db)
#     return teachers


# @app.get("/teachers/{teacher_id}", response_model=TeacherOut)
# async def read_teacher(teacher_id: int, db: AsyncSession = Depends(get_db)):
#     teacher = await get_teacher_by_id(db, teacher_id)
#     if not teacher:
#         raise HTTPException(status_code=404, detail="Teacher not found")
#     return teacher


# @app.post("/teachers/", response_model=TeacherOut, status_code=201)
# async def create_teacher_endpoint(
#     teacher: TeacherCreate, db: AsyncSession = Depends(get_db)
# ):
#     teacher_obj = await create_teacher(db, teacher.dict())
#     return teacher_obj


# @app.put("/teachers/{teacher_id}", response_model=TeacherOut)
# async def update_teacher_endpoint(
#     teacher_id: int, teacher: TeacherUpdate, db: AsyncSession = Depends(get_db)
# ):
#     updated = await update_teacher(db, teacher_id, teacher.dict())
#     if not updated:
#         raise HTTPException(status_code=404, detail="Teacher not found")
#     return updated


# @app.delete("/teachers/{teacher_id}", response_model=TeacherOut)
# async def delete_teacher_endpoint(teacher_id: int, db: AsyncSession = Depends(get_db)):
#     deleted = await delete_teacher(db, teacher_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Teacher not found")
#     return deleted