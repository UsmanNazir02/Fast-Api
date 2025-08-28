from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, nullable=True)

class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    age: Mapped[int | None] = mapped_column(nullable=True)