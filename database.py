from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

session = MongoClient('mongodb://localhost/')


def check_connection():
    try:
        return session.list_database_names()
    except ServerSelectionTimeoutError:
        return None


def get_databases_names():
    names = session.list_database_names()
    for i in ('admin', 'config', 'local'):
        names.remove(i)
    return names


def get_collections_names(database):
    names = session[database].list_collection_names()
    return names


def get_entries_names(database, table):
    entries = list(session[database][table].find({}))
    [n.pop('_id') for n in entries]
    formatted_entries = [[j['name'], j['price'], j['count']] for j in entries]
    return formatted_entries


def create_new_entry(database, table, name, price, count):
    session[database][table].insert_one({'name': name,
                                         'price': price,
                                         'count': count})


def delete_database(database):
    session.drop_database(database)


def delete_collection(database, table):
    session[database][table].drop()


def delete_entry(database, table, entry):
    session[database][table].delete_one({"name": entry})
