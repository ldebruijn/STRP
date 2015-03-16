class DataProcessor(object):

	def __init__(self):
		pass

	def transform_input_data(self, data):
		transform = list()

		try:
			data = data['profiles']
			transform.append(data["1"])
			transform.append(data["2"])
			transform.append(data["3"])
			transform.append(data["4"])
			transform.append(data["5"])
			transform.append(data["6"])
			transform.append(data["7"])
			transform.append(int(data["hb"]) % 10)
			transform.append(int(data["c1"], 16))
			# transform.append(int(data["c2"], 16))
			# transform.append(int(data["c3"], 16))
			# transform.append(int(data["c4"], 16))
			# transform.append(int(data["c5"], 16))
		except (KeyError):
			print("Key does not exist")

		return transform
