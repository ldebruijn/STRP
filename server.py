import asyncio
import json
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

class BroadcastServerFactory(WebSocketServerFactory):
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, data):
        for c in self.clients:
            c.sendMessage(data.encode('utf8'))


class STRPServerProtocol(WebSocketServerProtocol):
    """ Server protocol for the sockets
        All socket communication will go through this
    """

    def onConnect(self, request):
        print("New connection: {0}".format(request.peer))


    def onOpen(self):
        self.factory.register(self)


    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


    def onMessage(self, payload, isBinary):
        """ Handles all incoming messages
        """
        if isBinary:
            print("Binary message: {0} bytes".format(len(payload)))
        else:
            self.decodePayload(payload)


    def decodePayload(self, payload):
        """ Decode payload implements a socket.io like protocol
            This will call the handler function based on the message
        """

        decodedPayload = json.loads(payload.decode('utf8'))
        message = "on_{0}".format(decodedPayload['message'])

        # Get the method by string, based on the message
        method = getattr(self, message)

        try:
            # Run the handler with the data
            method(decodedPayload['data'])
        except NameError:
            pass


    def broadcast(self, message, data):
        """ Broadcasts message to all sockets
            Uses socket.io like protocol with message
        """
        # Create the dict for the data
        sendableObject = {
            'message': message,
            'data': data
        }

        # Stringify the dict and send it
        jsonString = json.dumps(sendableObject)
        self.factory.broadcast(jsonString)


    def on_new_input_blob(self, data):
        """ Handles new input blob
        """
        print("New input blob: {0}".format(data))
        # magic
        self.broadcast('new_blob', data)


    def on_collision(self, data):
        """ Handles collision
        """
        print("Collision: {0}".format(data))
        #magic
        print(data)



if __name__ == '__main__':
    ServerFactory = BroadcastServerFactory

    factory = ServerFactory("ws://localhost:8520", debug=False)
    factory.protocol = STRPServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', 8520)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
