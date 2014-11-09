import base64
from io import BytesIO
import json
import random
import string
from PIL import Image
from tornado.web import RequestHandler
from jsonschema import Draft4Validator
from tornado_cors import CorsMixin
from tornado.gen import coroutine
from exceptions import SchemaException
from db import Database
import os


class BaseHandler(CorsMixin, RequestHandler):

    CORS_ORIGIN = "*"
    CORS_HEADERS = 'Content-Type'
    CORS_METHODS = "GET,POST,PUT,OPTIONS"

    db = Database("mikotoboard")
    per_page = 10
    path = os.path.dirname(__file__)

    def prepare(self):

        if self.request.method not in ['GET', 'DELETE', 'OPTIONS']:
            try:
                data = json.loads(self.request.body.decode('UTF-8'))
            except ValueError:
                self.error(code=400, message="JSON input is malformed")
                return
            setattr(self.request, 'data', data)


    @coroutine
    def respond(self, response=None, output_schema=None, code=200,):

        if not response:
            response = {
                "status": "success",
                "data": None
            }
            self.set_status(status_code=code)
            self.write(json.dumps(response))
            self.finish()
            return
        if not output_schema:
            raise SchemaException()
        validator = Draft4Validator(output_schema)
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


    @coroutine
    def upload_b64(self, b64, name, image_format):

        path = os.path.join(self.path, 'images')
        image_file = BytesIO(base64.b64decode(b64))
        img = Image.open(image_file)
        img.save(
            open('%s/%s.%s' % (path, name, image_format), 'wb'),
            image_format.upper()
        )
        img.thumbnail((300, 300), Image.ANTIALIAS)
        img.save(
            open('%s/%s.%s-thumb' % (path, name, image_format), 'wb'),
            image_format.upper()
        )
        return 'images/%s.%s' % (name, image_format)

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


    # def build_query_params(self):
    #
    #     query_params = dict()
    #     get_params = self.request.arguments
    #     for key in get_params:
    #
    #         try:
    #             value = json.loads(get_params['key'])
    #         except ValueError:
    #             value = get_params['key']
    #
    #         if isinstance(value, str):
    #             query_params[key] = value