from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from collections import namedtuple
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import random

class STRPAlgorithm(object):
	""" STRPAlgorithm is a class which olds all the logic behind the 
		clustering algorithm. All direct interaction with the algorithm
		is done here.
	"""

	def __init__(self, n_clusters=10):
		self.n_clusters = n_clusters
		self.estimator = KMeans(init='k-means++', n_clusters=n_clusters)
		self.centroids = None 
		self.node_positions = None
		self.labels = None

	def adjust_n_clusters(self, n_clusters):
		""" Re-initialize the estimator with an adjusted amount of clusters.
			Doing it this way the other properties of the object will not change
			while the amount of clusters can be adjusted.

		"""
		self.estimator = KMeans(init='k-means++', n_clusters=n_clusters)

	def run(self, data):
		""" Run the estimator with the given parameters.
			Reduce the data to a 2 Dimensional format so that the positions of each node can be read
			Have the estimator run on the reduced data to get the results we want

			* Save the centroids of each cluster
			* Save the node positions (reduced_data)
			* Save the label of each node (which cluster each node belongs to)
		"""
		reduced_data = PCA(n_components=2).fit_transform(data)

		self.estimator.fit_transform(reduced_data)
		self.centroids = self.estimator.cluster_centers_
		self.node_positions = reduced_data
		self.labels = self.estimator.labels_

		# Enable visualising when debugging
		self.visualize(reduced_data)

	def visualize(self, reduced_data):
		""" Visualise the estimation of the algorithm using matplotlib.
			Fairly standard setup.

		"""
		# Step size of the mesh. Decrease to increase the quality of the VQ.
		h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].
		
		# Plot the decision boundary. For that, we will assign a color to each
		x_min, x_max = reduced_data[:, 0].min() + 1, reduced_data[:, 0].max() - 1
		y_min, y_max = reduced_data[:, 1].min() + 1, reduced_data[:, 1].max() - 1
		xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

		# Obtain labels for each point in mesh. Use last trained model.
		Z = self.estimator.predict(np.c_[xx.ravel(), yy.ravel()])

		# Put the result into a color plot
		Z = Z.reshape(xx.shape)
		
		plt.figure(1)
		plt.clf()
		plt.imshow(Z, interpolation='nearest',
		           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
		           cmap=plt.cm.Paired,
		           aspect='auto', origin='lower')

		plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=4)
		# Plot the centroids as a white X
		centroids = self.estimator.cluster_centers_
		plt.scatter(centroids[:, 0], centroids[:, 1],
		            marker='x', s=169, linewidths=3,
		            color='w', zorder=10)
		plt.title('K-means clustering with random data (PCA-reduced data)\n'
		          'Centroids are marked with white cross')
		plt.xlim(x_min, x_max)
		plt.ylim(y_min, y_max)
		plt.xticks(())
		plt.yticks(())
		plt.show()