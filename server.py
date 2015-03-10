from gevent import monkey; monkey.patch_all()

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace
from bottle import Bottle, request

app = Bottle()

class BroadcastMixin(object):
    """ Mix in this class with your Namespace to have a broadcast event method.
    """

    def broadcast_event(self, event, *args):
        """ This is sent to all in the sockets in this particular Namespace,
            including itself.
        """
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)

        for sessid, socket in self.socket.server.sockets.iteritems():
            socket.send_packet(pkt)


class STRPNamespace(BaseNamespace, BroadcastMixin):
    """ Namespace for the sockets
        All socket communication will go through this
    """

    def on_new_input_blob(self, data):
        print 'New input blob: ', data
        # Do algo magic
        self.broadcast_event('new_data', data)


    def on_collision(self, data):
        print 'Collision', data
        # Do algo magic
        self.broadcast_event('new_data', data)


@app.route('/socket.io/<arg:path>')
def socketio(*arg, **kw):
    """ Route to connect a socket
    """
    socketio_manage(request.environ, {'': STRPNamespace}, request=request)
    return "out"


if __name__ == '__main__':
    SocketIOServer(('localhost', 8520), app, policy_server=False).serve_forever()
