from PredictionController import PredictionController
from server import *
import threading

class MainController(object):
	""" The MainController is the top level Class and the highest layer of the
		application. This Class initialises the entire application and makes sure
		everythin is running.
	"""

	def __init__(self):
		self.socketServer = SocketServer()

	

	def main(self):
		print("Initializing Main Controller")
		self.socketServer.main()



if __name__ == '__main__':
	mc = MainController()
	mc.main()