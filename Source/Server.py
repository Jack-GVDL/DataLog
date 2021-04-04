from typing import *
from .Interface_DictData import Interface_DictData
from .Log_Data import Log_Data, Control_Data
from .Log_Layout import Log_Widget, Control_Layout
import json
from flask import Flask, request
from flask_cors import CORS
import logging


# Data
control_data_: 		List[Control_Data]		= [Control_Data()]
control_layout_:	List[Control_Layout]	= [Control_Layout()]
path_data_:			List[str]				= ["./Data/Data_Temp.json"]
path_layout_:		List[str]				= ["./Data/Layout_Temp.json"]

app = Flask(__name__)
CORS(app)

log = logging.getLogger("werkzeug")
log.disabled = True


# Function
def Server_main(
	control_data: 	Control_Data,
	control_layout: Control_Layout,
	path_save: 		str = None,
	path_layout: 	str = None,
	port:			int = 8001
) -> None:

	# Control_Log
	control_data_[0]	= control_data
	control_layout_[0]	= control_layout

	# path_save
	if path_save is not None:
		path_data_[0] = path_save

	if path_layout is not None:
		path_layout_[0] = path_layout

	# run
	app.run(port=port)


def getArgument(target: List[Any], name: str, func_convert: Callable[[str], Any]) -> bool:
	try:
		data = request.args.get(name)
		data = func_convert(data)

	except Exception:
		return False

	# if there is existing item
	# it is assumed that that item is the default value
	if not target:
		target.append(data)
	else:
		target[0] = data
	return True


def convertData(data_list: List[Any], type_: int) -> bool:
	# get convert function
	convert_func_table: Dict = {
		Log_Data.DataType.NONE:		None,
		Log_Data.DataType.BOOL:		lambda x: bool(x),
		Log_Data.DataType.INT:		lambda x: int(x),
		Log_Data.DataType.FLOAT:	lambda x: float(x),
		Log_Data.DataType.STR:		lambda x: str(x)
	}

	if type_ not in convert_func_table:
		return False

	convert_func = convert_func_table[type_]
	if convert_func is None:
		return False

	# convert
	try:
		for i in range(len(data_list)):
			data_list[i] = convert_func(data_list[i])
	except Exception:
		return False

	return True


def saveDict(data_dict: Interface_DictData, path: str) -> bool:
	with open(path, "w") as f:
		data = json.dumps(data_dict.getDictData(), indent=None, separators=(',', ':'))
		f.write(data)
	return True


# ----- route -----
@app.route("/GetList_LogData_Name")
def getList_LogData_DataName():
	# ----- compute return data -----
	data_list: List[Any] = []

	# CHECK
	# check if control_data existed or not
	if not control_data_:
		result = json.dumps(data_list)
		return result
	control_data: Control_Data = control_data_[0]

	# [id_, name] to dict
	for log_data in control_data.log_data_list:
		data = [log_data.id_, log_data.name]
		data_list.append(data)

	# to json
	result = json.dumps(data_list)

	# log
	print(f"GetLogList_DataName: size_data_list: {len(data_list)}")

	# RET
	return result


# return a list of id that the data inside is changed
@app.route("/GetList_LogData_Changed")
def getList_LogData_Changed():
	# ----- compute return data -----
	data_list: List[Any] = []

	# CHECK
	# check if control_data existed or not
	if not control_data_:
		result = json.dumps(data_list)
		return result
	control_data: Control_Data = control_data_[0]

	# [id_] to dict
	for id_log_data in control_data.change_list:
		data = id_log_data
		data_list.append(data)

	# TODO
	# reset change
	# control_data.resetChange()

	# to json
	result = json.dumps(data_list)

	# log
	print(f"GetList_LogData_Changed: size_change_list: {len(data_list)}")

	# RET
	return result


