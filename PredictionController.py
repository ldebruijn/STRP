from sklearn.cluster import KMeans
from STRPAlgorithm import STRPAlgorithm
from DataProcessor import DataProcessor
from datetime import datetime, timedelta
from collections import Counter

from random import *
import numpy as np


randBinList = lambda n: [randint(0,9) for b in range(1,n+1)]

class PredictionController(object):
	""" The PredictionController is the managing Class of all the 
		STRPAlgorithm objects. This Class handles when an algorithm should
		run and holds the logic to modify an algorithm based on triggers.
	"""

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
		self.max_percentual_treshold = .1
		self.min_percentual_treshold = .02

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
		""" Main application loop.

		"""
		container = list()
		last_iteration = datetime.now()
		print('Application initialised')
		self.is_running = True

		container.clear()

		# Create dummy data
		for x in range(1, 15):
			container.append(np.array(randBinList(10)))

		# Main application loop
		while(self.is_running):

			if (last_iteration < datetime.now() - timedelta(seconds=1)):
				print('iteration')

				# Add a new entity to the test data to simulate movement
				container.append(np.array(randBinList(10)))
				data = np.asarray(container)
				
				self.fuck_with_entities()

				self.algorithms['current'].run(data)

				self.check_cluster_sizes()

				last_iteration = datetime.now()

	def fuck_with_entities(self):
		""" Method to temper with the input data of an algorithm
			To keep the ecosystem dynamic, there has to be some movement 
			from the nodes between all clusters.

			To achieve this, we periodically temper with the input data of a(n) (set of)
			entities. 

			To have enough of a dynamic ecosystem with both a small and large dataset
			we have a threshold which has both an absolute value and is based on a percentual 
			amount of the total dataset.

			This functionality is explicity requested by the Media Designers, need I say more?
		"""

		algorithm = self.algorithms['current']
		data = algorithm.input_data

		# get number of entities to fuck with
		# Maybe absolute number + percentual increase as the dataset grows
		# Fuck with the input data (shift 1 to 0 and vice versa)

	def check_cluster_sizes(self):
		""" Check the amount of nodes in each cluster of the current algorithm
			If the amount of nodes in a specific cluster is greater or less than a specific 
			threshold, the amount of clusters on all algorithms will be adjusted.

		"""

		algorithm = self.algorithms['current']
		cluster_sizes = Counter(algorithm.labels)
		total_size = len(self.algorithms['current'].labels)

		print(cluster_sizes)

		for cluster_label, cluster_size in cluster_sizes.items():
			"""" Loop through each cluster size and check if the sizes of the cluster
				 Exceed any thresholds we set. If they do, we take action by in- or decreasing
				 the cluster sizes used by the algorithm.

			"""
			
			print(total_size, (self.max_absolute_treshold + (total_size * self.max_percentual_treshold)))

			if (cluster_size > (self.max_absolute_treshold + (total_size * self.max_percentual_treshold))):
				""" If the cluster size is greater than an absolute threshold and a percentual
					amount of the total dataset, increase the amount of clusters for all algorithms
					by 1.
				"""
				print('increasing cluster size!')
				self.adjust_n_clusters(+1)
				break
			
			elif(cluster_size > 2 and 
				cluster_size < (self.min_absolute_treshold + (total_size * self.min_percentual_treshold))):
				""" If the cluster size is greater than 2 (we don't allow a cluster size less than 2)
					
					And the size of this cluster is smaller than an absolute threshold plus a
					percentual amount of the total dataset, decrease the amount of clusters for all 
					algorithms by 1.
				"""
				
				print('decreasing cluster size!')
				self.adjust_n_clusters(-1)
				break
		