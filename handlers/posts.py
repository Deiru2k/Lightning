from tornado.gen import coroutine
from schemas.posts import post_multiple, post_single
from base import BaseHandler


class PostsHandler(BaseHandler):

    @coroutine
    def get(self):

        board = self.get_argument("board", None)
        thread = self.get_argument("thread", None)
        try:
            page = int(self.get_argument("page", 0))
        except ValueError:
            page = 0

        query_params = dict()
        if board:
            query_params['board'] = board
        if thread:
            query_params['thread'] = thread

        query = self.db.posts.filter(query_params).skip(self.per_page * page).limit(self.per_page)
        posts = yield self.db.run_query(query)
        self.respond(posts, post_multiple)

    @coroutine
    def post(self):

        post = self.request.data
        try:
            del post['id']
        except KeyError:
            pass

        query = self.db.posts.insert(post)
        result = yield self.db.run_query(query)
        key = result['generated_keys'][0]
        post = yield self.db.posts.get(key)
        self.respond(post, post_single)
