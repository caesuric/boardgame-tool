import tornado.options
import tornado.ioloop
import tornado.web
import logging

from datasocket import SocketHandler
import data

tornado.options.define("port", default=8080, help="run on the given port", type=int)

def main():
    data.process()
    tornado.options.parse_command_line()
    logging.getLogger('tornado.access').disabled = True
    SETTINGS = {
    "debug" : True
    }
    application = tornado.web.Application([
        (r"/datasocket", SocketHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, {"path": "../web/", 'default_filename': 'index.html'})
    ],**SETTINGS)
    application.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()
if __name__ == "__main__":
    main()
