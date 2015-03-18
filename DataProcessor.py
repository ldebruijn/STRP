class DataProcessor(object):

	def __init__(self):
		pass

	def transform_input_data(self, data):
		transform = list()

		try:
			data = data['profiles']
			transform.append(1 if data["1"] else 0)
			transform.append(1 if data["2"] else 0)
			transform.append(1 if data["3"] else 0)
			transform.append(1 if data["5"] else 0)
			transform.append(1 if data["4"] else 0)
			transform.append(1 if data["6"] else 0)
			transform.append(1 if data["7"] else 0)
			transform.append(int(data["hb"]) % 10)
			transform.append(int(data["c1"], 16))
			# transform.append(int(data["c2"], 16))
			# transform.append(int(data["c3"], 16))
			# transform.append(int(data["c4"], 16))
			# transform.append(int(data["c5"], 16))
		except (KeyError):
			print("Key does not exist")

		return transform
