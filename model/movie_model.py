from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from config.base import Base


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    genre = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)

    rentals = relationship("Rental", lazy="noload", back_populates="movie")

    def __repr__(self):
        return f"title={self.title}, genre={self.genre}, year={self.year}"
