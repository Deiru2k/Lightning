from tornado.gen import coroutine
from base import BaseHandler
from schemas.hello import hello_output


class HelloHandler(BaseHandler):

    output_schema = hello_output

    @coroutine
    def get(self, name):

        hello = "Hello, %s" % name
        self.respond(hello)