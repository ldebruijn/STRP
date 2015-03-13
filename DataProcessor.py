class DataProcessor(object):

	def __init__(self):
		pass

	def transform_input_data(self, data):
		transform = list()

		try:
			transform.append(data["1"])
			transform.append(data["2"])
			transform.append(data["3"])
			transform.append(data["4"])
			transform.append(data["5"])
			transform.append(data["6"])
			transform.append(data["7"])
			transform.append(int(data["hb"]) % 10)
			transform.append(int(data["c1"]))
			transform.append(int(data["c2"]))
			transform.append(int(data["c3"]))
			transform.append(int(data["c4"]))
			transform.append(int(data["c5"]))
		except (KeyError):
			print("Key does not exist")

		return transform