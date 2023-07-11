from pymongo import MongoClient

session = MongoClient('mongodb://localhost/')


class AbstractEntry():
    def __init__(self, parent, name, **additional):
        self.parent = parent
        self.name = name


def get_databases_names():
    return session.list_database_names()[3:]


def create_entry(database, table, entry):
    session[database][table].insert_one(entry)
