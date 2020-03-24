import constants
from pymongo import MongoClient


def mongo_connection():
    client = MongoClient("127.0.0.1", 27017)
    db = client.my
    collection = db[constants.MONGO_COLLECTION]
    return collection


def get_contract(id):
    collection = mongo_connection()
    cursor = collection.find({'contract_id': id})
    return cursor.next()


def get_all_contract_id():
    collection = mongo_connection()
    c_contracts = collection.find({'contract_id': {"$exists": 'true', "$ne": ""}})
    return c_contracts


def get_range_contract(start_id, end_id):
    collection = mongo_connection()
    c_contracts = collection.find({'contract_id': {"$gte":  start_id, "$lte": end_id}})
    return c_contracts


def get_from_number(start_id):
    collection = mongo_connection()
    c_contracts = collection.find({'contract_id': {"$gte": start_id}})
    return c_contracts

