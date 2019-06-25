import xlwt
import itertools
from elasticsearch import Elasticsearch
es = Elasticsearch(hosts='127.0.0.1:9200')

workbook = xlwt.Workbook(encoding='ascii')
table_list = ['资产负债表', '利润表', '现金流量表']
type_list = ['合并报表', '母公司报表', '合并报表（调整）','母公司报表（调整）']

# 建立列数对照字典
col_dict = {'msg':1, 'wind_value':2, 'pdf_value':3, 'wind_key':4, 'pdf_key':5, 'end_date':6}
index_name = 'error_compare_result_2'

def first_write(worksheet):
	'''写每一个sheet的第一行导航栏'''
	for i in col_dict:
		col = col_dict[i]
		worksheet.write(0, col, label = i)


for i,j in itertools.product(table_list, type_list):
	row_num = 1
	worksheet = workbook.add_sheet(i+j)
	data = {"query":{"bool":{"must":[{"term":{"table_type.keyword":i}},{"term":{"sheet_type.keyword":j}}],"must_not":[],"should":[]}},"from":0,"size":1000,"sort":[],"aggs":{}}
	result = es.search(index=index_name, doc_type = 'd_type', body = data)['hits']['hits']
	# print(result)
	print(len(result))
	first_write(worksheet)
	for item in result:
		item_list = item['_source']
		# print(item)
		for key in item_list:
			if key in col_dict:
				col = col_dict[key]
				worksheet.write(row_num, col, label=item_list[key])
		row_num += 1
	

workbook.save('error_result_2.xls')















