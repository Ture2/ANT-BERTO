import constants
from pymongo import MongoClient


def mongo_connection():
    client = MongoClient("127.0.0.1", 27017)
    db = client[constants.MONGO_DATABASE]
    collection = db[constants.MONGO_COLLECTION]
    return collection


def mongo_results_connection():
    client = MongoClient("127.0.0.1", 27017)
    db = client[constants.MONGO_RESULTS_DATABASE]
    collection = db[constants.MONGO_RESULTS_COLLECTION]
    return collection


def get_contract(id):
    collection = mongo_connection()
    cursor = collection.find({'contract_id': id})
    return cursor.next()


def get_all_contract_id():
    collection = mongo_connection()
    c_contracts = collection.find({'contract_id': {"$exists": 'true', "$ne": ""}}, no_cursor_timeout=True)
    return c_contracts


def get_range_contract(start_id, end_id):
    collection = mongo_connection()
    c_contracts = collection.find({'contract_id': {"$gte": start_id, "$lte": end_id}}, no_cursor_timeout=True)
    return c_contracts


def get_from_number(start_id):
    collection = mongo_connection()
    c_contracts = collection.find({'contract_id': {"$gte": start_id}}, no_cursor_timeout=True)
    return c_contracts


def insert_result(id, field, value):
    collection = mongo_results_connection()
    query = {'contract_id': id}
    new_values = {"$addToSet": {"results": {"{}".format(field): "{}".format(value)}},
                  "$setOnInsert": {"contract_id": id}}
    collection.update(query, new_values, upsert=True)


def remove_result(id):
    collection = mongo_connection()
    query = {"contract_id": id}
    remove_values = {"$unset": {"results": ""}}
    collection.update(query, remove_values)
