import json
from tornado.web import RequestHandler
from jsonschema import Draft4Validator
from tornado.gen import coroutine
from exceptions import SchemaException
from db import Database


class BaseHandler(RequestHandler):

    input_schema = None
    output_schema = None
    db = Database("mikotoboard")

    def prepare(self):

        if self.request.method not in ['GET', 'DELETE', 'OPTIONS']:
            if not self.input_schema:
                raise SchemaException()
            validator = Draft4Validator(self.input_schema)
            print(validator.is_valid(self.request.body.decode('UTF-8')))
            try:
                data = json.loads(self.request.body.decode('UTF-8'))
            except ValueError:
                self.error(code=400, message="JSON input is malformed")
                return
            setattr(self.request, 'data', data)


    @coroutine
    def respond(self, response=None, code=200):

        if not response:
            response = {
                "status": "success",
                "data": None
            }
            self.set_status(status_code=code)
            self.write(json.dumps(response))
            self.finish()
            return
        if not self.output_schema:
            raise SchemaException()
        validator = Draft4Validator(self.output_schema)
        if not validator.is_valid(response):
            self.error(code=500, message="Validation of output failed")
            return
        response = {
            "status": "success",
            "data": response
        }
        self.set_status(status_code=code)
        self.write(json.dumps(response))
        self.finish()

    @coroutine
    def error(self, code=500, message="Internal Server Error", data=None):

        response = {
            "code": code,
            "message": message
        }
        if data: response['data'] = data
        self.set_status(status_code=code, reason=message)
        self.write(json.dumps(response))
        self.finish()