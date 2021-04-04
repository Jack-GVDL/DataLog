from typing import *
import json
import os
from Source import *


# Function
def main() -> None:
	# ----- Config -----
	# read config
	with open("./Config_Server.json", "r") as f:
		data = json.load(f)

	# get path
	path_data 	= data["Path_Data"]
	path_layout = data["Path_Layout"]

	# ----- Control_Data -----
	# create Control_Data
	control_data   = Control_Data()
	control_layout = Control_Layout()

	# try to read data from json
	try:
		with open(path_data, "r") as f:
			data = json.load(f)
			control_data.setDictData(data)
	except Exception:
		pass

	try:
		with open(path_layout, "r") as f:
			data = json.load(f)
			control_layout.setDictData(data)
	except Exception:
		pass

	# ----- Server -----
	# start server
	Server_main(
		control_data,
		control_layout,
		path_data,
		path_layout
	)


# Operation
if __name__ != "__main__":
	raise RuntimeError


main()
