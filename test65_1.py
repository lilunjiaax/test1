import xlrd
from pandas import DataFrame
import itertools
from elasticsearch import Elasticsearch
es = Elasticsearch(hosts='127.0.0.1:9200')
index_name = 'wind_wss_index'

workbook = xlrd.open_workbook('house_c.xlsx')

data_sheet = workbook.sheets()[0]

print(data_sheet.name)

row = data_sheet.nrows  # 行数
col = data_sheet.ncols  # 列数

code_list = []

for i in range(row):
	code_list.append(data_sheet.cell_value(i,0))

code_list = code_list[1:]

# print(code_list)

num_dict = {}
for item in code_list:
	data = {"query":{"bool":{"must":[{"term":{"trade_code.keyword":item}}],"must_not":[],"should":[]}},"from":0,"size":1000,"sort":[],"aggs":{}}
	result = es.search(index=index_name, doc_type = 'd_type', body = data)['hits']['hits']
	num_dict.update({item: len(result)})

for i in num_dict:
	print('---{}---{}----'.format(i, num_dict[i]))




