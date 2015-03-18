from sklearn.cluster import KMeans
from STRPAlgorithm import STRPAlgorithm
from DataProcessor import DataProcessor
from datetime import datetime, timedelta
from collections import Counter
from copy import deepcopy
from pythonosc import osc_message_builder, udp_client

from random import *
import numpy as np
import math
import uuid


randBinList = lambda n: [randint(0,9) for b in range(1,n+1)]

FILTER_NEW_BLOB = '/newBlob'
FILTER_INCREASE_CLUSTER = '/increaseCluster'
FILTER_DECREASE_CLUSTER = '/decreaseCluster'
start_data = [ 
    {
        'profiles': {
            '6': True, 
            'hb': 85, 
            '1': True, 
            'userId': 'ac44b0d2-2253-482b-b458-bafc0ad04045', 
            '3': True, 
            '2': True, 
            '7': True, 
            '5': True, 
            'c1': 'FAAB11', 
            '4': True
        }
    },
    {
        'profiles': {
            '6': False, 
            'hb': 79, 
            '1': True, 
            'userId': 'bbb57860-042b-4f95-9337-756c1e9595c5', 
            '3': True, 
            '2': True, 
            '7': True, 
            '5': True, 
            'c1': '3d4499', 
            '4': False
        }
    }
]


class PredictionController(object):
	""" The PredictionController is the managing Class of all the
		STRPAlgorithm objects. This Class handles when an algorithm should
		run and holds the logic to modify an algorithm based on triggers.
	"""

	def __init__(self):
		self.n_clusters = 2;

		self.algorithms = {
			'current': STRPAlgorithm(self.n_clusters),
			'future': STRPAlgorithm(self.n_clusters)
		}

		self.data_processors = {
			'current': DataProcessor(),
			'future': DataProcessor()
		}

		self.max_absolute_treshold = 13
		self.min_absolute_treshold = 5
		self.max_percentual_treshold = .1
		self.min_percentual_treshold = .02

		self.entity_temper_percentual_threshold = .2

		self.is_running = False

		self.container = list()
		self.processed_nodes = list()
		self.raw_data = start_data

		self.client = udp_client.UDPClient('localhost', 8000)


		self.last_iteration = datetime.now()
		print('Application initialised')
		self.is_running = True

		# Create dummy data
		for x in range(1, 3):
			self.processed_nodes.append(np.array(randBinList(9)))


	def send_OSC_message(self, address):
		msg = osc_message_builder.OscMessageBuilder(address=address)
		msg.add_arg(100)
		msg = msg.build()
		self.client.send(msg)

	def process_new_node(self, data):
		""" Process a new node. Transform the data into a runnable format for our algorithm
			Add a universal unique identifier to the node.
			Save the raw data and the transformed data.
		"""
		self.send_OSC_message(FILTER_NEW_BLOB)
		tranformed_data = self.data_processors['current'].transform_input_data(data)
		data['profiles']['userId'] = str(uuid.uuid4())
		self.raw_data.append(data)
		self.processed_nodes.append(tranformed_data)
		return data['profiles']['userId']

	def adjust_n_clusters(self, amount):
		""" Adjust the number of clusters in each algorithm.

		"""
		print("adjusting clusters", self.n_clusters, amount)
		self.n_clusters += amount

		for key, value in self.algorithms.items():
			print(key, value)
			value.adjust_n_clusters(self.n_clusters)


	def process(self):
		""" Main application loop.

		"""

		print('iteration')

		# Add a new entity to the test data to simulate movement
		self.data = np.asarray(self.processed_nodes)

		self.algorithms['current'].run(self.data)

		self.fuck_with_entities()
		self.check_cluster_sizes()

		self.last_iteration = datetime.now()

		# Set the last processed algorithm to the buffer
		self.algorithms['current'] = deepcopy(self.algorithms['current'])

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

		# Determine how many items there should be tempered with depending on dataset size
		entities_to_fuck_with = int(math.floor(len(algorithm.labels) * self.entity_temper_percentual_threshold))


		for x in range(1, entities_to_fuck_with):
			# Fetch a random item from the entities input data
			index = randint(0, len(algorithm.labels) - 1)
			entity = data[index]

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
				self.send_OSC_message(FILTER_INCREASE_CLUSTER)
				break

			elif(len(cluster_sizes) > 2 and
				cluster_size < (self.min_absolute_treshold + (total_size * self.min_percentual_treshold))):
				""" If the cluster size is greater than 2 (we don't allow a cluster size less than 2)

					And the size of this cluster is smaller than an absolute threshold plus a
					percentual amount of the total dataset, decrease the amount of clusters for all
					algorithms by 1.
				"""

				print('decreasing cluster size!')
				self.adjust_n_clusters(-1)
				self.send_OSC_message(FILTER_DECREASE_CLUSTER)
				break
