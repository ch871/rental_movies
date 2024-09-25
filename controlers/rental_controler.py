from flask import request

from flask import Blueprint, jsonify
from dictalchemy.utils import asdict
from repository.rental_repo import insert_rental, find_rental_by_id, delete_rental, update_rental
from model import Rental

rental_bluprint = Blueprint("rental", __name__)


@rental_bluprint.route("/<int:r_id>", methods=['GET'])
def get_by_id(r_id):
    rental = asdict(find_rental_by_id(r_id).value_or(""))
    if rental is not "":
        return jsonify(rental), 200
    else:
        return jsonify({}), 400


@rental_bluprint.route("/", methods=['POST'])
def post_rental():
    rental_json = request.json
    rental = insert_rental(Rental(rental_date=rental_json["rental_date"],
                                  return_date=rental_json["return_date"],
                                  rental_fee=rental_json["rental_fee"],
                                  late_fee=rental_json["late_fee"],
                                  user_id=rental_json["user_id"],
                                  movie_id=rental_json["movie_id"],
                                  store_id=rental_json["store_id"],
                                  )).value_or("")
    if rental is not "":
        return jsonify(asdict(rental)), 200
    else:
        return jsonify({}), 400


@rental_bluprint.route("/<int:r_id>", methods=['PUT'])
def put_rental(r_id):
    rental_json = request.json
    rental = update_rental(r_id, Rental(rental_date=rental_json["rental_date"],
                                        return_date=rental_json["return_date"],
                                        rental_fee=rental_json["rental_fee"],
                                        late_fee=rental_json["late_fee"],
                                        user_id=rental_json["user_id"],
                                        movie_id=rental_json["movie_id"],
                                        store_id=rental_json["store_id"],
                                        )).value_or("")
    if rental is not "":
        return jsonify(asdict(rental)), 200
    else:
        return jsonify({}), 400


@rental_bluprint.route("/<int:r_id>", methods=['DELETE'])
def delete_rental_end_poynt(r_id):
    rental = delete_rental(r_id).value_or("")
    if rental is not "":
        return jsonify(asdict(rental)), 200
    else:
        return jsonify({}), 400
