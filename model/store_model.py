from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from config.base import Base


class Store(Base):
    __tablename__ = "stores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    state = Column(String(200), nullable=False)
    city = Column(String(200), nullable=False)
    street = Column(String(100), nullable=False)

    rentals = relationship("Rental", back_populates="store")

    def __repr__(self):
        return f"<User(id={self.id} name={self.name}, state={self.state}, city={self.city}, street={self.street})>"
