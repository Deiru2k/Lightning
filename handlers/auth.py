from base import BaseHandler
from tornado.gen import coroutine
import rethinkdb as r


class SignUpHandler(BaseHandler):

    @coroutine
    def post(self):

        invite = self.request.data
        query = self.db.requests.get(invite['code'])
        result = yield self.db.run_query(query)
        if not result:
            self.error(code=403, message="Invalid Invite Code", data=invite['code'])
            return
        if result['used']:
            self.error(code=403, message="Invite Code Already Used")
        yield self.db.run_query(query.update({"used": True}))
        now = r.now()
        user = {
            "email": invite['email'],
            "createdAt": now,
            "modifiedAt": now
        }
        query = self.db.users.insert(user)
        result = yield self.db.run_query(query)
        key = result['generated_keys'][0]
        response = {
            "key": key
        }
        self.respond(response, code=201)