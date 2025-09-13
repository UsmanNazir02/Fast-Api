# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import declarative_base, Mapped, mapped_column

# Base = declarative_base()

# class Student(Base):
#     __tablename__ = "student"

#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     name: Mapped[str] = mapped_column()
#     age: Mapped[int | None] = mapped_column(nullable=True)