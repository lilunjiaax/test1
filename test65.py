
"""
dian 9 是测试的
dian 99 是正式的
"""


class Base:
	def __init__(self, a):
		self.a = a
	def read(self):
		print('hahahha')


class AA(Base):
	"""docstring for ClassName"""
	def read(self):
		super(Base, self).read()
		print('AAAAAAA')
		


a = AA(2)
a.read()



class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		