@app.route("/AddLog_Data", methods=["POST"])
def addLog_Data():
	# CHECK
	# check if control_data existed or not
	if not control_data_:
		return "{}"
	control_data: 	Control_Data	= control_data_[0]
	path_save:		str				= path_data_[0]

	# ----- get data -----
	# CONFIG
	name:		Any = []
	data_list:	Any = []
	data_type:	Any = []

	# necessary
	if not getArgument(data_type, "type", lambda x: int(x)) or \
		not getArgument(data_list, "data", lambda x: json.loads(x)):
		return "{}"

	# optional
	getArgument(name, "name", lambda x: str(x))

	# unpack
	name:		str 		= name[0]
	data_list:	List[Any]	= data_list[0]
	data_type:	int			= data_type[0]

	# convert type of item in data_list to corresponding data type
	if not convertData(data_list, data_type):
		return "{}"

	# ----- add data -----
	if not control_data.addLog_Data(data_list, data_type, name):
		return "{}"

	# ----- save data -----
	with open(path_save, "w") as f:
		data = json.dumps(control_data.getDictData(), indent=None, separators=(',', ':'))
		f.write(data)

	# ----- log -----
	print(f"AddLog_Data: size data_list: {len(data_list)}; type: {data_type}; name: {name}")

	return "{}"


@app.route("/RmLog_Data", methods=["POST"])
def rmLog_Data():
	# CHECK
	# check if control_data existed or not
	if not control_data_:
		return "{}"
	control_data: 	Control_Data	= control_data_[0]
	path_save:		str				= path_data_[0]

	# ----- get data -----
	# config
	id_:	Any = []

	# necessary
	if not getArgument(id_, "id", lambda x: int(x)):
		return "{}"

	# unpack
	id_:	int = id_[0]

	# ----- rm data -----
	if not control_data.rmLog_Data(id_):
		return "{}"

	# ----- save data -----
	with open(path_save, "w") as f:
		data = json.dumps(control_data.getDictData(), indent=None, separators=(',', ':'))
		f.write(data)

	# ----- get log -----
	print(f"RmLog_Data: id: {id_}")

	return "{}"


@app.route("/GetLog_Data", methods=["POST"])
def getLog_Data():
	# CHECK
	# check if control_data existed or not
	if not control_data_:
		return "{}"
	control_data: 	Control_Data	= control_data_[0]

	# ----- get data -----
	# config
	id_:	Any = []

	# necessary
	if not getArgument(id_, "id", lambda x: int(x)):
		return "{}"

	# unpack
	id_:	int = id_[0]

	# ----- get data -----
	log_data: Log_Data = control_data.getLog_Data(id_)
	if log_data is None:
		return "{}"

	# convert Log_Data to dict
	# then from dict to json
	data = log_data.getDictData()
	data = json.dumps(data)

	# ----- get log -----
	print(f"GetLog_Data: id: {id_}; name: {log_data.name}")

	# RET
	return data


@app.route("/GetList_LogWidget_ID")
def getList_LogWidget_ID():
	# ----- compute return data -----
	data_list: List[Any] = []

	# CHECK
	# check if control_data existed or not
	if not control_data_:
		result = json.dumps(data_list)
		return result
	control_layout: Control_Layout = control_layout_[0]

	# get list of id
	for log_widget in control_layout.log_widget_list:
		data_list.append(log_widget.id_)

	# to json
	result = json.dumps(data_list)

	# log
	print(f"GetList_LogWidget_ID: size_data_list: {len(data_list)}")

	# RET
	return result


@app.route("/GetLog_Widget", methods=["POST"])
def getLog_Widget():
	# check if control_data existed or not
	if not control_data_:
		return "{}"

	control_layout: Control_Layout 	= control_layout_[0]
	path_save:		str				= path_layout_[0]

	# ----- get data -----
	# config
	id_: Any = []

	# necessary
	if not getArgument(id_, "id", lambda x: int(x)):
		return "{}"

	# unpack
	id_: int = id_[0]

	# get log_widget
	log_widget = control_layout.getLog_Widget(id_)
	if log_widget is None:
		return "{}"

	# to json
	data = log_widget.getDictData()
	data = json.dumps(data)

	# ----- save data -----
	saveDict(control_layout, path_save)

	# ----- log -----
	print(f"GetLog_Widget: id: {id_}")

	# RET
	return data


