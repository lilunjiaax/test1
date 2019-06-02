import xlwt
import itertools

workbook = xlwt.Workbook(encoding='ascii')
table_list = ['资产负债表', '利润表', '现金流量表']
type_list = ['合并报表', '母公司报表', '合并报表（调整）','母公司报表（调整）']

for i,j in itertools.product(table_list, type_list):
	worksheet = workbook.add_sheet(i+j)
	worksheet.write(0,1,label=i)
	worksheet.write(1,2,label=j)




workbook.save('error.xls')















