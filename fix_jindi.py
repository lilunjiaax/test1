# 采用策略模式重构代码

# 行为类的基类
class ReadData:
	def __init__(self, jindi_data):
		self.data0 = {}
		self.data1 = {}
		self.results = jindi_data['segments']

	def read_to_dict(self):
		# 针对三张表，他们各自有不同的转化方法，行为类子类里面重写
		pass


# 资产负债表读取原始数据的重写
class ReadDataBlance(ReadData):

	def read_to_dict(self):
		for result in self.results:
            try:
                info = result['inforow']
            except Exception as e:
                print('------->出现缺少inforow的情况<--------')
                print('该字典无 inforow ')
                info = '备注'
            row_list = result['rows']
            for line in row_list:
                # 此时的line是一个字典
                if line['tds'][0]['value'] == '项目' or line['tds'][0]['value'] == '':
                    # 判断出表格中的这一行是第一行或者空行
                    continue

                else:
                    '''每一行都包含未调整，调整的值'''
                    if line['tds'][0]['value'] == '其中：优先股':
                        key = info + '-' + line['tds'][2]['value'][3:]
                    if line['tds'][0]['value'] == '永续债':
                        key = info + '-' + line['tds'][2]['value']
                    else:
                        key = line['tds'][0]['value']

                    value0 = line['tds'][2]['value']
                    value1 = line['tds'][3]['value']
                    self.data0.update({key: value0})
                    self.data1.update({key: value1})

        # return self.data0, self.data1



# 利润表表读取原始数据的重写
class ReadDataIncome(ReadData):

	def read_to_dict(self):
		# 数据选取方法与资产负债表一样，只是初步的切片会有差异
		pass


# 现金流量表读取原始数据的重写
class ReadDataCashFlow(ReadData):

	def read_to_dict(self):
		# 数据选取方法与资产负债表一样，只是初步的切片会有差异
		pass




# 对于共有的方法我们采取的方法是直接放在客户类里面
# 客户类的基类，确定一个各家公司的最基本的方法
class BaseClient:
	'''首先需要根据传递的table_name来确定实例化哪个行为类'''
	def __init__(self, table_name, jindi_data):
		'''
		self.read是类的实例对象
		slef.read属性为self.read.data0,self.read.data1
		self.read方法为self.read.read_to_dict()
		'''
		self.fix_dict_yuyi = {}

		if table_name == '资产负债表':
			self.read = ReadDataBlance(jindi_data)
		if table_name == '利润表':
			self.read = ReadDataIncome(jindi_data)
		if table_name == '现金流量表':
			self.read = ReadDataCashFlow(jindi_data)
			
		self.read.read_to_dict()

	def fix_value(self):
		# 对于value的修复方法都是共有的
		for key in self.read.data0:
			if self.read.data0['key'] == '-':
				self.read.data0['key'] = 'None'
			else:
				self.read.data0['key'] = self.read.data0['key'].replace(',','')

			if self.read.data1['key'] == '-':
				self.read.data1['key'] = 'None'
			else:
				self.read.data1['key'] = self.read.data1['key'].replace(',','')


	def fix_key(self):
		# 替换修复key的值,在客户类子类中完成
		pass


class FixDataJindi(BaseClient):
	def fix_key(self):
		# 当yuyi中的name为列表时，也是可以正确查找的
		for old_key in self.read.data0:
            results = es.search(FINANCE_MATCH_INDEX,
                    doc_type='d_type',
                    body={"query": {"bool": {"must": [{"term": {"alias.name.keyword": old_key}}], "must_not": [], "should": []}},
                                                "from": 0, "size": 10, "sort": [], "aggs": {}})['hits']['hits']

            if results:
                # 存在我们检索到的值
                new_key = results[0]['_source']['alias'][1]['name'][0]

            else:
                print('{} 在yuyi数据库中不存在'.format(old_key))
                new_key = input('请手动输入对应的yuyi数据:')
                # 将数据补充到统计字典中
                self.fix_dict_yuyi.update({new_key, old_key})
            # 对key进行修复
            self.read.data0[new_key], self.read.data1[new_key] = self.read.data0.pop(old_key), self.read.data1.pop(old_key)


    def update_yuyi_index(self):
    	for yuyi_name in self.fix_dict_yuyi:
    		# 构造出带插入的字典
            # 插入一条document,id自定
            # 由于现在elasticsearch连接不上，错误在网上也没查到，只好暂定
            # 2019/05/29 21:59:43 [W] [visitor.go:139] [secret_es_visitor106] start new visitor connection error: custom listener for [secret_es] doesn't exist
            pass

    def execute_function(self):
    	self.fix_value()
    	self.fix_key()
    	self.update_yuyi_index()
    	pass

































