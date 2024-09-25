from flask import request

from flask import Blueprint, jsonify
from dictalchemy.utils import asdict
from repository.store_repo import insert_store, find_store_by_id, delete_store, update_store
from model import Store

store_bluprint = Blueprint("store", __name__)


@store_bluprint.route("/<int:s_id>", methods=['GET'])
def get_by_id(s_id):
    store = asdict(find_store_by_id(s_id).value_or(""))
    if store is not "":
        return jsonify(store), 200
    else:
        return jsonify({}), 400


@store_bluprint.route("/", methods=['POST'])
def post_store():
    store_json = request.json
    store = insert_store(Store(name=store_json["name"],
                               state=store_json["state"],
                               city=store_json["city"],
                               street=store_json["street"])).value_or("")
    if store is not "":
        return jsonify(asdict(store)), 200
    else:
        return jsonify({}), 400


@store_bluprint.route("/<int:s_id>", methods=['PUT'])
def put_store(s_id):
    store_json = request.json
    store = update_store(s_id, Store(name=store_json["name"],
                                     state=store_json["state"],
                                     city=store_json["city"],
                                     street=store_json["street"])).value_or("")
    if store is not "":
        return jsonify(asdict(store)), 200
    else:
        return jsonify({}), 400


@store_bluprint.route("/<int:s_id>", methods=['DELETE'])
def delete_store_end_poynt(s_id):
    store = delete_store(s_id).value_or("")
    if store is not "":
        return jsonify(asdict(store)), 200
    else:
        return jsonify({}), 400
