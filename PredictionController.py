from sklearn.cluster import KMeans
from STRPAlgorithm import STRPAlgorithm
from DataProcessor import DataProcessor
from datetime import datetime, timedelta

from random import *
import numpy as np


randBinList = lambda n: [randint(0,9) for b in range(1,n+1)]

class PredictionController(object):

	def __init__(self):
		self.default_n_clusters = 10;

		self.algorithms = {
			'current': STRPAlgorithm(self.default_n_clusters),
			'buffer': STRPAlgorithm(self.default_n_clusters)
		}

		self.data_processors = {
			'current': DataProcessor(),
			'buffer': DataProcessor()
		}

		max_treshold = 0
		min_treshold = 0

		self.is_running = False


	def loop(self):
		container = list()
		last_iteration = datetime.now()
		print('Application initialised')
		self.is_running = True

		while(self.is_running):

			if (last_iteration < datetime.now() - timedelta(seconds=3)):
				print('iteration')
				container.clear()

				for x in range(1,100):
					container.append(np.array(randBinList(10)))
				data = np.asarray(container)
				
				self.algorithms['current'].run(data)

				last_iteration = datetime.now()