from sklearn.cluster import KMeans
from STRPAlgorithm import STRPAlgorithm
from DataProcessor import DataProcessor
	
from random import *
import numpy as np

randBinList = lambda n: [randint(0,1) for b in range(1,n+1)]

class MainController(object):

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

	

	def main(self):
		data = list()
		for x in range(1,1000):
			data.append(np.array(randBinList(10)))
		data = np.asarray(data)
		self.algorithms['current'].run(data)


if __name__ == '__main__':
	mc = MainController()
	mc.main()