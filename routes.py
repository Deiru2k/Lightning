from tornado.web import StaticFileHandler
from handlers import boards, posts, threads, auth
import os

handlers = [
    # Media Content
    (r'/v1/images/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'images')}),
    # Boards
    (r'/v1/boards', boards.BoardsHandler),
    (r'/v1/boards/(\w+)', boards.BoardHandler),
    # Threads
    (r'/v1/boards/(\w+)/threads', threads.ThreadsHandler),
    (r'/v1/boards/(\w+)/threads/(.*)', threads.ThreadHandler),
    # Posts
    (r'/v1/posts/(.*)', posts.PostHandler),
    # Auth
    (r'/v1/auth/redeem', auth.RedeemInviteHandler)
]