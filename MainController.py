from PredictionController import PredictionController

class MainController(object):

	def __init__(self):
		self.predictionController = PredictionController()

	

	def main(self):
		self.predictionController.loop()


if __name__ == '__main__':
	mc = MainController()
	mc.main()