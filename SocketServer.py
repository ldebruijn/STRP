import tornado.httpserver
import tornado.websocket
import tornado.ioloop
from tornado.ioloop import PeriodicCallback
import tornado.web
from PredictionController import PredictionController
from ResponseBuilder import ResponseBuilder
import os

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

        self.callback = PeriodicCallback(self.update_ecosystem, 120)
        self.callback.start()
        self.write_message("You are connected")


    def update_ecosystem(self):
        """ To simulate a living ecosystem we periodically send updates to the connected clients
            This method handles the processed data, converts it to the output format and updates the clients
        """
        global timestamp

        self.predictionController.loop()
        algorithm = self.predictionController.algorithms['current']
        
        centroids = algorithm.centroids
        node_positions = algorithm.node_positions
        labels = algorithm.labels
        input_data = algorithm.input_data

        response = ResponseBuilder.build_json(timestamp, centroids, input_data, node_positions, labels)
        timestamp += 1

        # print('Ecosystem Update', response)
        self.write_message('Ecosystem Update: %s ' % response)

    def on_message(self, message):
        """ Handler for all messages received by the client
        """
        # self.predictionController.
        self.write_message(message)

    def on_close(self):
        """ Gracefully close the connections to the clients and let them know they are disconnected.
        """
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
