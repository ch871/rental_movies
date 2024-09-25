from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from config.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    phone = Column(String(255), nullable=False)

    rentals = relationship("Rental", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id} name={self.name}, email={self.email},phone={self.phone})>"
