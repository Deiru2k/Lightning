import os
import rethinkdb as r
from rethinkdb import errors
from base import DB_NAME, DB_PORT, DB_HOST


tables = {
    "boards": None,
    "posts": ['thread']
}


def create_tables():

    connection = r.connect(host=DB_HOST, port=DB_PORT)
    if DB_NAME == "EDIT_ME":
        print("You haven't edited DB_NAME. Go to base.py and check Database Settings")
        os.exit(0)
    try:
        print("Attempting to create database %s" % DB_NAME)
        r.db_create(DB_NAME).run(connection)
        print("Database Created.")
    except errors.RqlRuntimeError:
        print("Database already exists")
    db = r.db(DB_NAME)
    for table in tables:
        try:
            print("Creating table %s" % table)
            db.table_create(table).run(connection)
        except errors.RqlRuntimeError:
            print("Table already Exists")
        if tables[table]:
            for index in tables[table]:
                try:
                    print("Creating index %s on table %s" % (index, table))
                    db.table(table).index_create(index).run(connection)
                except errors.RqlRuntimeError:
                    print("Index already created.")
    print("All done. Follow further instructions to complete the setup.")


if __name__ == '__main__':
    create_tables()