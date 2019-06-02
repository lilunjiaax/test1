
class A:
	def __init__(self):
		self.a = 5
		print('A', self.a)


	def fun1(self):
		print('这是A类')



class B(A):
	"""docstring for ClassName"""
	# def __init__(self):
	# 	super(B, self).__init__()
	# 	print('B', self.a)

	def pick(self):
		print("pick",self.a)

	def fun1(self):
		print('这是B类')
	def execute(self):
		print('正在执行execute函数')
		self.fun1()
		
a = A()
b = B()

b.execute()

# kk = 99
# class KK:
# 	def __init__(self,num):
# 		self.pp = num + 1
# 		print(num)

# k = KK(kk)
# print('key', k.pp)
