from sklearn.cluster import KMeans
from STRPAlgorithm import STRPAlgorithm
from DataProcessor import DataProcessor
from datetime import datetime, timedelta
from collections import Counter

from random import *
import numpy as np


randBinList = lambda n: [randint(0,9) for b in range(1,n+1)]

class PredictionController(object):

	def __init__(self):
		self.n_clusters = 2;

		self.algorithms = {
			'current': STRPAlgorithm(self.n_clusters),
			'buffer': STRPAlgorithm(self.n_clusters)
		}

		self.data_processors = {
			'current': DataProcessor(),
			'buffer': DataProcessor()
		}

		self.max_absolute_treshold = 13
		self.min_absolute_treshold = 5
		self.max_percentual_treshold = 5
		self.min_percentual_treshold = 1

		self.is_running = False


	def adjust_n_clusters(self, amount):
		""" Adjust the number of clusters in each algorithm.

		"""
		print("adjusting clusters", self.n_clusters, amount)
		self.n_clusters += amount

		for key, value in self.algorithms.items():
			print(key, value)
			value.adjust_n_clusters(self.n_clusters)


	def loop(self):
		container = list()
		last_iteration = datetime.now()
		print('Application initialised')
		self.is_running = True

		container.clear()

		for x in range(1, 15):
			container.append(np.array(randBinList(10)))

		# Main application loop
		while(self.is_running):

			if (last_iteration < datetime.now() - timedelta(seconds=1)):
				print('iteration')
				container.append(np.array(randBinList(10)))
				data = np.asarray(container)
				
				self.algorithms['current'].run(data)
				self.check_cluster_sizes()

				last_iteration = datetime.now()

	def check_cluster_sizes(self):
		""" Check the amount of nodes in each cluster of the current algorithm
			If the amount of nodes in a specific cluster is greater or less than a specific 
			threshold, the amount of clusters on all algorithms will be adjusted.

		"""

		algorithm = self.algorithms['current']
		cluster_sizes = Counter(algorithm.labels)

		print(cluster_sizes)

		for cluster_label, cluster_size in cluster_sizes.items():

			# If a cluster size is greater than the absolute threshold, increase cluster size by 1.
			if (cluster_size > self.max_absolute_treshold):
				print('increasing cluster size!')
				self.adjust_n_clusters(+1)
				break
			
			# If a cluster size is less than the absolute threshold, decrease cluster size by 1.
			elif(cluster_size > 2 and cluster_size < self.min_absolute_treshold):
				self.adjust_n_clusters(-1)
				break
		