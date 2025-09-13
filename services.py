from typing import List, Dict, Optional
from type import StudentCreate, StudentUpdate, StudentOut
from fastapi import HTTPException

# In-Memory Storage
students_db: List[Dict] = []
next_id = 1

# === ORIGINAL DATABASE CODE (COMMENTED OUT) ===
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from models import Student
# from type import StudentCreate, StudentUpdate

# async def create_student(db: AsyncSession, student: StudentCreate):
#     db_student = Student(name=student.name, age=student.age)
#     db.add(db_student)
#     await db.commit()
#     await db.refresh(db_student)
#     return db_student

# async def update_student(db: AsyncSession, student_id: int, student: StudentUpdate):
#     result = await db.execute(select(Student).where(Student.id == student_id))
#     db_student = result.scalar_one_or_none()
#     
#     if db_student:
#         if student.name is not None:
#             db_student.name = student.name
#         if student.age is not None:
#             db_student.age = student.age
#         
#         await db.commit()
#         await db.refresh(db_student)
#         return db_student
#     return None

# async def delete_student(db: AsyncSession, student_id: int):
#     result = await db.execute(select(Student).where(Student.id == student_id))
#     db_student = result.scalar_one_or_none()
#     
#     if db_student:
#         await db.delete(db_student)
#         await db.commit()
#         return db_student
#     return None

# === NEW IN-MEMORY FUNCTIONS (ASSIGNMENT 2) ===

def get_next_id():
    global next_id
    current_id = next_id
    next_id += 1
    return current_id

def validate_gender(gender: str) -> bool:
    """Validate gender is one of allowed values"""
    if not gender:
        return True
    return gender.lower() in ["male", "female", "other"]

def is_email_unique(email: str, exclude_id: Optional[int] = None) -> bool:
    """Check if email is unique in the database"""
    if not email:
        return True
    
    for student in students_db:
        if student.get("email") == email and student["id"] != exclude_id:
            return False
    return True

def find_student_by_id(student_id: int) -> Optional[Dict]:
    """Find student by ID in memory"""
    for student in students_db:
        if student["id"] == student_id:
            return student
    return None

# Service functions for FastAPI endpoints (replacing database versions)
def get_all_students() -> List[StudentOut]:
    """Get all students - replaces list_students(db)"""
    return [StudentOut(**student) for student in students_db]

def get_student_by_id_memory(student_id: int) -> Optional[StudentOut]:
    """Get student by ID - replaces get_student_by_id(db, student_id)"""
    student = find_student_by_id(student_id)
    if student:
        return StudentOut(**student)
    return None

def create_student(student: StudentCreate) -> StudentOut:
    """Create new student - replaces async create_student(db, student)"""
    # Validate gender
    if student.gender and not validate_gender(student.gender):
        raise HTTPException(status_code=400, detail="Gender must be 'male', 'female', or 'other'")
    
    # Check email uniqueness
    if student.email and not is_email_unique(student.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_student = {
        "id": get_next_id(),
        "name": student.name,
        "age": student.age,
        "gender": student.gender.lower() if student.gender else None,
        "email": student.email
    }
    students_db.append(new_student)
    return StudentOut(**new_student)

def update_student(student_id: int, student: StudentUpdate) -> Optional[StudentOut]:
    """Update student - replaces async update_student(db, student_id, student)"""
    existing_student = find_student_by_id(student_id)
    if not existing_student:
        return None
    
    # Validate gender if provided
    if student.gender and not validate_gender(student.gender):
        raise HTTPException(status_code=400, detail="Gender must be 'male', 'female', or 'other'")
    
    # Check email uniqueness if provided
    if student.email and not is_email_unique(student.email, exclude_id=student_id):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Update fields
    if student.name is not None:
        existing_student["name"] = student.name
    if student.age is not None:
        existing_student["age"] = student.age
    if student.gender is not None:
        existing_student["gender"] = student.gender.lower()
    if student.email is not None:
        existing_student["email"] = student.email
    
    return StudentOut(**existing_student)

def delete_student(student_id: int) -> Optional[StudentOut]:
    """Delete student - replaces async delete_student(db, student_id)"""
    student = find_student_by_id(student_id)
    if not student:
        return None
    
    students_db.remove(student)
    return StudentOut(**student)