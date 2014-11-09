import hashlib
from tornado.gen import coroutine
from schemas.posts import post_multiple, post_single
from base import BaseHandler


# class PostsHandler(BaseHandler):
#
#     @coroutine
#     def get(self):
#
#         board = self.get_argument("board", None)
#         thread = self.get_argument("thread", None)
#         try:
#             page = int(self.get_argument("page", 0))
#         except ValueError:
#             page = 0
#
#         query_params = dict()
#         if board:
#             query_params['board'] = board
#         if thread:
#             query_params['thread'] = thread
#
#         query = self.db.posts.filter(query_params).skip(self.per_page * page).limit(self.per_page)
#         posts = yield self.db.run_query(query)
#         self.respond(posts, post_multiple)
#
#     @coroutine
#     def post(self):
#
#         post = self.request.data
#         try:
#             del post['id']
#         except KeyError:
#             pass
#
#         query = self.db.posts.insert(post)
#         result = yield self.db.run_query(query)
#         key = result['generated_keys'][0]
#         post = yield self.db.posts.get(key)
#         self.respond(post, post_single)


class PostHandler(BaseHandler):

    @coroutine
    def get(self, post_id):

        query = self.db.posts.get(post_id)
        post = yield self.db.run_query(query)
        self.respond(post, post_single)


    @coroutine
    def delete(self, post_id):

        password = self.get_argument("password", None)
        if not password:
            self.error(code=401, message="No Password")
        query = self.db.posts.get(post_id)
        post = yield self.db.run_query(query)
        if not post:
            self.error(code=404, message="Post not found")
            return
        password = hashlib.sha256(password.encode('UTF-8')).hexdigest()
        if password == post['password']:
            query = self.db.posts.get(post_id).delete()
            yield self.db.run_query(query)
            self.respond(code=204)
        else:
            self.error(code=403, message="Bad Password")