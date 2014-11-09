import hashlib
import rethinkdb as r
from base import BaseHandler
from tornado.gen import coroutine
from schemas.posts import post_single, post_multiple


class ThreadsHandler(BaseHandler):

    @coroutine
    def get(self, board):
        try:
            page = int(self.get_argument("page", 0))
        except ValueError:
            page = 0
        query = self.db.posts.filter(lambda thread: thread.has_fields('thread').not_().and_(thread['board'] == board))\
            .without('password').skip(self.per_page * page).limit(self.per_page)
        threads = yield self.db.run_query(query)
        for thread in threads:
            query = self.db.posts.get_all(thread['id'], index="thread").without('password').limit(3)
            posts = yield self.db.run_query(query)
            thread['posts'] = sorted(posts, key=lambda post: post['createdAt']['epoch_time'])
        self.respond(threads, post_multiple)

    @coroutine
    def post(self, board_id):

        post = self.request.data
        for key in ['id', 'thread']:
            try:
                del post[key]
            except KeyError:
                continue
        if 'password' in post:
            post['password'] = hashlib.sha256(post['password'].encode('UTF-8')).hexdigest()
        if 'image' in post:
            image_format = post['image']['filetype'].split('/')[1]
            name = post['image']['filename']
            b64 = post['image']['base64']
            filesize = post['image']['filesize']
            filename = self.id_generator()
            url = yield self.upload_b64(b64, filename, image_format)
            post['image'] = {
                'size': filesize,
                'url': url,
                'name': name
            }
        else:
            self.error(code=400, message="Threads without images attached are not allowed")
            return
        post['board'] = board_id
        post['createdAt'] = r.now()
        post['modifiedAt'] = post['createdAt']
        query = self.db.posts.insert(post)
        result = yield self.db.run_query(query)
        key = result['generated_keys'][0]
        query = self.db.posts.get(key).without('password')
        post = yield self.db.run_query(query)
        self.respond(post, post_single)


class ThreadHandler(BaseHandler):

    @coroutine
    def get(self, board, thread_id):

        query = self.db.posts.get(thread_id).without('password')
        thread = yield self.db.run_query(query)
        query = self.db.posts.get_all(thread_id, index='thread').without('password')
        posts = yield self.db.run_query(query)
        posts.insert(0, thread)
        response = sorted(posts, key=lambda post: post['createdAt']['epoch_time'])
        self.respond(response, post_multiple)


    @coroutine
    def post(self, board_id, thread_id):

        post = self.request.data
        for key in ['id', 'thread']:
            try:
                del post[key]
            except KeyError:
                pass
        if 'password' in post:
            post['password'] = hashlib.sha256(post['password'].encode('UTF-8')).hexdigest()
        if 'image' in post:
            image_format = post['image']['filetype'].split('/')[1]
            name = post['image']['filename']
            b64 = post['image']['base64']
            filesize = post['image']['filesize']
            filename = self.id_generator()
            url = yield self.upload_b64(b64, filename, image_format)
            post['image'] = {
                'size': filesize,
                'url': url,
                'name': name
            }
        post['board'] = board_id
        post['thread'] = thread_id
        post['createdAt'] = r.now()
        post['modifiedAt'] = post['createdAt']
        query = self.db.posts.insert(post)
        result = yield self.db.run_query(query)
        key = result['generated_keys'][0]
        query = self.db.posts.get(key).without('password')
        post = yield self.db.run_query(query)
        self.respond(post, post_single)

    @coroutine
    def delete(self, board_id, post_id):

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