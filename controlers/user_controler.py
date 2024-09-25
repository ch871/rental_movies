from flask import request

from flask import Blueprint, jsonify
from dictalchemy.utils import asdict
from repository.user_repo import insert_user, find_user_by_id, delete_user, update_user
from model import User

user_bluprint = Blueprint("user", __name__)


@user_bluprint.route("/<int:u_id>", methods=['GET'])
def get_by_id(u_id):
    user = asdict(find_user_by_id(u_id).value_or(""))
    if user is not "":
        return jsonify(user), 200
    else:
        return jsonify({}), 400


@user_bluprint.route("/", methods=['POST'])
def post_user():
    user_json = request.json
    user = insert_user(User(name=user_json["name"],
                            email=user_json["email"],
                            phone=user_json["phone"])).value_or("")
    if user is not "":
        return jsonify(asdict(user)), 200
    else:
        return jsonify({}), 400


@user_bluprint.route("/<int:u_id>", methods=['PUT'])
def put_useri(u_id):
    user_json = request.json
    user = update_user(u_id, User(name=user_json["name"],
                                  email=user_json["email"],
                                  phone=user_json["phone"])).value_or("")
    if user is not "":
        return jsonify(asdict(user)), 200
    else:
        return jsonify({}), 400


@user_bluprint.route("/<int:u_id>", methods=['DELETE'])
def put_user(u_id):
    user = delete_user(u_id).value_or("")
    if user is not "":
        return jsonify(asdict(user)), 200
    else:
        return jsonify({}), 400
