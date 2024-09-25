from flask import request

from flask import Blueprint, jsonify
from dictalchemy.utils import asdict
from repository.movie_repo import insert_movie, find_movie_by_id, delete_movie, update_movie
from model import Movie

movie_bluprint = Blueprint("movie", __name__)


@movie_bluprint.route("/<int:m_id>", methods=['GET'])
def get_by_id(m_id):
    movie = asdict(find_movie_by_id(m_id).value_or(""))
    if movie is not "":
        return jsonify(movie), 200
    else:
        return jsonify({}), 400


@movie_bluprint.route("/", methods=['POST'])
def post_movie():
    movie_json = request.json
    movie = insert_movie(Movie(genre=movie_json["genre"],
                               year=movie_json["year"],
                               title=movie_json["title"])).value_or("")
    if movie is not "":
        return jsonify(asdict(movie)), 200
    else:
        return jsonify({}), 400


@movie_bluprint.route("/<int:m_id>", methods=['PUT'])
def put_store(m_id):
    movie_json = request.json
    movie = update_movie(m_id, Movie(genre=movie_json["genre"],
                                     year=movie_json["year"],
                                     title=movie_json["title"])).value_or("")
    if movie is not "":
        return jsonify(asdict(movie)), 200
    else:
        return jsonify({}), 400


@movie_bluprint.route("/<int:m_id>", methods=['DELETE'])
def delete_movie_end_poynt(m_id):
    movie = delete_movie(m_id).value_or("")
    if movie is not "":
        return jsonify(asdict(movie)), 200
    else:
        return jsonify({}), 400
