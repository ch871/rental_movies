from sqlalchemy import Column, Integer, ForeignKey, Date, Float, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from config.base import Base


class Rental(Base):
    __tablename__ = 'rentals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    rental_date = Column(Date, nullable=False)
    return_date = Column(Date)
    rental_fee = Column(Float, nullable=False)
    late_fee = Column(Float, default=0.0)
    total_payment = Column(Float)

    user = relationship("User", back_populates="rentals")
    movie = relationship("Movie", back_populates="rentals")
    store = relationship("Store", back_populates="rentals")

    def __repr__(self):
        return f"<User(id={self.id} user_id={self.user_id}, movie_id={self.movie_id}, store_id={self.store_id}, rental_date={self.rental_date}, return_date={self.return_date}, rental_fee={self.rental_fee}, late_fee={self.late_fee})>"
