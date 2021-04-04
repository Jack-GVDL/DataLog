from typing import *
from .Interface_DictData import Interface_DictData


# Data Structure
class Log_Widget(Interface_DictData):

	# Enum
	class Label:
		ID:			int = 0
		GEOMETRY:	int = 1
		NAME:		int = 2
		COMPONENT:	int = 3
		STATE:		int = 4
		CUSTOM:		int = 5
		SIZE_MAX:	int = 6

	def __init__(self):
		super().__init__()
		
		# data
		self.id_:		int 		= -1
		self.name:		str			= ""
		self.geometry:	List[int] 	= [-1, -1, -1, -1]
		self.component:	str 		= ""
		self.state:		Dict		= {}
		self.custom:	Dict		= {}
		
		# operation
		self.state["is_focused"] = False
		
	def __del__(self):
		return
		
	# Property
	# ...
		
	# Operation
	# ...

	# Interface
	def getDictData(self) -> Dict:
		return {
			Log_Widget.Label.ID:		self.id_,
			Log_Widget.Label.NAME:		self.name,
			Log_Widget.Label.GEOMETRY:	self.geometry,
			Log_Widget.Label.COMPONENT:	self.component,
			Log_Widget.Label.STATE:		self.state,
			Log_Widget.Label.CUSTOM:	self.custom
		}

	def setDictData(self, data: Dict) -> None:
		self.id_			= data[str(Log_Widget.Label.ID)]
		self.name			= data[str(Log_Widget.Label.NAME)]
		self.geometry		= data[str(Log_Widget.Label.GEOMETRY)]
		self.component		= data[str(Log_Widget.Label.COMPONENT)]
		self.state			= data[str(Log_Widget.Label.STATE)]
		self.custom			= data[str(Log_Widget.Label.CUSTOM)]
	
	# Protected
	# ...


class Control_Layout(Interface_DictData):

	class Label:
		WIDGET_LIST:	int = 0
		INDEX:			int = 1
		SIZE_MAX:		int = 2

	def __init__(self):
		super().__init__()

		# data
		self.log_widget_list:	List[Log_Widget] 	= []
		self.index:				int					= 1

		# operation
		# ...

	def __del__(self):
		return

	# Property
	# ...

	# Operation
	def createWidget(self) -> Log_Widget:
		# get id of current data
		# avoid using "0"
		id_: int = self.index
		self.index += 1

		# create Log_Widget
		log_widget = Log_Widget()
		log_widget.id_ = id_

		# add to list
		self.log_widget_list.append(log_widget)

		# return widget
		return log_widget

	def rmLog_Widget(self, id_: int) -> bool:
		index: int = self._findIndex_(self.log_widget_list, lambda x: x.id_ == id_)
		if index < 0:
			return False

		self.log_widget_list.pop(index)
		return True

	def getLog_Widget(self, id_: int) -> Log_Widget:
		index: int = self._findIndex_(self.log_widget_list, lambda x: x.id_ == id_)
		if index < 0:
			return None

		return self.log_widget_list[index]

	# Interface
	def getDictData(self) -> Dict:
		log_widget_list: List[Dict] = []
		for log_widget in self.log_widget_list:
			log_widget_list.append(log_widget.getDictData())

		return {
			Control_Layout.Label.WIDGET_LIST:	log_widget_list,
			Control_Layout.Label.INDEX:			self.index
		}

	def setDictData(self, data: Dict) -> None:
		# log widget list
		log_widget_list: List[Any] = \
			self._getDataFromDict_(data, str(Control_Layout.Label.WIDGET_LIST), [])

		for item in log_widget_list:
			log_widget = Log_Widget()
			log_widget.setDictData(item)
			self.log_widget_list.append(log_widget)

		# index
		self.index = self._getDataFromDict_(data, str(Control_Layout.Label.INDEX), 1)

	# Protected
	def _findIndex_(self, list_: List[Any], cmp: Callable[[Any], bool]) -> int:
		for index, item in enumerate(list_):
			if not cmp(item):
				continue
			return index
		return -1
