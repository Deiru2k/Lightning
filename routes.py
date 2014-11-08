from handlers import boards

handlers = [
    (r'/v1/boards', boards.BoardsHandler),
    (r'/v1/boards/(\w+)', boards.BoardHandler)
]