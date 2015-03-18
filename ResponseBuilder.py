import json

class ResponseBuilder(object):

	@staticmethod
	def build_json(timestamp, centroids, input_data, positions, labels, newNode):
		"""
			Build a json according to the below format based on the input given.

				{
				    "timestamp": 1,
				    "nodes": [
				        {
				            "userId": 1,
				            "input_data": [],
				            "cluster": 3,
				            "position": [3, 4]
				        },
				        {
				            "userId": 2,
				            "input_data": [],
				            "cluster": 6,
				            "position": [16, 3]
				        }
				    ],
				    "clusters": [ 
				        {
				            "1": [20, 24],
				            "2": [14, 7]
				        }
				    ]

				}
		"""
		response = dict()
		response['timestamp'] = timestamp
		response['newestNode'] = newNode
		nodes = list()

		for i, n in enumerate(positions):
			node = dict()
			node['userId'] = '1'
			node['input_data'] = [int(x) for x in input_data[i]]
			node['cluster'] = int(labels[i])
			node['position'] = list((float(x) for x in n))

			nodes.append(node)

		response['nodes'] = nodes

		clusters = dict()
		for i, n in enumerate(centroids):
			clusters[str(i)] = list(n)

		response['clusters'] = clusters

		return json.dumps(response, default=ResponseBuilder._serializer, sort_keys=True, indent=4)
	
	@staticmethod
	def _serializer(obj):
		""" Method to convert non-serializable objects
			into a serializable object, if available.
		"""
		return obj.isoformat() if hasattr(obj, 'isoformat') else obj
        