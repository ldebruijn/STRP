import tornado.httpserver
import tornado.websocket
import tornado.ioloop
from tornado.ioloop import PeriodicCallback
import tornado.web

clients = []

class SocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True       

    # Open connection to client and let them know they are connected
    def open(self, *args):
        if self not in clients:
            clients.append(self)

        print("New client connected")

        self.callback = PeriodicCallback(self.send_hello, 120)
        self.callback.start()
        self.write_message("You are connected")


    def send_hello(self):
        print('hello')
        self.write_message('hello')

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        self.write_message('You are disconnected')

        if self in clients:
            clients.remove(self)

        self.callback.stop()

    

application = tornado.web.Application([
    (r'/', SocketHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
