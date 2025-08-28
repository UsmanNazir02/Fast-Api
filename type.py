from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    age: int | None = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentOut(StudentBase):
    id: int


# class TeacherBase(BaseModel):
#     name: str
#     age: int | None = None


# class TeacherCreate(TeacherBase):
#     pass


# class TeacherUpdate(TeacherBase):
#     pass


# class TeacherOut(TeacherBase):
#     id: int

#     class Config:
#         orm_mode = True