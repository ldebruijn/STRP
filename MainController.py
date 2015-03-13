from PredictionController import PredictionController
import SocketServer
import threading

class MainController(object):
	""" The MainController is the top level Class and the highest layer of the
		application. This Class initialises the entire application and makes sure
		everythin is running.
	"""

	def __init__(self):
		pass
	

	def main(self):
		print("Initializing Main Controller")
		SocketServer.main()



if __name__ == '__main__':
	mc = MainController()
	mc.main()