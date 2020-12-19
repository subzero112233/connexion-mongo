import json
import logging
import os

import pymongo
import data.nba_players

from collections import OrderedDict
from datetime import datetime

logger = logging.getLogger(__name__)

mongo_host = os.getenv('MONGODB_HOST', 'localhost')
username, password = os.environ['MONGODB_USERNAME'], os.environ['MONGODB_PASSWORD']
database, collection = 'nba', 'players'

conn = pymongo.MongoClient("mongodb://{}:27017/".format(mongo_host), username=username, password=password)
db = conn[database]
coll = db[collection]


def transform_date(func):
    def func_wrapper(body):
        try:
            body['birth_date'] = datetime.strptime(body['birth_date'], "%Y-%m-%d")
        except KeyError:
            pass
        except ValueError:
            body['birth_date'] = datetime.strptime("1900-01-01", "%Y-%m-%d")
        return func(body)

    return func_wrapper


def get_many(result_from, size, sort):
    total = coll.count()

    if sort:
        players = list(coll.find({}, {"_id": 0}, skip=result_from, limit=size).sort("name"))
    else:
        players = list(coll.find({}, {"_id": 0}, skip=result_from, limit=size))

    return players, total


def get_one(name):
    return list(coll.find({"name": name}, {"_id": 0}))


@transform_date
def create_one(details):
    try:
        res = coll.insert_one(details)
    except pymongo.errors.DuplicateKeyError:
        res = None
    return res


@transform_date
def update_one(details):
    res = coll.find_one_and_update(
        {"name": details['name']},
        {"$set":
             details}
        , {"_id": 0}, upsert=False, return_document=False
    )

    return res


def delete_one(name):
    return coll.delete_one({"name": name})


def init_database(populate=True, fetch_players=False):
    if collection in db.list_collection_names():
        logger.info("Collection already exists, skipping initialization")
        return

    logger.info("initializing database")

    # create the collection
    db.create_collection(collection)

    # enforce schema validation for storing only alphabetic names
    with open('backends/mongodb/schema/db_schema.json') as f:
        schema = json.load(f)

    cmd = OrderedDict(schema)
    db.command(cmd)

    # create an index for better performance and to avoid duplicates
    coll.create_index([("name", 1), ("birth_date", 1)], unique=True)

    if populate:
        if fetch_players:
            players = nba_players.generate_players_list()
        else:
            with open('data/players.json', 'r') as f:
                players = json.load(f)
                for item in players:
                    item['birth_date'] = datetime.strptime(item['birth_date'], "%Y-%m-%d")

        coll.insert_many(players)
        logging.info('{} Players inserted'.format(len(players)))
