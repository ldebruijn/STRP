import tornado.httpserver
import tornado.websocket
import tornado.ioloop
from tornado.ioloop import PeriodicCallback
import tornado.web
from PredictionController import PredictionController
import os

clients = []

class SocketHandler(tornado.websocket.WebSocketHandler):

    def initialize(self, predictionController):
        self.predictionController = predictionController

    def check_origin(self, origin):
        return True       

    # Open connection to client and let them know they are connected
    def open(self, *args):
        if self not in clients:
            clients.append(self)

        print("New client connected")

        self.callback = PeriodicCallback(self.update_ecosystem, 120)
        self.callback.start()
        self.write_message("You are connected")


    def update_ecosystem(self):
        self.predictionController.loop()
        algorithm = self.predictionController.algorithms['current']
        centroids = algorithm.centroids
        node_positions = algorithm.node_positions
        labels = algorithm.labels

        print(centroids)
        print('Ecosystem Update')
        self.write_message('Ecosystem Update')

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        self.write_message('You are disconnected')

        if self in clients:
            clients.remove(self)

        self.callback.stop()

application = tornado.web.Application([
    (r'/', SocketHandler, dict(predictionController=PredictionController())),
])

def main(predictionController=None):
    # if (not predictionController):
    #     predictionController = PredictionController()

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