@app.route("/AddLog_Widget", methods=["POST"])
def addLog_Widget():
	# CONFIG
	data: Dict = {
		"id": -1
	}

	# CHECK
	# check if control_data existed or not
	if not control_data_:
		ret = json.dumps(data)
		return ret

	control_layout: Control_Layout 	= control_layout_[0]
	path_save:		str				= path_layout_[0]

	# ----- get data -----
	# config
	component:	Any = [""]

	# necessary
	# ...

	# optional
	getArgument(component, "component", lambda x: x)

	# unpack
	component = component[0]

	# ----- create widget -----
	# create log_widget
	log_widget = control_layout.createWidget()
	if log_widget is None:
		ret = json.dumps(data)
		return ret

	# config widget (if exist configuration)
	log_widget.component = component

	# ----- save data -----
	saveDict(control_layout, path_save)

	# ----- log -----
	print(f"AddLog_Widget: id: {log_widget.id_}")

	# RET
	data["id"] = log_widget.id_
	ret = json.dumps(data)
	return ret


@app.route("/RmLog_Widget", methods=["POST"])
def rmLog_Widget():
	# CONFIG
	data: Dict = {
		"return": False
	}

	# CHECK
	# check if control_data existed or not
	if not control_data_:
		data: str = json.dumps(data)
		return data

	control_layout: Control_Layout 	= control_layout_[0]
	path_save:		str				= path_layout_[0]

	# ----- get data -----
	# config
	id_: Any = []

	# necessary
	if not getArgument(id_, "id", lambda x: int(x)):
		data: str = json.dumps(data)
		return data

	# unpack
	id_: int = id_[0]

	# ----- rm data -----
	if not control_layout.rmLog_Widget(id_):
		return "{}"

	# ----- save data -----
	saveDict(control_layout, path_save)

	# ----- log -----
	print(f"RmLog_Widget: id: {id_}")

	# RET
	data["return"] = True
	data: str = json.dumps(data)
	return data


@app.route("/ConfigLog_Widget", methods=["POST"])
def configLog_Widget():
	# CONFIG
	data: Dict = {
		"return": False
	}

	# CHECK
	# check if control_data existed or not
	if not control_data_:
		data: str = json.dumps(data)
		return data

	control_layout: Control_Layout 	= control_layout_[0]
	path_save:		str				= path_layout_[0]

	# ----- get data -----
	# config
	id_: 		List[Any] = []
	geometry: 	List[Any] = [None]
	name:		List[Any] = [None]
	component:	List[Any] = [None]
	state:		List[Any] = [None]
	custom:		List[Any] = [None]

	# necessary
	if not getArgument(id_, "id", lambda x: int(x)):
		data: str = json.dumps(data)
		return data

	# optional
	getArgument(geometry,	"geometry",		lambda x: [int(item) for item in x.split(",")][:4])
	getArgument(name,		"name",			lambda x: str(x))
	getArgument(component,	"component",	lambda x: str(x))
	getArgument(state,		"state",		lambda x: json.loads(x))
	getArgument(custom,		"custom",		lambda x: json.loads(x))

	# unpack
	id_: 		int 		= id_[0]
	geometry: 	List[int] 	= geometry[0]
	name:		str 		= name[0]
	component:	str 		= component[0]
	state:		Dict 		= state[0]
	custom:		Dict 		= custom[0]

	# ----- get log_widget -----
	log_widget: Log_Widget = control_layout.getLog_Widget(id_)
	if log_widget is None:
		return "{}"

	# ----- config data -----
	if geometry is not None:
		log_widget.geometry = geometry
	if name is not None:
		log_widget.name = name
	if component is not None:
		log_widget.component = component
	if state is not None:
		log_widget.state = state
	if custom is not None:
		log_widget.custom = custom

	# ----- save data -----
	saveDict(control_layout, path_save)

	# ----- log -----
	print(f"ConfigLog_Widget: id: {id_}")

	# RET
	data["return"] = True
	data: str = json.dumps(data)
	return data


# Operation
if __name__ == "__main__":
	raise RuntimeError
