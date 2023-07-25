from pymongo import MongoClient

session = MongoClient('mongodb://localhost/')


def get_databases_names():
    names = session.list_database_names()
    for i in ('admin', 'config', 'local'):
        names.remove(i)
    return names


def create_entry(database, table, entry):
    session[database][table].insert_one(entry)
