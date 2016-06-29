from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import define, options, parse_command_line
from app import app


if __name__ == "__main__":
    parse_command_line()        
    server = HTTPServer(WSGIContainer(app))
    server.bind(8888)
    server.start(0)
    #server.listen(8000)
    IOLoop.instance().start()
