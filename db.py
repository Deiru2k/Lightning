import rethinkdb as r
from tornado.gen import coroutine


class Database:

    def __init__(self, db_name):

        self.connection = r.connect()
        self.db = r.db(db_name)
        self.boards = self.db.table('boards')
        self.posts = self.db.table('posts')

    @coroutine
    def run_query(self, query) -> (list, object):
        """
        :param query: query to execute
        :type query: rethinkdb.RqlQuery
        """
        data = query.run(self.connection, time_format="raw")
        if isinstance(data, r.Cursor):
            data = list(data)
        return data