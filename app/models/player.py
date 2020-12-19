import string

from backends.mongodb import mongo_backend

# initialize the database
mongo_backend.init_database()


class Player():

    @staticmethod
    def get_one(name):
        return mongo_backend.get_one(name)

    @staticmethod
    def get_many(result_from, size, sort):
        return mongo_backend.get_one(result_from, size, sort)

    @staticmethod
    def create_one(body):
        return mongo_backend.create_one(body)

    @staticmethod
    def update_one(body):
        return mongo_backend.update_one(body)

    @staticmethod
    def delete_one(name):
        return mongo_backend.delete_one(name)
