# import pysnooper


# @pysnooper.snoop()
# def aa(num):
# 	for i in range(num):
# 		return i



# def aa(key, num1, num2, num3):
# 	if key == 'one':
# 		return {'one':num1}
# 	if key == 'two':
# 		return {'two':num2}


# print(aa('one',11,22,33))




# ({'compare_source': 'wind', 'msg': '键在wind中而不在jindi中', 'wind_key': '所有者权益', 'wind_value': 'None', 'pdf_key': 'None', 'trade_code': '600383', 'sheet_type': '合并报表', 'table_type': '资产负债表', 'end_date': '20171231'},)

# {'compare_source': 'wind', 'msg': '键在wind中而不在jindi中', 'wind_key': '所有者权益', 'wind_value': 'None', 'pdf_key': 'None', 'trade_code': '600383', 'sheet_type': '合并报表', 'table_type': '资产负债表', 'end_date': '20171231'}


import xlwt
import itertools
from elasticsearch import Elasticsearch
# es = Elasticsearch(hosts='192.168.31.99:9200')
workbook = xlwt.Workbook()
table_list = ['资产负债表', '利润表', '现金流量表']
type_list = ['合并报表', '母公司报表', '合并报表（调整）','母公司报表（调整）']
index_name = 'error_compare_result'

# {"query":{"bool":{"must":[{"term":{"table_type.keyword":"资产负债表"}},{"term":{"sheet_type.keyword":"合并报表（调整）"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}
for i,j in itertools.product(table_list, type_list):
	data = {"query":{"bool":{"must":[{"term":{"table_type.keyword":i}},{"term":{"sheet_type.keyword":j}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}
	# result = es.search(index=index_name, doc_type = 'd_type',body = data)['hits']['hits']
	
	print('正在读取--{}--{}--'.format(i, j))
	result = es.search(index=index_name, doc_type='d_type',body = data)['hits']['hits']




# worksheet = workbook.add_sheet('')

