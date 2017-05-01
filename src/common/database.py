import os

import pymongo

# Create the database class:

class Database(object):
    # Universal Resource Identifyer
    # 27017 is the default mongodb port

    # Mongolab already adds MONGOLAB_URI, so it's not necessary to do anything else.
    URI = os.environ.get("MONGOLAB_URI")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        # sets the database for name
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def insert_or_modify(collection, data):
        Database.DATABASE[collection].save(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def remove(collection, query):
        Database.DATABASE[collection].remove(query)

