from tornado.web import Application
from tornado.ioloop import IOLoop
from routes import handlers


app = Application(
    handlers=handlers
)


if __name__ == '__main__':

    print("\nRoute Mapping:")
    for route in handlers:
        print("%s -> %s" % (route[1].__name__, route[0]))

    app.listen(8080)
    IOLoop.instance().start()

