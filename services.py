from models import Teacher, Student
from sqlalchemy.ext.asyncio import AsyncSession
from type import StudentCreate, StudentUpdate


async def create_teacher(db: AsyncSession, teacher: dict):
    db_teacher = Teacher(**teacher)
    db.add(db_teacher)
    await db.commit()
    await db.refresh(db_teacher)

    return db_teacher


async def update_teacher(db: AsyncSession, teacher_id: int, teacher: dict):
    db_teacher = await db.get(Teacher, teacher_id)
    if not db_teacher:
        return None

    for key, value in teacher.items():
        setattr(db_teacher, key, value)

    await db.commit()
    await db.refresh(db_teacher)

    return db_teacher


async def delete_teacher(db: AsyncSession, teacher_id: int):
    db_teacher = await db.get(Teacher, teacher_id)

    if not db_teacher:
        return None

    await db.delete(db_teacher)
    await db.commit()

    return db_teacher


async def create_student(db: AsyncSession, student: StudentCreate):
    db_student = Student(name=student.name, age=student.age)
    db.add(db_student)

    await db.commit()
    await db.refresh(db_student)

    return db_student


async def update_student(db: AsyncSession, student_id: int, student: StudentUpdate):
    db_student = await db.get(Student, student_id)
    if not db_student:
        return None

    db_student.name = student.name
    db_student.age = student.age

    await db.commit()
    await db.refresh(db_student)

    return db_student


async def delete_student(db: AsyncSession, student_id: int):
    db_student = await db.get(Student, student_id)
    if not db_student:
        return None

    await db.delete(db_student)
    await db.commit()

    return db_student