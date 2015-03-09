from PredictionController import PredictionController

class MainController(object):
	""" The MainController is the top level Class and the highest layer of the
		application. This Class initialises the entire application and makes sure
		everythin is running.
	"""

	def __init__(self):
		self.predictionController = PredictionController()

	

	def main(self):
		self.predictionController.loop()


if __name__ == '__main__':
	mc = MainController()
	mc.main()