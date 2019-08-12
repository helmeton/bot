import pandas as pd
from pandas import ExcelWriter

path = 'data.xlsx'


class TaskManager:
	"""docstring for TaskManager"""
	def __init__(self, pictures_df):
		self.tasks = []
		self.build_first_tasks(pictures_df)

		# pictures_df = pd.read_excel(path, sheetname='pictures', index_col='pic_id')
		# queue_df = pd.read_excel(path, sheetname='queue', index_col='u_id')
		# log_df = pd.read_excel(path, sheetname='log', index_col='q_id')

	def build_first_tasks(self, pictures_df):
		"""
		Builds first type tasks.
		"""
		for i in range(len(pictures_df)):
			new_task1 = TaskTextAndPic(pictures_df.iloc[i]['pic_link'], pictures_df.iloc[i].name) # TODO: make task repetition more beautiful
			new_task2 = TaskTextAndPic(pictures_df.iloc[i]['pic_link'], pictures_df.iloc[i].name)
			self.tasks.append(new_task1)
			self.tasks.append(new_task1)

	def add_rephrase_tasks(self, msg):
		for i in range(3):
			new_task = TaskRephrase(msg)
			self.tasks.append(new_task)


class TaskTextAndPic:
	"""docstring for TaskTextAndPic"""
	def __init__(self, pic_link, pic_id):
		self.q_text = 'Опишите, пожалуйста, в одном коротком предложении ситуацию, которая происходит на картинке'
		self.q_type = 1
		self.task = self.q_text + ': ' + pic_link
		self.pic_id = pic_id


class TaskRephrase:
	"""docstring for TaskRephrase"""
	def __init__(self, initial_phrase):
		self.q_type = 2
		self.task = 'Пожалуйста, перефразируйте это предложение: ' + initial_phrase


class TaskValidate(object):
	"""docstring for TaskValidate"""
	def __init__(self, user_response):
		self.arg = user_response
