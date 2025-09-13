# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select
# from models import Student


# async def get_student_by_id(db: AsyncSession, student_id: int):
#     try:
#         result = await db.get(Student, student_id)
#         return result
#     except Exception as e:
#         print(f"Error fetching student by ID {student_id}: {e}")
#         return None


# async def list_students(db: AsyncSession):
#     try:
#         result = await db.execute(select(Student))
#         return result.scalars().all()
#     except Exception as e:
#         print(f"Error listing students: {e}")
#         return []
