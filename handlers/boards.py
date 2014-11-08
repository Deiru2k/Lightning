from tornado.gen import coroutine
from base import BaseHandler
from schemas.boards import board_multiple, board_single
import rethinkdb as r


class BoardsHandler(BaseHandler):

    input_schema = board_single
    output_schema = board_multiple

    @coroutine
    def get(self):

        query = self.db.boards
        boards = yield self.db.run_query(query)
        self.respond(response=boards)

    @coroutine
    def post(self):

        board = self.request.data
        check = self.db.boards.get(board['id'])
        check = yield self.db.run_query(check)
        if check:
            self.error(code=400, message="ID is already taken", data=board['id'])
            return
        board['createdAt'] = r.now()
        board['modifiedAt'] = board['createdAt']
        query = self.db.boards.insert(board)
        yield self.db.run_query(query)
        self.respond(code=201)


class BoardHandler(BaseHandler):

    input_schema = board_single
    output_schema = board_single

    @coroutine
    def get(self, board_id):

        query = self.db.boards.get(board_id)
        board = yield self.db.run_query(query)
        if not board:
            self.error(code=404, message="Board not found", data=board_id)
            return
        self.respond(board)


    @coroutine
    def put(self, board_id):

        board = self.request.data
        try:
            del board['id']
        except KeyError:
            pass
        query = self.db.boards.get(board_id).update(board)
        yield self.db.run_query(query)
        self.respond(code=204)