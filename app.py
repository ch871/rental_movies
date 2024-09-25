from repository.database import create_tables
import logging

from flask import Flask

from controlers.store_controler import store_bluprint
from controlers.rental_controler import rental_bluprint
from controlers.movie_contrler import movie_bluprint
from controlers.user_controler import user_bluprint

from repository.movie_repo import insert_movie
from repository.store_repo import insert_store
from repository.user_repo import insert_user
from repository.rental_repo import insert_rental
from model import Store, Movie, User, Rental

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

if __name__ == '__main__':
    create_tables()
    # saved_store = insert_store(Store(name='metach',
    #                             state='sar atabaot',
    #                             city="123456789",
    #                             street="poiuy")).value_or("problem")
    #
    # saved_rental = insert_rental(Rental(rental_date="2019-12-04",
    #                                     return_date='2019-12-12',
    #                                     rental_fee=6.0,
    #                                     late_fee=5.8,
    #                                     user_id=1,
    #                                     movie_id=1,
    #                                     store_id=1,
    #                                     )).value_or("problem")
    #
    # saved_user = insert_movie(Movie(genre='metach', year=1995, title='sar atabaot')).value_or("problem")
    #
    # saved_user = insert_user(User(name='metach',
    #                               email='sar atabaot',
    #                               phone="123456789")).value_or("problem")

    app.register_blueprint(user_bluprint, url_prefix="/api/user")
    app.register_blueprint(store_bluprint, url_prefix="/api/store")
    app.register_blueprint(movie_bluprint, url_prefix="/api/movie")
    app.register_blueprint(rental_bluprint, url_prefix="/api/rental")

    app.run(debug=True)
