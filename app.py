from tornado.web import Application
from tornado.ioloop import IOLoop
from routes import handlers
from base import APP_PORT


app = Application(
    handlers=handlers
)


if __name__ == '__main__':

    print("\nRoute Mapping:")
    for route in handlers:
        print("%s -> %s" % (route[1].__name__, route[0]))

    app.listen(APP_PORT)
    IOLoop.instance().start()

