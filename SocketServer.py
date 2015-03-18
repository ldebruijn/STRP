import tornado.httpserver
import tornado.websocket
import tornado.ioloop
from tornado.ioloop import PeriodicCallback
import tornado.web
from PredictionController import PredictionController

from ResponseBuilder import ResponseBuilder

import os
import json

clients = []
timestamp = 1

class SocketHandler(tornado.websocket.WebSocketHandler):
    """ SocketHandler class which handles the communication with the socket layer
    """


    def initialize(self, predictionController):
        """ Make sure this class can use the predictionController to operate
        """
        self.predictionController = predictionController

    def check_origin(self, origin):
        return True

    def open(self, *args):
        """ Open a connection to the client, save their socket connection and
            let them know they are connected
        """
        if self not in clients:
            clients.append(self)

        print("New client connected")

        # self.callback = PeriodicCallback(self.update_ecosystem, 1000)
        # self.callback.start()
        # self.write_message("You are connected")


    def update_ecosystem(self):
        """ To simulate a living ecosystem we periodically send updates to the connected clients
            This method handles the processed data, converts it to the output format and updates the clients
        """
        global timestamp

        self.predictionController.process()
        algorithm = self.predictionController.algorithms['current']

        centroids = algorithm.centroids
        node_positions = algorithm.node_positions
        labels = algorithm.labels
        input_data = algorithm.input_data

        response = ResponseBuilder.build_json(timestamp, centroids, input_data, node_positions, labels)
        timestamp += 1

        for con in clients:
            con.write_message(response)


    def on_message(self, message):
        """ Handler for all messages received by the client
        """
        if (message is None):
            return

        convert = json.loads(message)
        convert = json.loads(convert)
        print(type(convert))
        self.predictionController.process_new_node(convert)

        self.update_ecosystem()
        # self.write_message(json.dumps({ message: "success" }))

    def on_close(self):
        """ Gracefully close the connections to the clients and let them know they are disconnected.
        """
        # self.write_message('You are disconnected')

        if self in clients:
            clients.remove(self)

        self.callback.stop()


application = tornado.web.Application([
    (r'/', SocketHandler, dict(predictionController=PredictionController())),
])

def main():
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

