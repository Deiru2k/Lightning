from tornado.web import StaticFileHandler
from handlers import boards, posts, threads
import os

handlers = [
    (r'/v1/images/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'images')}),
    (r'/v1/boards', boards.BoardsHandler),
    (r'/v1/boards/(\w+)', boards.BoardHandler),
    (r'/v1/boards/(\w+)/threads', threads.ThreadsHandler),
    (r'/v1/boards/(\w+)/threads/(.*)', threads.ThreadHandler),
    #(r'/v1/posts', posts.PostsHandler)
    (r'/v1/posts/(.*)', posts.PostHandler)
]