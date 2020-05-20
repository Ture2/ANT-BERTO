import constants
from datetime import datetime
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


def get_contract_by_address(address):
    collection = mongo_connection()
    c_contracts = collection.find({'address': address})
    return c_contracts


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


def insert_result(id, address, field, value, time_elapsed):
    collection = mongo_results_connection()
    query = {'contract_id': id}
    new_values = {"$set": {
        "{}".format(field): {
            "output": "{}".format(value),
            "time_elapsed": time_elapsed}},
            "$setOnInsert": {"contract_id": id, "address": address, "timestamp": datetime.now()}}
    collection.update(query, new_values, upsert=True)


def remove_result(id):
    collection = mongo_connection()
    query = {"contract_id": id}
    remove_values = {"$unset": {"results": ""}}
    collection.update(query, remove_values)
